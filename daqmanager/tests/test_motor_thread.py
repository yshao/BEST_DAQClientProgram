__author__ = 'Ping'


class TimestampThread(object):
    UInt32("DateTime")

    def __init(self,struct_frame):
        self._frame=struct_frame

class InuTimerstampThread(TimestampThread):
    def __init__(self):
        UInt8("MData")
        UInt8("Razor_counter_hi")
        UInt8("Razor_counter_lo")

class EncTimestampThread(TimestampThread):
    def __init__(self):
        UInt8("MCTRL_1")
        UInt8("MCTRL_2")
        UInt8("counter_hi")
        UInt8("counter_lo")

class RadTimestampThread(TimestampThread):
    def __init__(self):
        UInt8("counter_hi")
        UInt8("counter_lo")


class ReaderThread(object):
    def __init__(self):
        UInt8()