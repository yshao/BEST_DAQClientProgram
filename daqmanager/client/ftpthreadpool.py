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
    def __init__(self,ips):
        ""

        cfg=Env().getConfig()
        # ips=[]
        # for ip in iplist:
        #     ips.append(cfg[ip])

        self.ips=ips

        self.pwd=cfg['praco_password']
        self.user=cfg['praco_username']
        self.local=cfg['local_dir']

    def ftpthread(self,ipk):
        ips=self.ips
        user=self.user
        pwd=user.pwd
        ### move files into folders ###
        fdr=ipk+'_'+ips[ipk].replace('.','_')
        print "transferring from %s" % ipk
        with ftputil.FTPHost(ips[ipk], user, pwd) as host:
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
        ips=self.ipsd


        for k in ips.keys():
            # print "transferring from %s %s" % (k,ips[k])
            # pool.apply_async(foo_pool, args = (i, ), callback = log_result)
            # ftpthread=FtpThread()
            pool.apply_async(self.ftpthread,args=(k,),callback=self.log_result)
        pool.close()
        pool.join()
        print(self.result_list)


if __name__ == '__main__':
    cfg=Env().getConfig()
    d={}
    l=['archival_ip','encoder_ip','rad33_ip']
    for k,v in cfg.items():
        if k in l:
            d[k]=v

    ips=d
    ftppool=FtpThreadPool(ips)
    ftppool.start()