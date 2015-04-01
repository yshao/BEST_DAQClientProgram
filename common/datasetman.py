import glob
import os
import shutil
import time
from common.utils import get_timestamp
from common.env import Env
from daqmanager.client.ftpfunc import ftp_list, ftp_delete, ftp_download, ftp_upload, touch
from daqmanager.client.utils import tm_to_epoch
from daqmanager.decoder.dataset import Dataset

__company__ = 'Boulder Environmental Sciences and Technology'
__project__ = ''
__author__ = 'Y. Shao'
__created__ = '3/30/2015' '12:53 PM'

class DatasetMan():
    def __init__(self):
        ""
        cfg=Env().getConfig()
        self.cfg=cfg
        self.local=cfg['local_dir']
        self.temp='%s/tempdata' % self.local
        # for dset in self.getSets():
        #     d=Dataset(dset)
        #     print d.basetm

    def list_datasets(self):
        local=self.local
        # print local
        return glob.glob('%s/**/' % local)


    def save_buffer(self):
        ""
        temp=self.temp
        local=self.local
        try:
            # print temp
            tm=os.path.splitext(os.path.basename(glob.glob('%s/*.time' % temp)[0]))[0]
            # print tm
            ep=tm_to_epoch(tm,'%Y%m%d_%H%M%S')
            # print ep

            newfdr='%s/%s/%s' % (local,ep,'data')
            shutil.move(temp,newfdr)
        except:
            print "buffer empty"

    def getSets(self):
        local=self.local
        sets=glob.glob('%s/**/'% local)
        if  sets == []:
            os.mkdir('%s/%s' % (local,'buffer'))
        if 'buffer' in sets: sets.remove('buffer')
        # sets.re
        return sets

    def clear_buffer(self):
        try:
            local=self.local
            shutil.rmtree('%s/tempdata' % local)
        except:
            pass

        try:
            os.mkdir('%s/tempdata' % local)
        except:
            pass

    def poll_praco(self,ip):
        ""
        cfg=self.cfg
        # fa=ftp_list(cfg['archival_ip'],cfg['praco_username'],cfg['praco_password'])
        fe=ftp_list(ip,cfg['praco_username'],cfg['praco_password'])
        # d={}
        # d['archival']=fa
        # d['encoder']=fe
        # print fa
        print fe
        return fe

    def download_time(self,ip):
        temp=self.temp
        cfg=self.cfg
        try:
            os.mkdir(temp)
        except:
            pass
        try:
            ftp_download(ip,cfg['praco_username'],cfg['praco_password'],temp)
        except:
            pass

    def download(self,ip):
        temp=self.temp
        # print temp
        cfg=self.cfg
        try:
            os.mkdir(temp)
        except:
            pass
        try:
            ftp_download(ip,cfg['praco_username'],cfg['praco_password'],temp)
        except:
            pass

    def clear_praco(self,ip):
        ""
        cfg=self.cfg
        ftp_delete(ip,cfg['praco_username'],cfg['praco_password'])

    def init(self):
        ""
        # self.temp=
        local=self.local
        temp='%s/data' % local
        self.temp=temp

    def sync(self):
        ""
        cfg=self.cfg
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
        # os.move(tm,temp)



if __name__ == '__main__':
    ""
    # cfg=Env().getConfig()
    # local_dir=cfg['local_dir']
    # dm=DatasetMan()
    # print dm.getSets()
    # try:
        # globals()
    # dset=Dataset('c:/datasets/')
    # print dset.scan_files()
    # # except:
    #
    # files={}
    #
    # group={}
    # inuFileGroup=glob.glob('%s/**.inu')
    # for f in inuFileGroup:
    #     d={}
    #     stat=os.stat(f)
    #     d['ctime']=stat.st_ctime
    #     d['mtime']=stat.st_mtime
    #     group[f]=d
    # files['inu']=group
    #
    #
    # # print inuFileGroup
    # encFileGroup=glob.glob('%s/**.enc')
    # for f in encFileGroup:
    #     d={}
    #     stat=os.stat(f)
    #     d['ctime']=stat.st_ctime
    #     d['mtime']=stat.st_mtime
    #     group[f]=d
    # files['enc']=group

    # radFileGroup=glob.glob('%s/**.rad')

    # d['fileGroup']['inu']=inuFileGroup
    # d['fileGroup']['enc']=encFileGroup
    # self.files=files
    #
    # db=DatasetDB()
    # basetm=self.basetm
    # for g in self.files.keys():
    #     for fname,v in self.files[g].iteritems():
    #         print fname, v
    #         if g == 'enc':
    #             # task=DecodeEncTask()
    #             ctime=v['ctime'] + basetm
    #             mtime=v['mtime'] + basetm
    #             aTime=db.select('select * from counter') + ctime
    #
    #             db.insert(ctime)
    #             db.insert(aTime)
    #             db.insert(mtime)


