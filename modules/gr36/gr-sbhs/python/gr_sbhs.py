import gnuradio
from gnuradio import gr
import numpy
import serial
import time
from sbhs import *
from scan_machines import *

class gr_sbhs(gr.sync_block):

        def __init__(self):
                
                gr.sync_block.__init__(self,
                        name="gr_sbhs",
                        in_sig=[numpy.float32, numpy.float32],
                        out_sig=[numpy.float32])        
                
                from scan_machines import *
                print "Scanning Machines"
                scan_machines()

                # SBHS init
                self.new_device = Sbhs()
                self.new_device.connect(1)
                self.new_device.connect_device(0)


        def set_parameters(self,window):
                self.n = window
        
        # Check if value of window is integral of length of input source vector 
        # For cases like -> input = [3 , 4, 5 ,6] & window = 3
        def isIntegralWin(self, input_item, window):
                if (len(input_item) % window ):
                        raise Exception("Value of Window should be an integral value of length of input items")
                        
                
        def work(self, input_items, output_items):
                print "length of input item\n",len(input_items[0]) 
                print "value of input item\n",input_items[0][0]
                # Assuming input_items[0] and input_items[1] have same LENGTH
                for heat_items, fan_items in zip(input_items[0][:1], input_items[1][:1]):
                        
                        print "HEAT WRITTEN", heat_items
                        
                        # Set heat as 0 for negative values of heat
                        if heat_items < 0:
                                self.new_device.setHeat(0)
                        else:
                                self.new_device.setHeat(heat_items)

                        time.sleep(0.01)
                        self.new_device.setFan(fan_items)
                        time.sleep(0.01)
                
                # For Zero Temperatures
                if not self.new_device.getTemp():
                        raise Exception("Check SBHS connection, try re-plugging it and run scan_machines.py")

                # Get temperature
                output_items[0][:] =  numpy.float32(self.new_device.getTemp())

                print "Temperature: ",output_items[0][:1]
                return len(output_items[0])
