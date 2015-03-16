from multiprocessing import Pool
from functools import partial
import os
from common.env import Env
from mputils import mp_reg

class FtpProcess(object):
    def __init__(self,ips):
        self.l=[]

        cfg=Env().getConfig()
        # print ips

        self.ips=ips
        self.pwd=cfg['praco_password']
        self.user=cfg['praco_username']
        self.local=cfg['local_dir']

        fdr={}
        for k in ips.keys():
            lfdr=k+'_'+ips[k].replace('.','_')
            lfdr=self.local+'/'+lfdr
            print lfdr,k
            fdr[k]=lfdr

        self.folders=fdr

    def ftpthread(self, ipk):
        ips=self.ips
        user=self.user
        pwd=self.pwd
        ### move files into folders ###



        l=[]
        ldr=self.folders[ipk]
        ip=self.ips[ipk]
        if not os.path.exists(ldr):
            os.makedirs(ldr)

        # os.mkdir(ldr)
        print "transferring from %s to %s" % (ip,ldr)
        # with ftputil.FTPHost(ip, user, pwd) as host:
        #     names = host.listdir(host.curdir)
        #     for name in names:
        #         if host.path.isfile(name):
        #             # Remote name, local name, binary mode
        #             host.download_if_newer(name, name)
        for f in ['a','b']:
            l.append(f)
        #     return len(l)
        return len(l)

    def go(self):
        pool = Pool()
        ips=self.ips

        res=pool.map(self.ftpthread, ips)
        return res

def run_ftppool(d):
    ### pickle instance
    mp_reg()
    # p=Pool()
    d.keys()

    p=FtpProcess(d)
    print p.go()

if __name__ == '__main__':
    cfg=Env().getConfig()
    d={}
    l=['archival_ip','encoder_ip','rad33_ip']
    for k,v in cfg.items():
        if k in l:
            d[k]=v

    for k,v in cfg['radiometer'].items():
        if k in l:
            d[k]=v

    run_ftppool(d)