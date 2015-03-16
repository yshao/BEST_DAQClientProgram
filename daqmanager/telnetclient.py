import telnetlib
from common.env import Env
from common.sysutils import run_command


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
      self.telnet.write('Winsocket'+self.newline)
      run_command('wintime')
      self.telnet.read_until("\>",3)


  def close(self):
    ""
    self.telnet.write("exit"+self.newline)