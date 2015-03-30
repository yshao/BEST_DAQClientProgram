#!/usr/bin/python
 
import binascii
 
def calcCheckSum(incoming):
    msgByte = hexStr2Byte(incoming)
    check = 0
    for i in msgByte:
        check = AddToCRC(i, check)
    return check
 
def AddToCRC(b, crc):
    b2 = b
    if (b < 0):
        b2 = b + 256
    for i in xrange(8):
        odd = ((b2^crc) & 1) == 1
        crc >>= 1
        b2 >>= 1
        if (odd):
            crc ^= 0x8C # this means crc ^= 140
    return crc
 
def hexStr2Byte(msg):
    hex_data = msg.decode("hex")
    msg = bytearray(hex_data)
    return msg
    
if __name__ == '__main__':
    import sys
 
    # msg = sys.argv[1]
    msg='4888'
    print "CRC-8 Maxim/Dallas: %s " % hex(calcCheckSum(msg))