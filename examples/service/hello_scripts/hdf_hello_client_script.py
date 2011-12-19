#!/usr/bin/env python

__author__ = 'Swarbhanu Chatterjee'

import h5py
import numpy

# use the core driver of h5Py to write an hdf file
file = h5py.File('myfile_check.hdf5', mode = 'w', driver='core')
#file = h5py.File('myfile_check2.hdf5', mode = 'w', driver='log')
grp = file.create_group('myGroup')
dataset = grp.create_dataset('dataset', (10,10), '=f8', maxshape=(None,None))
file['dataset'] = numpy.ones((10,10))
file.flush()
file.close()

# open the hdf5 file using python 'open()'
f = open("myfile_check.hdf5", mode='rb')
# read the binary string representation of the file
dataString = f.read()
f.close()

# Connecting to the server and sending the hdf file as a binary string
from interface.services.examples.hello.ihello_service import HelloServiceClient
hsc=HelloServiceClient(node=cc.node, name='hdf_hello')   # specifies the broker to connect to as cc.node
									   # cc is the container that automatically start when
									   # pycc is started.
dataString_fromServer = hsc.hello(dataString) # where dataString is some string

# write the binary string to a new file
f = open("myfile_check_out.hdf5", mode='wb')
f.write(dataString_fromServer)
