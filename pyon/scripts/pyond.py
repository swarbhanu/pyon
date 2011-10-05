
import yaml

from pyon.container import runner
from pyon.container import container

class ContainerOptions(runner.Options):
    """
    """

    def set_options(self):
        self.parser.add_argument('-d', '--daemon', action='store_true', help="Daemonize")
        self.parser.add_argument('--pidfile', default='pyond.pid', help="Name of pidfile")
        # broker options? Exchange space name? list spaces option?
        # It would be better to have an exchange space config file
        # installed in the system. This would allow the user/dev to specify
        # pre configured (authoritative or local) exchange spaces. So, an
        # exchange space name maps to a broker connection configuration.
        self.parser.add_argument('--broker_host', default='localhost')
        self.parser.add_argument('--broker_port', type=int, default=5672)
        self.parser.add_argument('--broker_vhost', default='/')


    def Xparse_args(self, tokens):
        # Exploit yaml's spectacular type inference (and ensure consistency with config files)
        args, kwargs = [], {}
        for token in tokens:
            token = token.lstrip('-')
            if '=' in token:
                key,val = token.split('=', 1)
                kwargs[key] = yaml.load(val)
            else:
                args.append(yaml.load(token))

        #return args, kwargs #?

class ContainerApplicationRunner(runner.Runner):
    """
    Capability container entry point class
    """

    def pre_application(self):
        """
        Load ion objects like in bootstrap file
        """

    def post_application(self):
        #self.start_application(self.application)
        cont_root = container.Container(self.config)
        self.application.set_parent(cont_root)
        self.cont_root = cont_root
        self.cont_root.start()

    def start_application(self, application):
        """
        Configure container specific things and run application.
        """
        if daemon:
            with DaemonContext(pidfile=pidfile):
                #main entry point
                pass

def run_app(config):
    """
    Like a typical main function, except instead of argv, we have a
    tailored config object.
    """
    ContainerApplicationRunner(config).run()

def run():
    """
    External entry point to call from bin script.
    """
    runner.run(run_app, ContainerOptions)

