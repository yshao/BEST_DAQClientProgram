__author__ = 'Ping'

ROUTER_IP='192.168.1.210'


import subprocess
import time
import re
import math

import subprocess as sub
import threading

class TimedThread(threading.Thread):
    def __init__(self, cmd, timeout):
        threading.Thread.__init__(self)
        self.cmd = cmd
        self.timeout = timeout

    def run(self):
        self.p = sub.Popen(self.cmd)
        self.p.wait()

    def Run(self):
        self.start()
        self.join(self.timeout)

        if self.is_alive():
            self.p.terminate()      #use self.p.kill() if process needs a kill -9
            self.join()



def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def main():
    while(True):
        time.sleep(1)
        msg=timeout_command(['ping',ROUTER_IP,'-c','1'],2)
        # print msg
        try:
            num=parse_command(msg)
            print "time=",num,"ms"

            if is_number(num):
                if math.ceil(float(num)) > 20:
                    print "[INFO","recover from high ping"
                    call_command(['ifconfig','eth0','down'])
                    call_command(['ifconfig','eth0','up'])
            else:
                raise "Unparseable result"
        except:
            print "[INFO","recover from unknown"
            call_command(['ifconfig','eth0','down'])
            call_command(['ifconfig','eth0','up'])
            msg,err=call_command(['ls','-l'])
            print msg




def call_command(list):
    subproc = subprocess.Popen(list, stdout=subprocess.PIPE)
    return subproc.communicate()

def timeout_command(command, timeout):
    """call shell-command and either return its output or kill it
    if it doesn't normally exit within timeout seconds and return None"""
    import subprocess, datetime, os, time, signal
    start = datetime.datetime.now()
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    while process.poll() is None:
      time.sleep(0.1)
      now = datetime.datetime.now()
      if (now - start).seconds> timeout:
        os.kill(process.pid, signal.SIGKILL)
        os.waitpid(-1, os.WNOHANG)
        return None
    return process.stdout.read()


def parse_command(msg):
    p = re.compile(r'time=.*')
    return (p.findall(msg)[0]).replace('time=','').replace('<','').replace('ms','')



main()