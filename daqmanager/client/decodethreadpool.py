import glob
import os

__company__ = 'Boulder Environmental Sciences and Technology'
__project__ = ''
__author__ = 'Y. Shao'
__created__ = '3/16/2015' '12:18 PM'

import multiprocessing as mp
import time
from common.env import Env

        ### scheduler ###
        # self.scheduler=schedule.Scheduler()
        # self.scheduler.every(cfg['update_interval']).minutes.do(self.start)


def decode_enc(f):
    print f

def decode_imu(f):
    print f

def decode_rad(f):
    print f


class DecodeThreadPool():
    def __init__(self,ips):
        ""

        cfg=Env().getConfig()
        self.local=cfg['local_dir']
        # self.folders=glob.glob('%s/**/' % cfg['local_dir'])
        fdr=[]
        for k in ips.keys():
            lfdr=k+'_'+ips[k].replace('.','_')
            lfdr=self.local+'/'+fdr
            fdr.append(lfdr)

        self.folders=fdr

        print 'found ' + self.folders

    def decodethread(self,folder):
        # ips=self.ips
        # ips=self.ips
        # user=self.user
        # pwd=user.pwd
        ### move files into folders ###

        print "decoding from %s" % folder
        for f in glob.glob(folder+'/**'):
            filen=os.path.basename(f)
            ftype=filen[:3]
            if ftype == 'enc':
                decode_enc(f)
            elif ftype == 'arc':
                decode_imu(f)
            elif ftype == 'rad':
                decode_rad(f)

        # with ftputil.FTPHost(ip, user, pwd) as host:
        #     names = host.listdir(host.curdir)
        #     for name in names:
        #         if host.path.isfile(name):
        #             # Remote name, local name, binary mode
        #             host.download(name, name)
        #
        #     l=[]
        #     return len(l)

    result_list = []
    def log_result(self,result):
        # This is called whenever foo_pool(i) returns a result.
        # result_list is modified only by the main process, not the pool workers.
        print "files decoded %s" % result
        self.result_list.append(result)

    def start(self):
        pool = mp.Pool()
        folders=self.folders
        for fdr in folders:
            print "decoding %s" % fdr
            pool.apply_async(self.decodethread,args=(fdr,),callback=self.log_result)

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
    pool=DecodeThreadPool(ips)
    pool.start()