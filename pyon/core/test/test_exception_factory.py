
from pyon.core.exception import *

from nose.plugins.attrib import attr
from unittest import TestCase
import traceback

@attr('UNIT')
class TestExceptionUtils(TestCase):
    def setUp(self):
        self.subject = ExceptionFactory()
    def tearDown(self):
        self.subject = None

    def testCreateException(self):
        ex = self.subject.create_exception(553, 'test message')
        self.assertEqual(553, ex.status_code)
        self.assertEqual('test message', ex.message)
        self.assertTrue(isinstance(ex, ContainerStartupError))

        try:
            raise ex
            fail('should be unreachable')
        except ContainerStartupError:
            pass
        except:
            fail('should have caught this above')

    def testCreateWithStack(self):
        stack = traceback.extract_stack()
        ex = self.subject.create_exception(553, 'test2 message', [('added',stack)])
        self.assertEqual(553, ex.status_code)
        self.assertEqual('test2 message', ex.message)
        d = ex.get_stacks()
        labels = [ label for label,stack in ex.get_stacks() ]
        self.assertTrue('__init__' in labels)
        self.assertTrue('added' in labels)
        self.assertTrue(all(isinstance(stack,list) for label,stack in ex.get_stacks()))

    def testToString(self):
        stack = self.get_stack(3)
        ex = self.subject.create_exception(553, 'test2 message', [('added',stack)])
        msg1 = ex.format_stack()
        msg2 = ex.format_stack(formatter=self.custom_stack_format)
        self.assertTrue(len(msg1)>len(msg2))

    def get_stack(self, n):
        if n>0:
            return self.get_stack(n-1)
        else:
            return traceback.extract_stack()

    def custom_stack_format(self, label, stack):
        # does not display label like default formatter
        for f,l,m,c in stack:
            yield '%s:%d\t%s'%(f,l,c)
