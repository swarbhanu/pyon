#!/usr/bin/env python

__author__ = 'Swarbhanu Chatterjee'

from pyon.util.log import log

from interface.services.examples.hello.ihello_service import BaseHelloService

from examples.service.hello_service import HelloService

import h5py
import numpy


class HDFHelloService(HelloService):

    def hello(self, text=''):
        log.debug("In hdf_hello_service.hello. Text=%s" % text)

        ### Do HDF Stuff here!

        # write the binary string to a new file
        f = open("myfile_check_server.hdf5", mode='wb')
        f.write(text)
        f.close()

        ## Do something with the file using h5py
        # use the core driver of h5Py to write an hdf file
        file = h5py.File('myfile_check_server.hdf5', mode = 'a', driver='core')
        # file = h5py.File('myfile_check2.hdf5', mode = 'w', driver='log')
        grp = file.create_group('anotherGroup')
        dataset2 = grp.create_dataset('dataset2', (10,10), '=f8', maxshape=(None,None))
        file['dataset2'] = numpy.ones((10,10))
        file.flush()
        file.close()

        # write the hdf file back into a string
        f = open("myfile_check_server.hdf5", mode='rb')
        # read the binary string representation of the file
        dataString = f.read()
        f.close()

        # return the string to the client
        return "%s" % dataString


