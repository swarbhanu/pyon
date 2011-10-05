


class Service(object):

    name = None
    running = 0
    parent = None

    def start(self):
        self.running = 1

    def stop(self):
        self.running = 0

    def set_parent(self, parent):
        if self.parent is not None:
            self.disown_parent()
        self.parent = parent
        self.parent.add_service(self)

    def disown_parent(self):
        self.parent.remove_service(self)
        self.parent = None

class ServiceCollection(Service):

    def __init__(self):
        self.services = []

    def __iter__(self):
        return iter(self.services)

    def start(self):
        Service.start(self)
        for service in self:
            service.start()

    def stop(self):
        Service.stop(self)
        services = list(self)
        services.reverse()
        for service in services:
            service.stop() #this can block if the service stop needs to do
                           #things like save data or something

    def add_service(self, service):
        self.services.append(service)
        if self.running:
            service.start()

    def remove_service(self, service):
        self.services.remove(service)
        if self.running:
            return service.stop()

def Application(name=None):
    return ServiceCollection()
