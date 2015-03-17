from daqmanager.client.clientutils import check_network
import sys
import telnetlib
import time
from common.env import Env
from daqmanager.client.ftpfunc import ftp_list,ftp_delete

# hostIP="192.168.38.4"
# rad22IP="192.168.38.38"
# encIP="192.168.38.31"
# archIP="192.168.38.46"

# def check_network():
#     ""
#     run_command('ping %s' % rad22IP)
#     run_command('ping %s' % encIP)
#     run_command('ping %s' % archIP)

### check network ###
# if not check_network():
#     sys.exit(0)
cfg=Env().getConfig()

### clean previous data ###
l=ftp_list(cfg['archival_ip'],cfg['praco_username'],cfg['praco_password'])
if len(l) > 0:
    ftp_delete(cfg['archival_ip'],cfg['praco_username'],cfg['praco_password'])
l=ftp_list(cfg['encoder_ip'],cfg['praco_username'],cfg['praco_password'])
if len(l) > 0:
    ftp_delete(cfg['encoder_ip'],cfg['praco_username'],cfg['praco_password'])

### telnet login ###
cfg=Env().getConfig()

# t1=telnetlib.Telnet("192.168.38.38",port=23)
# newline = "\n"
# print t1.read_until("login:")
# t1.write("admin"+newline)
# print t1.read_until("Password:",3)
# t1.write("BEST"+newline)
# print t1.read_until(">")
# t1.write("cd FlashDisk/Best"+newline)
# print t1.read_until("Best")
#
# t2=Telnet()
t2=telnetlib.Telnet(cfg['archival_ip'],port=23)
newline = "\n"
print t2.read_until("login:")
t2.write("admin"+newline)
print t2.read_until("Password:",3)
t2.write("BEST"+newline)
print t2.read_until(">")
t2.write("cd FlashDisk/Best"+newline)
print t2.read_until("Best")



t3=telnetlib.Telnet(cfg['encoder_ip'],port=23)
newline = "\n"
print t3.read_until("login:")
t3.write("admin"+newline)
print t3.read_until("Password:",3)
t3.write("BEST"+newline)
print t3.read_until(">")
t3.write("cd FlashDisk/Best"+newline)
print t3.read_until("Best")


######

### DAQ
# t1.write("DAQrad1"+newline)
# print t1.read_until(">",3)
print cfg['archival_ip'],'arch'
print cfg['encoder_ip'],'enc'
print 'login'
t2.write("DAQArchImuS1"+newline)
print t2.read_until(">",3)
t3.write("DAQenc_new"+newline)
print t3.read_until(">",3)
# t1.close()
t2.close()
t3.close()
