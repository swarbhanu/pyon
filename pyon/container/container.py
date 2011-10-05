import gevent

from pyon.core.process import GreenProcessSupervisor
from pyon.container import service
from pyon.net import messaging
from pyon.util.log import log





class Container(service.ServiceCollection):
    node = None

    def __init__(self, config):
        """
        config arg is hack for now.
        should use exact args
        """
        service.ServiceCollection.__init__(self)
        self.proc_sup = GreenProcessSupervisor()
        self.config = config

    def start(self):
        """
        """
        log.debug("In Container.start")
        self.proc_sup.start() 
        self.node, self.ioloop = makeNode(self.config) # shortcut hack
        self.proc_sup.spawn('green', self.ioloop.join)
        service.ServiceCollection.start(self)

    def stop(self):
        """
        """
        service.ServiceCollection.stop(self)
        log.debug("In Container.stop")
        # TODO: Have a choice of shutdown behaviors for waiting on children, timeouts, etc
        self.proc_sup.shutdown(CFG.cc.timeout.shutdown)

    def listen_rpc(self, name, factory):
        """
        """





def makeNode(config):
    """
    blocking construction and connection of node
    """
    log.debug("In makeNode")
    node = messaging.NodeB()
    messagingParams = config['server']['amqp']
    log.debug("messagingParams: %s" % str(messagingParams))
    credentials = messaging.PlainCredentials(messagingParams["username"], messagingParams["password"])
    conn_parameters = messaging.ConnectionParameters(host=messagingParams["host"], virtual_host=messagingParams["vhost"], port=messagingParams["port"], credentials=credentials)
    connection = messaging.SelectConnection(conn_parameters , node.on_connection_open)
    ioloop_process = gevent.spawn(messaging.ioloop, connection)
    #ioloop_process = gevent.spawn(connection.ioloop.start)
    node.ready.wait()
    return node, ioloop_process
 
