##############
# 0. clear previous data
# 1. home motor
# 2. starts motor
# 3. starts DAQ
# 4. sync time


import os
import telnetlib
import time
from common.datasetman import DatasetMan
from common.env import Env
from common.utils import get_timestamp
from daqmanager.client.ftpfunc import upload_time, touch
import shutil

cfg=Env().getConfig()

### clear data folder ###
dataman=DatasetMan()
dataman.clear_buffer()

print cfg['radiometer']['rad22_ip']

dataman.clear_praco(cfg['archival_ip'])
dataman.clear_praco(cfg['encoder_ip'])
dataman.clear_praco(cfg['radiometer']['rad22_ip'])

t1=telnetlib.Telnet(cfg['radiometer']['rad22_ip'],port=23)
newline = "\n"
print t1.read_until("login:")
t1.write("admin"+newline)
print t1.read_until("Password:",3)
t1.write("BEST"+newline)
print t1.read_until(">")
t1.write("cd FlashDisk/Best"+newline)
print t1.read_until("Best")


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


### start DAQ program ###
t1.write("DAQrad1"+newline)
print t1.read_until(">",3)
t2.write("DAQArchImuS1"+newline)
print t2.read_until(">",3)
t3.write("DAQenc_new"+newline)
print t3.read_until(">",3)

tm=get_timestamp()
tm=tm.replace('-','_')+'.time'
touch(tm)
upload_time(cfg['archival_ip'],tm)
upload_time(cfg['encoder_ip'],tm)
upload_time(cfg['radiometer']['rad22_ip'],tm)
time.sleep(3)
os.remove(tm)