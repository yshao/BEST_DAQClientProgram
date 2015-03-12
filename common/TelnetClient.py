from best.common.netutils import *

### test scan network ###
config=Config("config.xml")
# scan_network()


### test all colibri connection
# rad22IP=config.get("IP_RADIOMETER_22-30")
# t=TelnetClient(rad22IP)
# newline = "\n"
# print t.read_until("login:")
# t.write("admin"+newline)
# print t.read_until("Password:")
# t.write("BEST"+newline)
# print t.read_until(">")
# t.write("cd FlashDisk/Best"+newline)
# print t.read_until("Best",3)
# t.write("DAQrad1"+newline)
# print t.read_until(">",3)
# t.close()
#
# encIP=config.get("IP_ENCODER")
# t2=TelnetClient(encIP)
# newline = "\n"
# print t2.read_until("login:")
# t2.write("admin"+newline)
# print t2.read_until("Password:")
# t2.write("BEST"+newline)
# print t2.read_until(">")
# t2.write("cd FlashDisk/Best"+newline)
# print t2.read_until("Best",3)
# t2.write("DAQenc_new"+newline)
# print t2.read_until(">",3)
# t2.close()
#
# archIP=config.get("IP_ARCHIVAL")
# t3=TelnetClient(archIP)
# newline = "\n"
# print t3.read_until("login:")
# t3.write("admin"+newline)
# print t3.read_until("Password:",3)
# t3.write("BEST"+newline)
# print t3.read_until(">")
# t3.write("cd FlashDisk/Best"+newline)
# print t3.read_until("Best")
# t3.write("DAQArchImuS1"+newline)
# print t3.read_until(">",3)
# t3.close()
#
# ### test ftp sync basic ###
# # from best.common.utils.configutil import *
# from best.daqmanager.ftp_mirror import *
# config=Config("../config.xml")
# login="admin"
# passwd="BEST"
# localdir="c:/Demo/ftptest"
# remotedir="/FlashDisk/Data"
# ip=(rad22IP,21)
# ftp_mirror(ip,login,passwd,localdir,remotedir)
#
# ip=(encIP,21)
# ftp_mirror(ip,login,passwd,localdir,remotedir)
#
# ip=(archIP,21)
# ftp_mirror(ip,login,passwd,localdir,remotedir)
#
# ### test time injection ###
# # import socket
# #
# # t1=TelnetClient("192.168.38.39")
# # t1.sendwait("time")
# #
# # s1=socket()
# # s1.send()
# #
# # t1.close()
# #
# # tE=TelnetClient("192.168.38.34")
# # tR=TelnetClient("192.168.38.38")
# # tA=TelnetClient("192.168.38.39")
# #
# # tE.send("pollTime")
# # tR.send("pollTime")
# # tA.send("serveTime")
#
# ### decode ###


rad22IP="192.168.38.31"
t=TelnetClient(rad22IP)
t.send("DAQrad1")

encIP="192.168.38.31"
t2=TelnetClient(encIP)
t2.send("DAQenc_new")

archIP="192.168.38.46"
t3=TelnetClient(archIP)
t3.send("DAQArchImuS1")

### test ftp sync basic ###
# from best.common.utils.configutil import *
from best.daqmanager.ftp_mirror import *
config=Config("../config.xml")
login="admin"
passwd="BEST"
localdir="c:/Demo/ftptest"
remotedir="/FlashDisk/Data"
ip=(rad22IP,21)
ftp_mirror(ip,login,passwd,localdir,remotedir)

ip=(encIP,21)
ftp_mirror(ip,login,passwd,localdir,remotedir)

ip=(archIP,21)
ftp_mirror(ip,login,passwd,localdir,remotedir)

### test time injection ###
# import socket
#
# t1=TelnetClient("192.168.38.39")
# t1.sendwait("time")
#
# s1=socket()
# s1.send()
#
# t1.close()
#
# tE=TelnetClient("192.168.38.34")
# tR=TelnetClient("192.168.38.38")
# tA=TelnetClient("192.168.38.39")
#
# tE.send("pollTime")
# tR.send("pollTime")
# tA.send("serveTime")

### decode ###

