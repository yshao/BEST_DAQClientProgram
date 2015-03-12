UPDATESW=0xB5
import math
import telnetlib
from best.common.configutils import *

class TelnetClient(object):
  newline = "\n"
  def __init__(self,host_url,username="admin",password="BEST"):
    newline="\n"
    ""
    try:
        self.telnet=telnetlib.Telnet(host_url,port=23)
        self.telnet.read_until("login: ")
        self.telnet.write(username+self.newline)
        self.telnet.read_until("Password: ")
        self.telnet.write(password+self.newline)
        self.telnet.read_until(">")
        self.telnet.write("cd FlashDisk/Best"+self.newline)
        self.telnet.read_until("Best")
    except Exception, e:
        print e
        #TODO


  def send(self,command):
    ""
    self.telnet.write(command+self.newline)
    return self.telnet.read_until("\>",3)

  def close(self):
    ""
    self.telnet.write("exit"+self.newline)




COMMAND={"HOME":"mohome",
         "FORWARD":"moforward",
         "REVERSE":"moreverse",
         "SLOW":"moslow",
         "DAQENC":"DAQenc_new",
         "DAQRAD":"DAQrad1",
         "DAQENCSTOP":"stopdata",
         "DAQRADSTOP":"stopdata",
         "CLEARDIR":"del *.*"
        }


from best.common.sysutils import *

def scan_network(list):
    ""
    def parser_scan(out):
        result = {}
        for row in out.split('\n'):
            ### regexp parsering
            if row.startswith("Reply from"):
                result=True

        return result

    for k,v in list.iteritems():
        command=Command("ping -n 1 %s" % v,parser_scan)
        result,out,err=command.run(timeout=5)

        list[k]=result

    # print list
    return list

# if __name__ == '__main__':
#     d={}
#     d['IP']='localhost'
#     d['G']='localhost'
#     d['J']='192.168.38.11'
#     scan_network(d)

### test scan_network
# d={}
# d['IP']='localhost'
# d['G']='localhost'
# d['J']='192.168.38.11'
#
# assert scan_network(d) == {"IP":True,"G":True,"J":False}


### test a remote site ###
# t=telnetlib.Telnet("www.telehack.com",23)
# newline = "\n"
# t.write("help"+newline)
# print t.read_until(".")
#
# t.write("help"+newline)
# print t.read_until("zc")


# 192.168.38.31 - archival
# 192.168.38.46 - encoder

# t = TelnetClient()