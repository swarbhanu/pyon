#!/usr/bin/env python
#
# File generated on 2011-12-15 13:36:46.552744
#
# Author: Swarbhanu Chatterjee
#
# Description: For HDF Messaging
#

from zope.interface import Interface, implements
from collections import OrderedDict, defaultdict

from pyon.service.service import BaseService, BaseClients
from pyon.net.endpoint import RPCClient, ProcessRPCClient

from interface.services.examples.hello.ihello_service import HelloServiceClientMixin

class HDFHelloServiceClient(RPCClient, HelloServiceClientMixin):
    def __init__(self, name=None, node=None, **kwargs):
        name = name or 'hdf_hello'
        RPCClient.__init__(self, name=name, node=node, **kwargs)
        HelloServiceClientMixin.__init__(self)

