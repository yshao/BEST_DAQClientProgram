import telnetlib
from common.env import Env
from common.sysutils import run_command
from daqmanager.client.utils import p_mname, tm_to_epoch


class TelnetClient(object):
  newline = "\n"
  def __init__(self,host_ip):
    # newline="\n"
    ""
    cfg=Env().getConfig()
    user=cfg['praco_username']
    pwd=cfg['praco_password']
    host_url=cfg[host_ip]

    try:
        self.telnet=telnetlib.Telnet(host_url,port=23)
        self.telnet.read_until("login: ")
        self.telnet.write(user+self.newline)
        self.telnet.read_until("Password: ")
        self.telnet.write(pwd+self.newline)
        self.telnet.read_until(">")
        self.telnet.write("cd FlashDisk/Best"+self.newline)
        self.telnet.read_until("Best")
    except Exception, e:
        print e,"Failed in login"


  def send(self,command):
    ""
    self.telnet.write(command+self.newline)
    return self.telnet.read_until("\>",3)

  def sync_time(self):
      self.telnet.write('DAQclk_test'+self.newline)
      run_command('WinsockClient')
      try:
        self.telnet.read_until("\>",3)
        return True
      except Exception,e:
        print '%s' % e,p_mname()
        # pass
        return False

  def sync_mock(self):
      tm=tm_to_epoch()
      fh=open(tm,'wb')


  def run_daq(self):
      ""


  def close(self):
    ""
    self.telnet.write("exit"+self.newline)