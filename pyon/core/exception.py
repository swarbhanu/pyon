#!/usr/bin/env python
from collections import OrderedDict

__author__ = 'Thomas R. Lennan'
__license__ = 'Apache 2.0'

BAD_REQUEST = 400
UNAUTHORIZED = 401
NOT_FOUND = 404
TIMEOUT = 408
CONFLICT = 409
SERVER_ERROR = 500
SERVICE_UNAVAILABLE = 503

import traceback
import inspect
import sys

def _default_stack_formatter(label, stack):
    yield '--- %s ---'%label
    for f,l,m,c in stack:
        yield '%s:%d\t%s'%(f,l,c)

class IonException(Exception):
    status_code = -1

    def __init__(self, *a, **b):
        super(IonException,self).__init__(*a,**b)
        self._stacks = []
        self._stacks.append(('__init__', traceback.extract_stack()))

    def get_status_code(self):
        return self.status_code

    def get_error_message(self):
        return self.message

    def add_stack(self, label, stack):
        self._stacks.append((label, stack))

    def get_stacks(self, trim=True):
        return self._stacks

    # TODO: filter should become an iterator that takes the full stack
    # TODO: and emits just the frames of interest.  otherwise don't have enough context.
    def format_stack(self, formatter=_default_stack_formatter):
        """ return a multiline string representation of the stacks in this exception

            by default, the string has one section for each stack
            and each section shows the label then each stack element as "file:line code"

            a formatter generator function can alter how and which of these lines are printed.
            it should take a label and stack (list of tuples) as arguments
            and yield string lines to be printed.
        """
        lines = []
        for label, stack in self._stacks:
            lines += formatter(label,stack)
        return '\n'.join(lines)

    def __str__(self):
        return str(self.get_status_code()) + " - " + str(self.get_error_message())

class BadRequest(IonException):
    '''
    Incorrectly formatted client request
    '''
    status_code = 400

class Unauthorized(IonException):
    '''
    Client failed policy enforcement
    '''
    status_code = 401

class NotFound(IonException):
    ''''
    Requested resource not found
    '''
    status_code = 404

class Timeout(IonException):
    '''
    Client request timed out
    '''
    status_code = 408

class Conflict(IonException):
    '''
    Client request failed due to conflict with the current state of the resource
    '''
    status_code = 409

class Inconsistent(IonException):
    '''
    Client request failed due to internal error of the datastore
    '''
    status_code = 410

class ServerError(IonException):
    '''
    For reporting generic service failure
    '''
    status_code = 500

class ServiceUnavailable(IonException):
    '''
    Requested service not started or otherwise unavailable
    '''
    status_code = 503

class ConfigNotFound(IonException):
    '''
    '''
    status_code = 540

class ContainerError(IonException):
    '''
    '''
    status_code = 550

class ContainerConfigError(ContainerError):
    '''
    '''
    status_code = 551

class ContainerStartupError(ContainerError):
    '''
    '''
    status_code = 553

class ContainerAppError(ContainerError):
    '''
    '''
    status_code = 554

class IonInstrumentError(IonException):
    """
    """
    status_code = 600
    
class InstConnectionError(IonInstrumentError):
    """
    """
    status_code = 610
    
class InstNotImplementedError(IonInstrumentError):
    """
    """
    status_code = 620
    
class InstParameterError(IonInstrumentError):
    """
    """
    status_code = 630

class InstProtocolError(IonInstrumentError):
    """
    """
    status_code = 640

class InstSampleError(IonInstrumentError):
    """
    """
    status_code = 650

class InstStateError(IonInstrumentError):
    """
    """
    status_code = 660

class InstUnknownCommandError(IonInstrumentError):
    """
    """
    status_code = 670

class InstDriverError(IonInstrumentError):
    """
    """
    status_code = 680

class InstTimeoutError(IonInstrumentError):
    """
    """
    status_code = 690



# must appear after ServerError in python module
class ExceptionFactory(object):
    def __init__(self, default_type=ServerError):
        self._default = default_type
        self._exception_map = {}
        for name, obj in inspect.getmembers(sys.modules[__name__]):
            if inspect.isclass(obj):
                if hasattr(obj, "status_code"):
                    self._exception_map[str(obj.status_code)] = obj
    def create_exception(self, code, message, stacks=None):
        """ build IonException from code, message, and optionally one or more stack traces """
        if str(code) in self._exception_map:
            out = self._exception_map[str(code)](message)
        else:
            out = self._default(message)
        if stacks:
            for label,stack in stacks:
                out.add_stack(label,stack)
        return out
