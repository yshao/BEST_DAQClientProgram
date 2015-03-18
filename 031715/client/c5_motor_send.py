from best.common.socketclient import SocketClient

class DAQ(object):
    ""
    COMMANDS={}
    SW={}

config=Config("../config.xml")

class Motor(object):
    ""
    COMMANDS={"set_dir":"AC=",
    "run":"XQ##",
    "stop":"KL",
    "set_speed":"VX=",
    "load_bin":"LD",

    "motor_ctrl":"MO="}


    SW={"on":"1","off":"0"

    }

    def __init__(self):
        ""
        self.sc=SocketClient(config.get("IP_ARCHIVAL"))

    def build(self,cmd,sw):
        ""
        str=self.__getattribute__(COMMANDS)[cmd]
        str+self.__getattribute__(SW)[sw]
        print str

    def load_bin(self):
        ""

    def send(self,args):
        ""
        sSend=self.build(args)
        self.sc.send(sSend)




import unittest
class TestMotor(unittest.case):
    def __init__(self):
        ""
        self.motor=Motor()


    def test_build(self):
        assert self.motor.build("set_speed","20000") == "VX=20000"

        assert self.motor.build("motor_ctrl","on") == "MO=1"

TestMotor.test_build()