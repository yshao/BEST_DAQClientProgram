def convert_data(dr):
    ""
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

    # print P

    TEMP = TEMP/100.

    P = P * 0.0145037738




    ### convert humidity sensor data

    SH=dr[8]
    ST=dr[9]

    # print (SH/2**16)

    RH = 125*(SH/2**16) - 6
    # print RH

    Bw = 17.62
    Lw = 243.12
    Bi = 22.46
    Li = 272.62

    RHi = RH * math.exp(Bw * TEMP/(Lw+TEMP))/math.exp(Bi*TEMP/(Li+TEMP))


    T = -46.85 + 175.72*(ST/2**16)



    return TEMP,P,RH,T,RHi