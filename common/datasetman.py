import glob
import os
import shutil
from common.utils import get_timestamp
from common.env import Env
from daqmanager.client.ftpfunc import ftp_list, ftp_delete, ftp_download, ftp_upload, touch
from daqmanager.decoder.dataset import Dataset

__company__ = 'Boulder Environmental Sciences and Technology'
__project__ = ''
__author__ = 'Y. Shao'
__created__ = '3/30/2015' '12:53 PM'

class DatasetMan():
    def __init__(self):
        ""
        self.local=Env().getConfig()['local_dir']

        for dset in self.getSets():
            d=Dataset(dset)
            print d.basetm

    def list_datasets(self):
        local=self.local
        print local
        return glob.glob('%s/**/' % local)


    def save_buffer(self):
        ""


    def getSets(self):
        local=self.local
        sets=glob.glob('%s/**/'% local)
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

    def create_dataset(self):
        ""



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

    files={}

    group={}
    inuFileGroup=glob.glob('%s/**.inu')
    for f in inuFileGroup:
        d={}
        stat=os.stat(f)
        d['ctime']=stat.st_ctime
        d['mtime']=stat.st_mtime
        group[f]=d
    files['inu']=group


    # print inuFileGroup
    encFileGroup=glob.glob('%s/**.enc')
    for f in encFileGroup:
        d={}
        stat=os.stat(f)
        d['ctime']=stat.st_ctime
        d['mtime']=stat.st_mtime
        group[f]=d
    files['enc']=group

    # radFileGroup=glob.glob('%s/**.rad')

    # d['fileGroup']['inu']=inuFileGroup
    # d['fileGroup']['enc']=encFileGroup
    self.files=files

    db=DatasetDB()
    basetm=self.basetm
    for g in self.files.keys():
        for fname,v in self.files[g].iteritems():
            print fname, v
            if g == 'enc':
                # task=DecodeEncTask()
                ctime=v['ctime'] + basetm
                mtime=v['mtime'] + basetm
                aTime=db.select('select * from counter') + ctime

                db.insert(ctime)
                db.insert(aTime)
                db.insert(mtime)


