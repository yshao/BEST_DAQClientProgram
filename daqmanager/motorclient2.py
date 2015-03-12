from telnetclient import TelnetClient
import math

class MotorClient(object):
  # A - 22-30 Rad
  # B -
  # C -
  # D -

  COUNTS_PER_ROTATION=32768
  MODE= {"SPEED":1,"POSITION":2}
  PROFILE={"ABCD":1,"ABC":2,"AB":3,"A":4,
           "ACD":2,"AC":3,"A":4,
           "AD":4,

           "BCD":5,"BC":6,"B":1,
           "BD":2,

           "CD":3, "C":3,
           "D":4
           }

  STAT = {"STATUS":1,"ERROR":2}
  DIR = {"FORWARD":1,"REVERSE":-1}

  def __init__(self,mode,host_url,us):
      ""
      cfg=Env().getConfig()
      self.telnet=TelnetClient(cfg['archival_ip'],cfg['praco_username'],cfg['praco_password'])
      self.newline=self.telnet.newline

      mode = self.MODE.get(mode)
      self.sendwait(""%mode)


  def exec_cmd(self,cmd):
      "provides business logic to cmd"



  def sendwait(self,cmd):
      self.telnet.send(cmd+self.newline)
      if (self.telnet.read_until(";")):
        return True
      else:
        return False

  def send(self,cmd):
      self.telnet.send(cmd)

      return self.telnet.read_all()

  def exec_program(self,num):
      ""
      if (self.telnet.send("XQ##PROG%s" % num)):
          ""

  def download_binary(self,file):
    ""
    loc=self.telnet.send("LP[3]")

    length=self.telnet.send("LP[4]")

    ### verify image will fit

    if (self.telnet.send("CP")):
        ""

    if (self.telnet.send("LD[1]=loc")):
        ""

    if (self.telnet.send("LD[1]=loc")):
        ""

    if (self.telnet.send("LD[1]=(loc+%s)")):
        ""

    ### verify checksum

    if (self.telnet.send("CC=checksum")):
        ""

  def set_speed(self,val):
      speed_counts = math.floor(val * self.COUNTS_PER_ROTATION)
      acc = val

      self.telnet.sendwait("AC=%s"%acc)
      self.telnet.sendwait("JV=%s"%speed_counts)
      
  def get_speed(self):
      self.set_dir()
      return self.telnet.send("JV")

  def set_dir(self,dir):
      ""

      # val = AC*DIR.get(dir)
      # if (self.telnet.send("AC=%s"%val):
      #     ""
      #
      #
      # if (self.telnet.send("AC"=)):
      #     ""


  def set_pos(self,val):
      self.telnet.sendwait("PX=%s"%val)


  def get_pos(self,val):
      return self.telnet.send("PA")



  def load_script(self,script):

    num_lines=len(script)
    n=0
    for line in script:
        self.telnet.send(line+self.newline)
        self.telnet.read_until(";")
        n=n+1

    if n == num_lines:
        self.load_correct=True

  def get(self,key):
      return self.STAT[key]



  def load_profile(self,profile):
    path=self.PROFILE.get(profile)
    self.telnet.send("LD %s" % profile)



# import unittest
# import common.configutils
#
# # config=Config("config.xml")
#
# class MotorClientTest(unittest):
#     setup_done = False
#
#     def setUp(self):
#         ""
#         # self.motor=MotorClient(config)
#
#
#     def test_get(self):
#         ""
#
#
#     def test_load_script(self):
#         script="MO=1\n" \
#                "AC=14000\n" \
#                "JV=15000\n" \
#                "BG\n"
#
#         ### mock call
#         self.motor.load_script(script)
#
#
#         assert self.expect("MO=1\n")
#         assert self.expect("AC=14000\n")
#         assert self.expect("JV=15000\n")
#         assert self.expect("BG\n")
#
#     def test_set_speed(self):
#         ""
#         self.motor.set_speed(15000)
#
#         assert 15000 == self.motor.get_speed()
#
#
#     def test_download_binary(self):
#         ""
#
#         file="testmotordownload.bin"
#         self.motor.download_binary(file)
#
#         # expect("")
#
#     def test_download_binary_exception(self):
#         ""
#         file="testmotordownload.bin"
#         self.motor.download_binary(file)
#
#         self.catch_exception("Not found testmotordownload.bin")
#
#
# class I2CMaster(object):
#     ""
#     def __init__(self):
#         ""
#
# class SensorClient(object):
#     SENSOR={"P_SENSOR1":31,"P_SENSOR2":21,"P_SENSOR3":31,
#             "P_SENSOR4":31,"P_SENSOR5":21,"P_SENSOR6":21,
#             "H_SENSOR1":31,"H_SENSOR2":21,"H_SENSOR3":31,
#             "H_SENSOR1":31,"H_SENSOR2":21,"H_SENSOR3":31,
#             "T_SENSOR1":11
#             }
#
#     READ={
#
#     }
#
#     READINIT={
#
#
#     }
#
#     INIT={
#
#     }
#
#     def __init__(self):
#        ""
#        self.i2c=I2CMaster()
#
#
#     def reading_bytes(self,addr,n_bytes):
#         ""
#         bytes=self.i2c.send(self.READ[addr])
#         return bytes
#
#
#     def writing_bytes(self,sensor,bytes):
#         ""
#         addr=self.SENSOR[sensor]
#         cmd=self.READ[sensor]
#         bytes=self.i2c.write(addr,cmd,bytes)
#         return bytes
#
#     def read_config(self,sensor):
#         ""
#         addr=self.SENSOR[sensor]
#         cmd=self.READINIT[sensor]
#         bytes=self.i2c.send(cmd)
#         return bytes
#
#     def read_data(self,sensor):
#         ""
#         addr=self.SENSOR[sensor]
#         cmd=self.READ[sensor]
#         bytes=self.i2c.send(cmd)
#
#     def init(self,sensor):
#         ""
#         addr=self.SENSOR[sensor]
#         cmd=self.INIT[sensor]
#         bytes=self.i2c.send(cmd)
#
#
# class SPIMaster(object):
#     def __init__(self):
#         ""
#
#     def send(self):
#         ""
#
#
# class SPITest(unittest.TestCase):
#     def setUp(self):
#         ""
#         self.spi=SPIMaster()
#
#     def test_send(self):
#         ""
#         self.spi.send()


