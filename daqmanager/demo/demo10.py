#########################
# home motor
#


import os
import telnetlib
import time
from common.env import Env
from common.utils import get_timestamp
from daqmanager.client.ftpfunc import upload_time, ftp_delete, touch
import shutil

cfg=Env().getConfig()

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

t2.write("stop_motor"+newline)
print t2.read_until(">",5)
t2.write("stop_motor"+newline)
print t2.read_until(">",5)

t2.write("encoder_home"+newline)
print t2.read_until(">",5)
