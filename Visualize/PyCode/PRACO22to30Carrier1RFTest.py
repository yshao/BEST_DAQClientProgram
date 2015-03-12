import time
import serial
import matplotlib.pyplot as plt
import numpy as np

### User Input ###
COMPORT="COM3"
GPIB_ADDR="16"
Fpoints=401
Fstart = 21.5
Fstop = 22.5
Tmeas = 2.0
#saveFile = 'PRACO22to30s2_Carrier1Test_21.5to22.5GHz_NDPS011'
#headerString = 'Branch 1 Out on Port A; Branch 2 Out on Port B; Input Reference on Port R\n'
#headerString = headerString + 'ND off; PS1 high; PS2 high'
saveFile = 'Test'
headerString = 'Test'
#==============================================================================
if __name__ == '__main__':
  #### Initialize Local Variables ####
  comport = COMPORT # Prologix Serial Port
  addr = GPIB_ADDR # HP33120A GPIB address
  points = Fpoints # Number of waveform data Fpoints
  # 101, 201, or 401 points required
  if (points != 101) and (points != 201) and (points != 401):
      print "Select points = 101, 201, or 401."
      exit(1)
  freq = np.linspace(Fstart, Fstop, points, endpoint=True)

  #### Initialize Instrument ####
  ser = serial.Serial( comport, 9600, timeout=0.5 ) # Open serial port
  ser.write('++auto 1\n') # Turn Read-After-Write On
  ser.write('++addr ' + addr + '\n') # Send SNA address to Prologix
  ser.write('OI;\n') # Ping SNA
  s = ser.read(256);
  if (len(s) > 0)and(s == '8757E REV 4.3\n'):
      print 'Now Controlling ' + s
  else:
      print "Cannot Talk to Instrument."
      exit(1)
  
  #### Set-Up Instrument ####  
  ser.write('++auto 0\n') # Turn Read-After-Write Off
  ser.write('C2;\n') # Channel 2 Active
  ser.write('C0;\n') # Turn Channel 2 Off
  ser.write('C1;\n') # Channel 1 Active
  #### Perform Measurement ####
  # Input A Power Measurement
  ser.write('IA;\n') # Select Input A
  time.sleep(Tmeas) # Wait for trace to update
  ser.write('OD;\n') # Output trace data
  ser.write('++read eoi;\n') # Issue read command
  dataS = ser.read(999999); # Read the serial buffer
  dataS = dataS.split(',') # Split single string with comma seperation
  dataA = np.array([float(x) for x in dataS]) # Format data
  # Input B Power Measurement
  ser.write('IB;\n') # Select Input B
  time.sleep(Tmeas) # Wait for trace to update
  ser.write('OD;\n') # Output trace data
  ser.write('++read eoi;\n') # Issue read command
  dataS = ser.read(999999); # Read the serial buffer
  dataS = dataS.split(',') # Split single string with comma seperation
  dataB = np.array([float(x) for x in dataS]) # Format data
  # Input R Power Measurement
  ser.write('IR;\n') # Select Input R
  time.sleep(Tmeas) # Wait for trace to update
  ser.write('OD;\n') # Output trace data
  ser.write('++read eoi;\n') # Issue read command
  dataS = ser.read(999999); # Read the serial buffer
  dataS = dataS.split(',') # Split single string with comma seperation
  dataR = np.array([float(x) for x in dataS]) # Format data
  
  #### Plot Data ####
  plt.plot(freq,dataA,'r',freq,dataB,'b',freq,dataR,'k')
  plt.title('VNA Output')
  plt.ylabel('Power (dBm)')
  plt.xlabel('Frequency (GHz)')
#  plt.legend('Port A','Port B','Port R')
  plt.show()
  
  #### Release Instrument Control ####
  ser.write('++mode 1\n') # Return Prologix to talk mode
  ser.write('++auto 1\n') # Turn Read-After-Write On   
  ser.close() # Release serial port 
  #### Save Data ####
  headerString = headerString + '\nfreq(GHz),PA(dBm),PB(dBm),PR(dBm)'   
  data = np.array(zip(freq,dataA,dataB,dataR))
  np.savetxt(saveFile + '.csv', data, delimiter=',',header=headerString,comments='')

