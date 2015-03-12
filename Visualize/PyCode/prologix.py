import serial, re
## from visa import instrument
from time import sleep
## import numpy as np
#import string

"""
--------------------------------------------------------------------
 Class to change the settings of the Prologix GPIB/USB Adapter vers. 6.0
 
 The commands implemented are not comprehensive.
 
 Note: Not all functions have been tested.
 
 My general convention (some based on Python convention...):
 
   .__function__()  built-in/reserved methods
   ._variable_      variables that are not callable...i.e. no '()' at end
   .InternalFunc()  initial capital letter indicates the function is called internally only
   .someCommand()   perform instrument commands/queries
   .MACRO_FUNC()    "macro" functions that do a whole bunch of things, like set up the instrument
   'SCRIPT: ...'     indicates the script is outputting information (as opposed to an instrument)

Revision History:
10 Aug 2010 (LNT)
 - Initial revision

USAGE EXAMPLE
        import prologix
        proctrl = prologix.GPIBUSB(4,12)
        #...
        print proctrl.ask('*idn?')
--------------------------------------------------------------------
"""

class GPIBUSB():
################################################################################
## Initialization
################################################################################
        def __init__(self, portNum=1, gpibAddr=12):
                self._serPort_ = portNum-1
                self._GPIBaddr_ = gpibAddr
                ## Port setup
                self.raw = serial.Serial(self._serPort_,9600,timeout=1,rtscts=True) #open the serial on COM n+1
                self.raw.write('++rst\n')
                sleep(5)
                self.setProController()         # set up as a controller
                self.write('++ifc')
                self.setProAddr(self._GPIBaddr_)                # set the controller's initial GPIB address
                print self.getProAddr()
                
        def openport(self):
                self.raw=serial.Serial(self._serPort_,9600,timeout=1) #open the serial on COM n+1
                        
        def closeport(self):
                self.raw.close()

################################################################################
## Basic I/O
################################################################################
        def write(self,buffer):
                return self.raw.write(buffer + '\n')
        
        def read(self):
                buffer = ''
                chunk = self.raw.read(1)
                buffer += chunk
                while chunk != '\n':
                        chunk = self.raw.read(1)
                        buffer += chunk
                return buffer.rstrip('\r'+'\n')
        
        def ask(self,buffer):
                self.write(buffer)
                return self.read()
                
################################################################################
## Settings (Pro is short for Prologix Unit)
################################################################################
        def ProAutoAsk(self,buffer):
                self.setProAuto()
                return self.ask(buffer)
        
        def ProAsk(self,buffer,eoi='\n'):
                self.clrProAuto()
                self.write(buffer)
                self.write('++read ' + eoi)
                return self.read()
                
        def setProAddr(self,newaddress):
                self.write('++addr'+str(newaddress))
                return self.ask('++addr')
                
        # Set the Prologix unit as a bus controller (master)
        def setProController(self):
                self.write('++mode 1')
                mode = self.ask('++mode')
                if mode == 1:
                        return 'controller'
                else:
                        return 'SCRIPT: mode changing failed'

        # Set the Prologix unit as a bus device (slave)
        def setProDevice(self):
                self.write('++mode 0')
                mode = self.ask('++mode')
                if mode == 0:
                        return 'device'
                else:
                        return 'SCRIPT: mode changing failed'
        
        # Automatically set to read after writing
        def setProAuto(self):
                self.raw.write('++auto 1\n')
                
        def clrProAuto(self):
                self.raw.write('++auto 0\n')
                
        def getProAddr(self):
                addr = self.ask('++addr')
                return addr