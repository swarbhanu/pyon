"""
The Runner class provides the mechanics for invoking a Pyon application
from the command line (or, in a script if you want! just change the way the
Options parser gets the initial options list before for when parse_options
is called).

The Runner has a
 - Logger
 - an associate set of Options for configuring common Runner things,
   including anything the Logger needs.

This is the base Runner class that defines the fundamental Runner behavior.

The Logger class takes care of configuring the pyon logging
(pyon.util.log). If the Options specifies a config file, then it applies
that to the default logger.


"""

import argparse
import logging

from pyon import __version__ as version
from pyon.util.log import log
from pyon.util.config import Config
from pyon.util.misc import load_value_from_file


class Logger(object):
    """
    """

    def __init__(self, config):
        self._logfilename = config.get("log_filename")
        self._configfilename = config.get("log_config", "")
        self._config()

    def _config(self):
        """
        A default config is coded here to prevent requiring a config file
        for generic logging. All config options can be overridden by
        providing a log config file in the command line.
        """
        d = {'formatters': {
                'brief': {'format': '%(message)s'},
                'default': {'datefmt': '%Y-%m-%d %H:%M:%S', 'format': '%(asctime)s %(levelname)-8s %(name)-15s %(message)s'}
                },
             'handlers': {
                'console': {
                    'class': 'logging.StreamHandler', 
                    'formatter': 'brief',
                    'level': 'DEBUG',
                    'stream': 'ext://sys.stdout'
                    },
                'file': {
                    'backupCount': 3,
                    'class': 'logging.handlers.RotatingFileHandler',
                    'filename': self._logfilename,
                    'formatter': 'default',
                    'level': 'DEBUG',
                    'maxBytes': 1024
                    }
                },
             'loggers': {
                 'pyon': {'handlers': ['console', 'file'], 'level': 'WARN'}
                 },
             'version':1,
            }
        if self._configfilename:
            log_conf = Config([self._configfilename]).data
            d.updata(log_conf)
        logging.config.dictConfig(d)



    def start(self):
        """
        This could be used to control network based log handlers or
        something.
        Since python logging isn't really started, handlers are just added.
        """
        log.warn('Pyon Logging started')

    def stop(self):
        """
        """


class Runner(object):
    """
    Before the Application Runner can start, the messaging node needs to be
    completely activated.
    The bootstrap phase is for a specific set of core operational
    dependencies..(wait for these to start)
    The run phase is for any generic services to start (don't wait, just
    start; they do their own things and shouldn't inter-depend).
    """

    loggerFactory = Logger

    def __init__(self, config):
        self.config = config
        self.logger = self.loggerFactory(config)

    def run(self):
        self.pre_application()
        self.application = self.create_or_get_application()
        self.logger.start()
        self.post_application()
        self.logger.stop()

    def pre_application(self):
        """
        Implement specific actions in a subclass.
        """

    def post_application(self):
        """
        Implement specific actions in a subclass.
        """

    def create_or_get_application(self):
        """
        Load application from an app file or
        
        Create a generic application container that can have services added
        to it. 
        If a service is specified by name on the command line, use the
        service making mechanism to load service (service may be specified
        by name and config block)

        This is where you would hook in the mechanism that reads app or rel
        files. I'm not sure you should still use app and rel files, as
        those are literally copied from Erlang. Consider starting over with
        something simpler, that can leverage existing pythonic things (but
        not be too python specific...well, app and rel files are actually 
        Erlang specific...so, to make life easier, you could start from 
        something that is at least Pyton specific, and generalize from 
        there). 
        """
        if self.config['app_file']:
            return load_value_from_file(self.config['app_file'], 'application')

class Options(object):
    """
    Use argparse to define set of config options and to parse them from the
    command line. 
    Use pyon.util.config module to read a core config file.
    """
    description = """pyond Ion messaging Exchange and gevent services"""

    def __init__(self):
        self._init_parser()
        self.opts = {}
        self.app_file = None

    def _init_parser(self):
        self.parser = argparse.ArgumentParser(description=self.description)
        self.parser.add_argument('--version', action='version', version=version)
        self.parser.add_argument('--log_filename', default='pyond.log', help='Name of logfile')
        self.parser.add_argument('--log_config', help='Configuration for python logging levels')
        self.parser.add_argument('-c', '--pyon_config', help='Configuration for core pyond system, including messaging') # What should the default be?

        self.set_options()

    def set_options(self):
        """
        Add more specific options in a subclass.
        """

    def parse_options(self):
        opts, extra = self.parser.parse_known_args()
        print opts, extra
        self.opts = vars(opts)
        if extra:
            print 'fddfdf'
            self.parse_args(*extra)

        self.post_options()

    def post_options(self):
        """
        Called after options are parsed.

        Implement this to do something specific in a subclass.
        """
        if self.opts['pyon_config']:
            self.read_config()

    def parse_args(self, *args):
        """
        Implement specific extra arg handling
        """
        print args
        if args:
            self.app_file = args[0]
            print self.app_file
            self.opts['app_file'] = self.app_file
            print self.opts

    def read_config(self):
        cfg = Config([self.opts['pyon_config']]).data
        print cfg
        self.opts.update(cfg)
        print self.opts
        


def run(run_app, Options):
    """
    Generic run for all Runner implementations.
    At this point of execution the Options are parsed. This means we're
    using sys.argv, but it would be possible to use something else if
    necessary (some other list, not taken from the command line).
    """
    config = Options()
    config.parse_options() # uses argv
    run_app(config.opts)

def start_application(application):
    """
    Here we could add hooks to have the application get shutdown if the
    gevent gets shutdown...
    """
