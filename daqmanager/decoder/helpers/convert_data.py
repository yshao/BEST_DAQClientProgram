import pandas as pd
import math

def convert_enc_data(encData):
    ""


def convert_rad_data(radData):
    ""


def convert_inu_data(inuData):
    ""

def convert_gps_data(gpsData):
    ""


def convert_MS_data(Pdata,Tdata,drc):
    ""
    ### pressure conversion
# variable Description/Equation variable size bit size value(min) value(max) example
# C1 Pressure sensitivity | SENST1 unsigned int 16 16 0 65535 40127
# C2 Pressure offset | OFFT1 unsigned int 16 16 0 65535 36924
# C3 Temperature coefficient of pressure sensitivity | TCS unsigned int 16 16 0 65535 23317
# C5 Reference temperature TREF unsigned int 16 16 0 65535 33464
# C6 Temperature coefficient of the temperature | TEMPSENS unsigned int 16 16 0 65535 28312
# D1 Digital pressure value unsigned int 32 24 0 16777216 9085466
# D2 Digital temperature value unsigned int 32 24 0 16777216 8569150

    ### convert pressure sensor data
    D1 = Pdata
    D2 = Tdata

    print drc

    C1 = drc[0]
    C2 = drc[1]
    C3 = drc[2]
    C4 = drc[3]
    C5 = drc[4]
    C6 = drc[5]



    d=pd.DataFrame()
    d['D1']=D1
    d['D2']=D2
    d['dT'] = d.D2 - C5 * 2**8

    d['TEMP'] = 2000 + d.dT * C6 / 2**23

    d['OFF'] = C2 * 2**16 + (C4 * d.dT ) / 2**7

    d['SENS'] = C1 * 2**15 + (C3 * d.dT ) / 2**8

    d['P'] = (d.D1 * d.SENS / 2**21 - d.OFF) / 2**15

    print d
    return d

def convert_SHT_data(Hdata,Tdata):
    ### convert humidity sensor data

    SH=Hdata
    ST=Tdata

    print SH
    print ST
    d=pd.DataFrame()

    # print (SH/2**16)

    # d['RH'] = 125*(SH/2**16) - 6
    RH = 125*(SH/2**16) - 6
    T= 175.72*(ST/2**16) - 46.85

    # print d.T
    # print d.RH
    # print d.T


    # d.RH.astype(float)
    # d.T.astype(float)

    Bw = 17.62
    Lw = 243.12
    Bi = 22.46
    Li = 272.62

    # d['T'] = 20.11 #-46.85 + 175.72*(d.T/2**16)
    print d.T
    print Bw * d.T/(Lw+d.T)
    print Bi*d.T/(Li+d.T)
    d['RHi'] = RH * math.exp(Bw * T/(Lw+ T))/math.exp(Bi* T/(Li+ T))

    return d

# def insert_selected_columns(db,cols):
#
#     if flavor=='sqlite' or flavor=='odbc':
#         wildcards = ','.join(['?'] * len(frame.columns))
#         insert_sql = 'INSERT INTO %s VALUES (%s)' % (name, wildcards)
#         #print 'insert_sql', insert_sql
#         data = [tuple(x) for x in frame.values]
#         #print 'data', data
#         cur.executemany(insert_sql, data)