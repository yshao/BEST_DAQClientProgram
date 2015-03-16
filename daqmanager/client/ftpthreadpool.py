# Download some files from the login directory.
import ftputil
import schedule
from common.env import Env



class FtpThreadPool():
    def __init__(self,iplist):
        ""

        cfg=Env().getConfig()
        ips=[]
        for ip in iplist:
            ips.append(cfg[ip])

        self.ips=ips
        ### scheduler ###
        self.scheduler=schedule.Scheduler()

        self.scheduler.every(cfg['update_interval']).minutes.do(self.start)

        # d={}
        # for k in cfg.keys():
        #     if k[-2:] == 'ip':
        #         name=k[:-3]
        #         d[k]={}
        #         d[k]['ip']=cfg[k]
        #         d[k]['folder']=name

        # ips

        self.pwd=cfg['praco_password']
        self.user=cfg['praco_username']
        self.local=cfg['local_dir']

    def start(self):
        ips=self.ips
        user=self.user
        pwd=user.pwd
        ### move files into folders ###
        for idx,ip in enumerate(ips):
            print "transferring from %s" % ip
            with ftputil.FTPHost(ip, user, pwd) as host:
                names = host.listdir(host.curdir)
                for name in names:
                    if host.path.isfile(name):
                        # Remote name, local name, binary mode
                        host.download(name, name)

