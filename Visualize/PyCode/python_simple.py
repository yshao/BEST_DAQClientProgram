import os.path
import serial
import sys

# ********************
# options
# ********************
COMPORT="COM3"
GPIB_ADDR="16"
POINTS=401


if __name__ == '__main__':

    #if len( sys.argv ) != 3:
      #  print "Usage: ", os.path.basename( sys.argv[0] ), "<COM port> <GPIB address>"
       # sys.exit(1)

    comport = COMPORT
    addr = GPIB_ADDR
    
    ser = serial.Serial()
    
    try:
        success = True
        
        #ser = serial.Serial( '\\\\.\\'+sys.argv[1], 9600, timeout=0.5 )
        ser = serial.Serial( comport, 9600, timeout=0.5 )
        ### 

        cmd = '++mode 1'
        print 'Sending:', cmd        
        ser.write(cmd + '\n')
        s = ser.read(256);
        if len(s) > 0:
            print s


        ### 

        cmd = '++addr ' + addr
        print 'Sending:', cmd        
        ser.write(cmd + '\n')
        s = ser.read(256);
        if len(s) > 0:
            print s

        ### 

        cmd = '++auto 1'
        print 'Sending:', cmd        
        ser.write(cmd + '\n')
        s = ser.read(256);
        if len(s) > 0:
            print s


        ### reads data from analyzer 

        cmd = 'plot;'
        print 'Sending:', cmd        
        ser.write(cmd + '\n')


        

        f = open("plot.bin", "wb")
        
        while (1):
            s = ser.read(1000)           
            if len(s) > 0:
                f.write(s)
            else:
                break

        f.close()
        
    except serial.SerialException, e:
        print e
        f.close()
        
    except KeyboardInterrupt, e:
        ser.close()
        f.close()

    