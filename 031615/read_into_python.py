import numpy as np
import matplotlib.pyplot as plt
from test.common.sqliteutils import *

def start_plot(d):
    ""
    #### Plot Data ####
    # f=d[:2]

    plt.plot(f,d,'r')
    plt.title('VNA Output')
    plt.ylabel('Power (dB)')
    plt.xlabel('Frequency (GHz)')
#    plt.legend('Port A','Port B','Port R')
    plt.show()



def main():
    db=DaqDB("daqRad.db")
    # db=DaqDB("daqEnc.db")

    x = np.array([(1.5,2.5,(1.0,2.0)),(3.,4.,(4.,5.)),(1.,3.,(2.,6.))],
        dtype=[('x','f4'),('y',np.float32),('value','f4',(2,2))])

    print x
    print x.shape


    data=db.load_data('rad')

    print data.shape

    # data=db.load_data('enc')

    print data
    start_plot(data)


main()