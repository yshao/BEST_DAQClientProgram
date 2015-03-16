# Download some files from the login directory.
import ftputil
import schedule
import multiprocessing as mp
import time
from common.env import Env

        ### scheduler ###
        # self.scheduler=schedule.Scheduler()
        # self.scheduler.every(cfg['update_interval']).minutes.do(self.start)


class FtpThreadPool():
    def __init__(self,iplist):
        ""

        cfg=Env().getConfig()
        ips=[]
        for ip in iplist:
            ips.append(cfg[ip])

        self.ips=ips

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

    def ftpthread(self,ip):
        ips=self.ips
        user=self.user
        pwd=user.pwd
        ### move files into folders ###
        # for idx,ip in enumerate(ips):
        print "transferring from %s" % ip
        with ftputil.FTPHost(ip, user, pwd) as host:
            names = host.listdir(host.curdir)
            for name in names:
                if host.path.isfile(name):
                    # Remote name, local name, binary mode
                    host.download(name, name)

            l=[]
            return len(l)

    result_list = []
    def log_result(self,result):
        # This is called whenever foo_pool(i) returns a result.
        # result_list is modified only by the main process, not the pool workers.
        print "files transferred %s" % result
        self.result_list.append(result)

    def start(self):
        pool = mp.Pool()
        ips=self.ips
        for ip in ips:
            print "transferring from %s" % ip
            # pool.apply_async(foo_pool, args = (i, ), callback = log_result)
            # ftpthread=FtpThread()
            pool.apply_async(self.ftpthread,args=(ip,),callback=self.log_result)
        pool.close()
        pool.join()
        print(self.result_list)


if __name__ == '__main__':
    cfg=Env().getConfig()

    ips=[cfg['archival_ip'],['encoder_ip']]
    ftppool=FtpThreadPool(ips)