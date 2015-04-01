import telnetlib
import time
from common.env import Env
newline = "\n"
cfg=Env().getConfig()
FORWARD='prog2'+newline
REVERSE='prog4'+newline
STOP='stop'+newline
HOME='prog1'+newline
TEST='prog3'+newline
TEST_REV='prog5'+newline


t2=telnetlib.Telnet(cfg['archival_ip'],port=23)

print t2.read_until("login:")
t2.write("admin"+newline)
print t2.read_until("Password:",3)
t2.write("BEST"+newline)
print t2.read_until(">")
t2.write("cd FlashDisk/Best"+newline)
print t2.read_until("Best")


### home motor ###
t2.write(STOP)
print t2.read_until(">",5)
t2.write(STOP)
print t2.read_until(">",5)

t2.write(HOME)
print t2.read_until(">",5)
time.sleep(15)

t2.write(STOP)
print t2.read_until(">",5)
t2.write(STOP)
print t2.read_until(">",5)