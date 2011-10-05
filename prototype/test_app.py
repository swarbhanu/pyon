

from zope.interface import implements

from interface.services.isample_service import ISampleService

from pyon.container import service 
from pyon.container import net

class SampleService(service.Service):
    implements(ISampleService)

    def doc_fields_(self, name='text_', time='datetime_', an_int='int_', a_float='float_', a_string='text_', none='???', a_dict='dict_', a_list='list_'):
        pass

    def sample_ping(self, name='', time='2011-07-27 02:59:43.100000', an_int=0, a_float=0.0, a_str='', none=None, a_dict={}, a_list=[]):
        pass

    def sample_other_op(self, foo='bar', num=84):
        pass

application = service.Application('Test Sample')
s = SampleService()
l = net.RPCServer('sample', s)
l.set_parent(application)
