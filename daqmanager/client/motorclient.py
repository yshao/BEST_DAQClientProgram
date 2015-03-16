import glob
from common.env import Env
from daqmanager.client.sync import Telnet


class MotorClient():
    logger=[]
    def __init__(self):
        cfg=Env().getConfig()

        t1=Telnet(cfg['archival_ip'])
        t1.login()
        self.client=t1
        # ln=sender.getText()
        # mem=ln.splitlines()
        #
        # for l in mem:
        #     self.send(ln)
        #     logger


    def motor_send_cmd(self,cmd):
        ""

        self.client.send('serialport %s' %cmd)

    def motor_send_list(self):
        ""
        l=self.l
        for cmd in l:
            self.logger.append(cmd)
            self.motor_send_list(cmd)

        print self.logger

### sort into three files ###
# local=cfg['local_dir']
# ext='imu'
# glob.glob('%s/*.%s'%(local,ext))
#
# ext='enc'
# glob.glob('%s/*.%s'%(local,ext))
#
# ext='rad'
# glob.glob('%s/*.%s'%(local,ext))
#
#
# ### ftp ###
