#from os import *   #Import all of os

import os.path
import sys
import array
import time
import serial

# ********************
# options
# ********************
COMPORT="COM3"
GPIB_ADDR="16"
POINTS=400

# Special characters to be escaped
LF   = 0x0A
CR   = 0x0D
ESC  = 0x1B
PLUS = 0x2B





#==============================================================================
def IsSpecial(data):
    return data in (LF, CR, ESC, PLUS)

    
#==============================================================================
def CheckError():
    ser.write("SYST:ERR?\n")
    ser.write("++read eoi\n")
    s = ser.read(100)
    print s


#==============================================================================
if __name__ == '__main__':

#    if len( sys.argv ) != 4:
#        print "Usage: ", os.path.basename( sys.argv[0] ), "<COM port> <HP33120A GPIB address> <points>"
#        sys.exit(1)

    # Prologix GPIB-USB Controller serial port
    comport = COMPORT

    # HP33120A GPIB address
    addr = GPIB_ADDR
    
    # Number of waveform data points
    points = POINTS
    
    # 8-16000 points required
    if points < 8:
        print "Too few points."
        exit(1)

    if points > 16000:
        print "Too many points."
        exit(1)

    try:
        # Waveform points are in short int (16-bit) array
        data = array.array('H');

        # Create waveform data. Simple ramp up and down.    
        for i in range(points/2):
            data.append((i * 2047)/(points/2))

        for i in range(points/2):
            data.append((((points/2)-i) * 2047)/(points/2))

        # Swap bytes so MSB is first. (Required on Windows)
        data.byteswap()

        # Output data is in byte array
        outdata = array.array('B');

        # Build output data, escaping all special characters        
        for byte in data.tostring():
            if IsSpecial(ord(byte)):
                outdata.append(ESC)
                
            outdata.append(ord(byte))                    

        # Open serial port
        ser = serial.Serial( comport, 9600, timeout=0.5 )

        # Set mode as CONTROLLER
        ser.write("++mode 1\n")
        
        # Set HP33120A address
        ser.write("++addr " + addr + "\n")

        # Turn off read-after-write to avoid "Query Unterminated" errors
        ser.write("++auto 0\n")

        # Do not append CR or LF to GPIB data
        ser.write("++eos 3\n")

        # Assert EOI with last byte to indicate end of data
        ser.write("++eoi 1\n")

#******************************
# scripts starts here
#******************************
    
        # Reset AWG 
        cmd = "*RST"
        print cmd
        ser.write(cmd + "\n")        

        time.sleep(1.0)
        CheckError()        

  ###      # Format output data command. Use length of points array, NOT output array
        datalen = len(data) * 2
        
        cmd = "DATA:DAC VOLATILE, #" + str(len(str(datalen))) + str(datalen)
        print cmd
        
        # Write binary block data
        ser.write(cmd)
        ser.write(outdata.tostring())

        # Terminate USB command string
        ser.write("\n")

        time.sleep(0.5)
        CheckError()        
   
   ###
        
        cmd = "DATA:COPY PULSE, VOLATILE"
        print cmd

        ser.write(cmd + "\n")
        time.sleep(2.0)     
        CheckError()        

   ###
   
        cmd = "FUNC:USER PULSE"
        print cmd

        ser.write(cmd + "\n")
        time.sleep(1)
        CheckError()        

   ###
        cmd = "FUNC:SHAP USER"
        print cmd

        ser.write(cmd + "\n")
        time.sleep(0.5)
        CheckError()        

   ###

        cmd = "OUTP:LOAD 50"
        print cmd

        ser.write(cmd + "\n")
        time.sleep(0.5)
        CheckError()        

   ###

        cmd = "FREQ 5000;VOLT 0.5"
        print cmd

        ser.write(cmd + "\n")
        time.sleep(0.5)
        CheckError()        
    ###
    
      input=raw_input("Presss enter when ready")
    
    
        
    except serial.SerialException, e:
        print e
        