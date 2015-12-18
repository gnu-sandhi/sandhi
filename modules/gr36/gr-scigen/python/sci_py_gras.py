#!/usr/bin/env python
# 
# Copyright 2014 <+YOU OR YOUR COMPANY+>.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

import numpy
from gnuradio import gr
import gras
import time
class sci_py_gras(gras.Block):
    """
    Executes a given scilab file. The output vector should have the same name as the var_name. Set_parameters function sets the parameters passed by the users through Sandhi. The file_import function auto-generates a code string of the scilab file and feeds it to sciscipy module for execution. It then reads the value of the 'var_name' variable in the scilab file and feeds it to the flowgraph.
    """
    def __init__(self):
        gras.Block.__init__(self,
            name="sci_py_gras",
            in_sig=[numpy.float32],
            out_sig=[numpy.float32])
	self.i = 0
	self.ret_array = []

    def set_parameters(self,path,window,var_name):
	self.path = path
	self.n = window
	self.var_name = var_name
	self.file_import()

    def file_import(self):
	import sciscipy
	f = open(self.path)
	x = f.read()
	x = x.split("\n")
	code_string = ""
	
	for i in range(0,len(x)):
		code_string += x[i]

	sciscipy.eval(code_string)
	self.ret_array = sciscipy.read(self.var_name)
	#print self.ret_array


    def work(self, input_items, output_items):
        #in0 = input_items[0]
        out = output_items[0]
	self.ret_array = numpy.array(self.ret_array)
        # <+signal processing here+>
	#print self.i
	self.i+=1
        #print self.i
	#print len(self.ret_array)

	if self.i >= len(self.ret_array):	#To reset the value of self.i
                self.i = 0
	
	#producing one value at a time
	output_items[0][:1] = numpy.array(self.ret_array[self.i])
	self.produce(0,1)	
	self.consume(0,1)
        #return len(output_items[0])
