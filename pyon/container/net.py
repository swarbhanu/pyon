
from pyon.container import service
from pyon.net import endpoint

class RPCServer(service.Service):
    """
    A pyon container service that starts and stops an RPCServer listener

    Set the parent of this to be the container application
    """

    def __init__(self, name, s):
        """
        s should be Endpoint Factory, but the Endpoint Factory still
        requires node as an arg. See if that can be removed
        """
        self.name = name
        self.service = s

    def start(self):
        """
        The listen call should not block.
        That loop should be set up in a greenlet, and returned by the
        listen call so this service can start and stop the greenlet.
        """
        service.Service.start(self)
        f = endpoint.RPCServer(node=self.parent.parent.node,
                            name=self.name,
                            service=self.service)
        self.l = endpoint.BinderListener(node=self.parent.parent.node, 
                            name=self.name,
                            endpoint_factory=f)
        self.l.listen() # This blocks! F, this isn't gonna work

    def stop(self):
        """
        this will control the listening greenlet.
        """
        service.Service.stop(self)

class RPCClient(service.Service):
    """
    """
