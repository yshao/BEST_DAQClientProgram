from best.common.netutils import *

### test motor
# rad22IP="192.168.38.38"
# t=TelnetClient(rad22IP)
# # t.send("DAQrad1")
#
# encIP="192.168.38.31"
# t2=TelnetClient(encIP)
# t2.send("DAQArchImuS1")
#
# archIP="192.168.38.46"
# t3=TelnetClient(archIP)
# # t3.send("DAQenc_new")
#
# t3.send("stop_motor")



# archIP=config.get("IP_ARCHIVAL")
# t3=telnetlib.Telnet("192.168.38.31",port=23)
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

# t1=telnetlib.Telnet("192.168.38.38",port=23)
# newline = "\n"
# print t1.read_until("login:")
# t1.write("admin"+newline)
# print t1.read_until("Password:",3)
# t1.write("BEST"+newline)
# print t1.read_until(">")
# t1.write("cd FlashDisk/Best"+newline)
# print t1.read_until("Best")


t2=telnetlib.Telnet("192.168.38.31",port=23)
newline = "\n"
print t2.read_until("login:")
t2.write("admin"+newline)
print t2.read_until("Password:",3)
t2.write("BEST"+newline)
print t2.read_until(">")
t2.write("cd FlashDisk/Best"+newline)
print t2.read_until("Best")



t3=telnetlib.Telnet("192.168.38.46",port=23)
newline = "\n"
print t3.read_until("login:")
t3.write("admin"+newline)
print t3.read_until("Password:",3)
t3.write("BEST"+newline)
print t3.read_until(">")
t3.write("cd FlashDisk/Best"+newline)
print t3.read_until("Best")


######
import time
# t2.write("stop_motor"+newline)
# print t3.read_until(">",3)
# t2.write("stop_motor"+newline)
# print t3.read_until(">",3)
# t2.write("stop_motor"+newline)
# print t3.read_until(">",3)
# time.sleep(2)
#
# t2.write("encoder_home"+newline)
# print t3.read_until(">",3)
# time.sleep(8)
#
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

# t2.write("stop_motor"+newline)
# print t3.read_until(">",3)



### DAQ
t1.write("DAQrad1"+newline)
print t1.read_until(">",3)
t2.write("DAQArchImuS1"+newline)
print t2.read_until(">",3)
t3.write("DAQenc_new"+newline)
print t3.read_until(">",3)
t1.close()
t2.close()
t3.close()

import time

# t2=telnetlib.Telnet("192.168.38.31",port=23)
# newline = "\n"
# print t2.read_until("login:")
# t2.write("admin"+newline)
# print t2.read_until("Password:",3)
# t2.write("BEST"+newline)
# print t2.read_until(">")
# t2.write("cd FlashDisk/Best"+newline)
# print t2.read_until("Best")
#
#
