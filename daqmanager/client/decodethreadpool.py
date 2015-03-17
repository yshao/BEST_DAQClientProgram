import glob

__company__ = 'Boulder Environmental Sciences and Technology'
__project__ = ''
__author__ = 'Y. Shao'
__created__ = '3/16/2015' '2:45 PM'

from multiprocessing import Pool
from functools import partial
import os
from common.env import Env
from mputils import mp_reg

def decode_enc(f):
    print 'decode %s' % f
    num_r='1000'
    l='records %s' % num_r
    return l

def decode_imu(f):
    print 'decode %s' % f
    num_r='1003'
    l='records %s' % num_r
    return l

def decode_rad(f):
    print 'decode %s' % f
    num_r='1001'
    l='records %s' % num_r
    return l

class DecodeProcess(object):
    def __init__(self,ips,fdr):
        self.l=[]

        cfg=Env().getConfig()
        # print ips

        self.ips=ips
        self.pwd=cfg['praco_password']
        self.user=cfg['praco_username']
        self.local='%s/%s' %(cfg['local_dir'],fdr)

        fdr={}
        for k in ips.keys():
            lfdr=k+'_'+ips[k].replace('.','_')
            lfdr=self.local+'/'+lfdr
            print lfdr,k
            fdr[k]=lfdr

        self.folders=fdr
        print self.local

    def decodethread(self, ipk):
        ips=self.ips
        user=self.user
        pwd=self.pwd
        ### move files into folders ###



        total_res=[]
        ldr=self.folders[ipk]
        ip=self.ips[ipk]
        if not os.path.exists(ldr):
            os.makedirs(ldr)

        print "decoding from %s" % ldr
        # print glob.glob(ldr+'/*')
        res=[]
        for f in glob.glob(ldr+'/**'):
            filen=os.path.basename(f)
            ftype=filen[-3:]
            if ftype == 'enc':
                res=decode_enc(f)
            elif ftype == 'imu':
                res=decode_imu(f)
            elif ftype == 'rad':
                res=decode_rad(f)

        print res
        total_res=total_res+[res]
        # print res
        # return len(l)
        return total_res

    def go(self):
        pool = Pool()
        ips=self.ips

        res=pool.map(self.decodethread, ips)
        return res

def run_decodepool(d,rel_p):
    ### pickle instance
    mp_reg()
    # p=Pool()
    d.keys()

    p=DecodeProcess(d,rel_p)
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

    run_decodepool(d,'1426610475')