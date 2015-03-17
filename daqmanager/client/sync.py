import telnetlib
from common.env import Env
from daqmanager.telnetclient import TelnetClient


class Telnet():
    ""

def sync():
    cfg=Env().getConfig()
        # parser = IniParser()
        # parser.read('test.ini')
        # print parser.as_dict()
    # telnet=Telnet()
    # telnet.login()
    # # telnet.
    #
    # t2=telnetlib.Telnet("192.168.38.31",port=23)
    # newline = "\n"
    # print t2.read_until("login:")
    # t2.write("admin"+newline)
    # print t2.read_until("Password:",3)
    # t2.write("BEST"+newline)
    # print t2.read_until(">")
    # t2.write("cd FlashDisk/Best"+newline)
    # print t2.read_until("Best")

    t1=TelnetClient('archival',cfg['archival_ip'])
    res=t1.sync_time()
    print res

    t2=TelnetClient('encoder',cfg['encoder_ip'])
    res=t2.sync_time()
    print res

    # for k in cfg['radiometer'].keys():
    #     ip=cfg['radiometer'][k]
    #     t3=TelnetClient(ip)
    #     res=t3.sync_time()
    #     print res

if __name__ == '__main__':
    sync()