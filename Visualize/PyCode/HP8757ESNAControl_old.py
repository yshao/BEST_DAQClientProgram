#import os.path
#import sys
#import array
#import time
import serial
import matplotlib.pyplot as plt
import numpy as np

### User Input ###
COMPORT="COM3"
GPIB_ADDR="16"
POINTS=401
Fstart = 11
Fstop = 16



#==============================================================================
if __name__ == '__main__':
  
  # Prologix GPIB-USB Controller serial port
  comport = COMPORT
  
  # HP33120A GPIB address
  addr = GPIB_ADDR
  
  # Number of waveform data points
  points = POINTS
  freq = np.linspace(Fstart, Fstop, points, endpoint=True)
  
  # 101, 201, or 401 points required
  if (points != 101) and (points != 201) and (points != 401):
      print "Select points = 101, 201, or 401."
      exit(1)

  #### Initialize Instrument ####
  # Open serial port
  ser = serial.Serial( comport, 9600, timeout=0.5 )
  # Send SNA address to Prologix
  cmd = '++addr ' + addr
  print 'Sending:', cmd        
  ser.write(cmd + '\n')
  s = ser.read(256);
  if len(s) > 0:
      print s
  
  # Ping SNA
  cmd = 'OI;'
  print 'Sending:', cmd        
  ser.write(cmd + '\n')
  #time.sleep(1.0)
  s = ser.read(256);
  if len(s) > 0:
      print s
  if s != '8757E REV 4.3\n':
      print "Cannot Talk to Instrument."
      exit(1)
  
  cmd = 'OD;'    
  print 'Sending:', cmd        
  ser.write(cmd + '\n')    
  dataS = ser.read(999999);     
  dataA = np.array([float(x) for x in dataS.split(',')])
  
  plt.plot(freq,dataA)
  plt.ylabel('VNA Output (dB)')
  plt.xlabel('Frequency (GHz)')
  plt.show()
  

  # Return Prologix to talk mode
  cmd = '++mode 1'
  print 'Sending:', cmd        
  ser.write(cmd + '\n')
  s = ser.read(256);
  if len(s) > 0:
      print s 
  # Release serial port    
  ser.close()
      
  data = np.array(zip(freq,dataA))
  np.savetxt("test.csv", data, delimiter=",")

# Use following to prob instrument states      
#  cmd = '++auto'
#  print 'Sending:', cmd        
#  ser.write(cmd + '\n')
#  s = ser.read(256);
#  if len(s) > 0:
#      print s 
#      
#  cmd = '++mode'
#  print 'Sending:', cmd        
#  ser.write(cmd + '\n')
#  s = ser.read(256);
#  if len(s) > 0:
#      print s 
