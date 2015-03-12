# -*- coding: utf-8 -*-
"""
Created on Thu Aug 14 16:22:42 2014

@author: Lab

This Script Kicks Ass
IT WORKS
refer to doc

https://pypi.python.org/pypi/pyFirmata

"""
from pyfirmata import Arduino, util
import serial

board = Arduino('COM4')
board.digital[12].write(1)

board.digital[2].write(1)

board.digital[5].write(1)

board.digital[7].write(1)
board.digital[7].write(0)
ser.close()