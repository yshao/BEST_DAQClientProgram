import serial

### User Input ###
COMPORT="COM3"
GPIB_ADDR="16"

#==============================================================================
if __name__ == '__main__':
  #### Initialize Local Variables ####
  comport = COMPORT # Prologix Serial Port
  addr = GPIB_ADDR # HP33120A GPIB address
  #### Reset Instrument ####
  ser = serial.Serial( comport, 9600, timeout=0.5 ) # Open serial port
  ser.write('++addr ' + addr + '\n') # Send SNA address to Prologix
  ser.write('OI;\n') # Ping SNA
  s = ser.read(256);
  if (len(s) > 0)and(s == '8757E REV 4.3\n'):
      print 'Now Resetting ' + s
  else:
      print "Cannot Talk to Instrument."
      ser.close() # Release serial port
      exit(0)
  ser.write('++auto 0\n') # Turn Read-After-Write Off
  ser.write('IP;\n') # Reset SNA
  ser.write('++mode 1\n') # Return Prologix to talk mode
  ser.write('++auto 1\n') # Turn Read-After-Write On
  ser.close() # Release serial port