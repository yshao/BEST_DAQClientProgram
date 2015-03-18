### humidity conversion
def SH_humidity_conversion(SH):
    ""
    RH = -6 + 125 * SH / 2 ** 16
    return RH

def SH_temp_conversion(ST):
    ""
    T = -46.85 + 175.72 * ST / 2**16
    return T


# RHtc = (T - 25) * (0.01 + 0.00008 * result) + RH


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


def pressure_conversion(D1,D2,calib):
    ""
    C1 = calib[0] #SENST1
    C2 = calib[1] #OFFT1
    C3 = calib[2] #TCS
    C4 = calib[3] #TCO
    C5 = calib[4] #TREF
    C6 = calib[5] #TEMPSENS

# D1 #pressure
# D2 #temp

    dT = D2 - C5 * 2 ** 8
    TEMP = 20 + dT*C6/ 2 ** 23
    OFF = C2 ** 2**16 + (C4 * dT)/2 ** 7
    SENS = C1 * 2**15 + (C3 * dT)/2 ** 8
    P = (D1 * SENS/2**21 - OFF)/2 ** 15

    return TEMP,P

# def main():
#
#
#     humidity_conversion()
#     pressure_conversion()

