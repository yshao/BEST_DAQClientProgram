import math




D1 = 8088880
D2 = 8072160

C1 = 40439
C2 = 36650
C3 = 23486
C4 = 22888
C5 = 31179
C6 = 28619

SH = 26364.

ST = 19270.


dr=(D1,D2,C1,C2,C3,C4,C5,C6,SH,ST)


# print 2**8
#
# print 'dT'
# print dT

def convert_data(dr):
    ""
    ### pressure conversion
# variable Description/Equation variable size bit size value(min) value(max) example
# C1 Pressure sensitivity | SENST1 unsigned int 16 16 0 65535 40127
# C2 Pressure offset | OFFT1 unsigned int 16 16 0 65535 36924
# C3 Temperature coefficient of pressure sensitivity | TCS unsigned int 16 16 0 65535 23317
# C4 Temperature coefficient of pressure offset | TCO unsigned int 16 16 0 65535 23282
# C5 Reference temperature TREF unsigned int 16 16 0 65535 33464
# C6 Temperature coefficient of the temperature | TEMPSENS unsigned int 16 16 0 65535 28312
# D1 Digital pressure value unsigned int 32 24 0 16777216 9085466
# D2 Digital temperature value unsigned int 32 24 0 16777216 8569150

    ### convert pressure sensor data
    D1 = dr[0]
    D2 = dr[1]

    C1 = dr[2]
    C2 = dr[3]
    C3 = dr[4]
    C4 = dr[5]
    C5 = dr[6]
    C6 = dr[7]


    dT = D2 - C5 * 2**8

    TEMP = 2000 + dT * C6 / 2**23

    OFF = C2 * 2**16 + (C4 * dT ) / 2**7

    SENS = C1 * 2**15 + (C3 * dT ) / 2**8

    P = (D1 * SENS / 2**21 - OFF) / 2**15

    print P

    TEMP = TEMP/100.

    P = P * 0.0145037738




    ### convert humidity sensor data

    SH=dr[8]
    ST=dr[9]

    print (SH/2**16)

    RH = 125*(SH/2**16) - 6
    print RH

    Bw = 17.62
    Lw = 243.12
    Bi = 22.46
    Li = 272.62

    RHi = RH * math.exp(Bw * TEMP/(Lw+TEMP))/math.exp(Bi*TEMP/(Li+TEMP))


    T = -46.85 + 175.72*(ST/2**16)



    return TEMP,P,RH,T,RHi

print convert_data(dr)
