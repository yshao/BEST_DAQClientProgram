import time
import serial
import matplotlib.pyplot as plt
import numpy as np
from pyfirmata import Arduino#, util

### User Input ###
COMPORT="COM3"
GPIB_ADDR="16"
BOARD = Arduino('COM4')
Fpoints=401
Fstart = 20
Fstop = 26.4
Tmeas = 2.0
portMeas = ['A','B','R']#'A'#
psState = ((0,1,0,1),(0,0,1,1))
saveDirectory = 'C:\Users\Lab\Desktop\BEST LabBench\TestData\PRACO\Serial 3'
saveFile = '\PRACO22to30s3_Carrier1Test_%sto%sGHz' %(Fstart, Fstop)
headerString = 'Branch 1 Out on Port A; Branch 2 Out on Port B; Input Reference on Port R'
#==============================================================================
if __name__ == '__main__':
    #### Initialize Local Variables ####
    comport = COMPORT # Prologix Serial Port
    addr = GPIB_ADDR # HP33120A GPIB address
    board = BOARD
    points = Fpoints # Number of waveform data Fpoints
    # 101, 201, or 401 points required
    if (points != 101) and (points != 201) and (points != 401):
        print "Select points = 101, 201, or 401."
        exit(1)
    freq = np.linspace(Fstart, Fstop, points, endpoint=True)
    data = freq
    
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
        ser.close()
        board.exit()
        exit(1)
    
    #### Set-Up Instrument ####  
    ser.write('++auto 0\n') # Turn Read-After-Write Off
    ser.write('C2;\n') # Channel 2 Active
    ser.write('C0;\n') # Turn Channel 2 Off
    ser.write('C1;\n') # Channel 1 Active
    
    #### Perform Measurement ####
    portString = ''
    psStateString = ' ,'
    for jj in range(0,len(psState[1])):
        board.digital[12].write(psState[0][jj])
        board.digital[11].write(psState[1][jj])
        psStateString = psStateString+'PS'+str(psState[0][jj])+str(psState[1][jj])+','*len(portMeas)
        for ii in range(0, len(portMeas)):
            ser.write('I' + portMeas[ii] + ';\n') # Select Input ii
            time.sleep(Tmeas) # Wait for trace to update
            ser.write('OD;\n') # Output trace data
            ser.write('++read eoi;\n') # Issue read command
            dataS = ser.read(999999); # Read the serial buffer
            dataS = dataS.split(',') # Split single string with comma seperation
            dataA = np.array([float(x) for x in dataS]) # Format data
            data = np.column_stack((data,dataA))
            portString = portString + ',P' + portMeas[ii] + '(dBm)'
    
    #### Plot Data ####
    for ii in range(0, data.shape[1]-1):
        plt.plot(freq,data[:,ii+1], label=('Trace', ii+1))
    plt.title('VNA Output')
    plt.ylabel('Power (dB)')
    plt.xlabel('Frequency (GHz)')
    plt.legend()
    plt.show()
    
    #### Release Instrument Control ####
    ser.write('++mode 1\n') # Return Prologix to talk mode
    ser.write('++auto 1\n') # Turn Read-After-Write On   
    ser.close() # Release serial port 
    board.exit()
    #### Save Data ####  
    headerString = headerString+'\n'+psStateString+'\nfreq(GHz)' + portString    
    np.savetxt(saveDirectory + saveFile + '.csv', data, delimiter=',',header=headerString,comments='')
