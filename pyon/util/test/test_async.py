#!/usr/bin/env python

__author__ = 'Adam R. Smith'
__license__ = 'Apache 2.0'

import unittest

from pyon.util.async import blocking_cb

class AsyncTest(unittest.TestCase):
    def i_call_callbacks(self, cb):
        cb(1, 2, 3, foo='bar')

    def test_blocking(self):
        a, b, c, misc = blocking_cb(self.i_call_callbacks, cb_arg='cb')
        self.assertEqual((a, b, c, misc), (1, 2, 3, {'foo': 'bar'}))
