import glob
import os
import shutil
import time
from common.env import Env
from common.utils import get_timestamp
from daqmanager.client.ftpfunc import ftp_list, ftp_download, ftp_delete, touch, ftp_upload


class Dataset():
    def __init__(self,fp):
        self.path=fp
        self.basetm=os.path.basename(fp)

        ### builds dataset attributes ###
        self.scan_files()
        # self.make_stats()

        # self.make_fullfile()
        # self.decode()

        # self.sync_db()

        # self.write_log()

    def make_stats(self):
        ""

        ### file tm ###
        self.basetm=os.path.splitext(os.path.basename())[0]

        d={}
        self.filestats=d
        ### decode ###

        ### time sync ###

    def decode(self):
        ""
        lBuffers=[]

        self.bufferp=lBuffers

    def log(fliep,a):
      with open(fliep) as fh:
        for l in a:
          fh.write(l)

    def read_stats(self):
        ""

    def scan_files(self):
        ""
        base=self.path
        return glob.glob('%s/data/**' %base)

    def make_fullfile(self):
      tm=self.tm
      fullfilep='%s' % tm

      lStats=[]
      lFiles=self.scan_files()
      for f in lFiles:
        lStats.append(self.read_stats(f))
        file(fullfilep,'wb').write(file(f,'rb').read())

      self.filetm=lStats
      # self.log(lStats)

    def write_log(self):
        ""
        logname=self.basetm+'.log'
        with open(logname,'wb') as fh:
            fh.write(self.files)
            fh.write(self.filem)
            fh.write(self.bufferp)
            fh.write(self.res)

class DatasetMan():
    def __init__(self):
        ""
        self.local=Env().getConfig()['local_dir']

        for dset in self.getSets():
            d=Dataset(dset)
            print d.basetm

    def getSets(self):
        sets=glob.glob('%s/**/'% local_dir)
        if  sets == []:
            os.mkdir('%s/%s' % (cfg['local_dir'],'buffer'))
        if 'buffer' in sets: sets.remove('buffer')
        # sets.re
        return sets

    def clear_buffer(self):
        try:
            local=self.local
            shutil.rmtree('%s/data' % local)
        except:
            pass

    def poll_praco(self):
        ""
        #TODO: ipnetwork
        fa=ftp_list(cfg['archival_ip'],cfg['praco_username'],cfg['praco_password'])
        fe=ftp_list(cfg['encoder_ip'],cfg['praco_username'],cfg['praco_password'])
        d={}
        d['archival']=fa
        d['encoder']=fe
        print fa
        print fe
        return d

    def download(self):
        temp=self.temp
        try:
            os.mkdir(temp)
        except:
            pass
        try:
            ftp_download(cfg['archival_ip'],cfg['praco_username'],cfg['praco_password'],temp)
        except:
            pass
        try:
            ftp_download(cfg['encoder_ip'],cfg['praco_username'],cfg['praco_password'],temp)
        except:
            pass

    def clear_praco(self):
        ""

        ftp_delete(cfg['encoder_ip'],cfg['praco_username'],cfg['praco_password'])
        ftp_delete(cfg['archival_ip'],cfg['praco_username'],cfg['praco_password'])

    def init(self):
        ""
        # self.temp=
        local=self.local
        temp='%s/data' % local
        self.temp=temp

    def sync(self):
        ""
        tm=get_timestamp()
        tm=tm.replace('-','_')
        touch(tm)
        # upload_time(cfg['archival_ip'],tm)
        try:
            ftp_upload(cfg['archival_ip'],cfg['praco_username'],cfg['praco_password'],tm)
        except:
            pass

        try:
            ftp_upload(cfg['encoder_ip'],cfg['praco_username'],cfg['praco_password'],tm)
        except:
            pass

        # upload_time(cfg['encoder_ip'],tm)
        time.sleep(5)
        os.move(tm,temp)


if __name__ == '__main__':
    cfg=Env().getConfig()
    local_dir=cfg['local_dir']
    dm=DatasetMan()
    # print dm.getSets()
    # try:
        # globals()
    dset=Dataset('c:/datasets/')
    print dset.scan_files()
    # except:




    inuFileGroup=glob.glob()