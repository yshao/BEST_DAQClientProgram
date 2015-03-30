from daqmanager.client.clientutils import check_network
import sys
import telnetlib
import time
from common.env import Env

__company__ = 'Boulder Environmental Sciences and Technology'
__project__ = ''
__author__ = 'Y. Shao'
__created__ = '3/16/2015' '10:43 AM'

### check network ###
if not check_network():
    sys.exit(0)

### telnet login ###
cfg=Env().getConfig()
t1=telnetlib.Telnet(cfg['radiometer']['rad33_ip'],port=23)
newline = "\n"
print t1.read_until("login:")
t1.write("admin"+newline)
print t1.read_until("Password:",3)
t1.write("BEST"+newline)
print t1.read_until(">")
t1.write("cd FlashDisk/Best"+newline)
print t1.read_until("Best")


t2=telnetlib.Telnet(cfg['archival'],port=23)
newline = "\n"
print t2.read_until("login:")
t2.write("admin"+newline)
print t2.read_until("Password:",3)
t2.write("BEST"+newline)
print t2.read_until(">")
t2.write("cd FlashDisk/Best"+newline)
print t2.read_until("Best")



t3=telnetlib.Telnet(cfg['encoder'],port=23)
newline = "\n"
print t3.read_until("login:")
t3.write("admin"+newline)
print t3.read_until("Password:",3)
t3.write("BEST"+newline)
print t3.read_until(">")
t3.write("cd FlashDisk/Best"+newline)
print t3.read_until("Best")


### actuate ###
t2.write("stop_motor"+newline)
print t2.read_until(">",3)
t2.write("stop_motor"+newline)
print t2.read_until(">",3)
# t2.write("stop_motor"+newline)
# print t2.read_until(">",3)
time.sleep(2)

t2.write("encoder_home"+newline)
print t2.read_until(">",3)
time.sleep(10)


t2.write("stop_motor"+newline)
print t2.read_until(">",3)
t2.write("stop_motor"+newline)
print t2.read_until(">",3)
# t2.write("stop_motor"+newline)
# print t3.read_until(">",3)
time.sleep(2)

t2.write("encoder_reverse"+newline)
print t2.read_until(">",3)
time.sleep(20)

t2.write("stop_motor"+newline)
print t2.read_until(">",3)
t2.write("stop_motor"+newline)
print t2.read_until(">",3)
# t2.write("stop_motor"+newline)
# print t3.read_until(">",3)
time.sleep(2)

t2.write("encoder_forward"+newline)
print t2.read_until(">",3)

time.sleep(20)
### ftp ### thread

pool=FtpThreadPool()
pool.start()
