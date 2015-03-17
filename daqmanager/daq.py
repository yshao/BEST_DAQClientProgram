import glob
import os
import shutil
import time
from common.env import Env
from daqmanager.client.archive import archive_folder, make_folder
from daqmanager.client.utils import daqtm_to_epoch, tm_to_epoch, epoch_to_tm, get_localtime

__company__ = 'Boulder Environmental Sciences and Technology'
__project__ = ''
__author__ = 'Y. Shao'
__created__ = '3/17/2015' '10:30 AM'

### API for daqmanager ###

EPOCH_BASE=int(time.mktime(time.strptime('20000101_000000', '%Y%m%d_%H%M%S')))

def proc_folder(path):
    # print path


    folders=glob.glob(path+'/**/')
    # print folders
    for fdr in folders:
        lFdr=glob.glob(fdr+'/**')
        # print lFdr
        for f in lFdr:
            ep= daqtm_to_epoch(f)
            print ep
            ext=os.path.basename(f)[-3:]
            # ext=os.path.extname(f)
            print get_localtime()
            base_time=tm_to_epoch(get_localtime())
            print ext,base_time
            print base_time,ep
            ### adjust for 1970 ###
            print EPOCH_BASE
            print epoch_to_tm(int(base_time) + int(ep) - EPOCH_BASE)
            # shutil.move(f,'%s/%s'%(ep,ext))

if __name__ == '__main__':
    cfg=Env().getConfig()
    local_dir=cfg['local_dir']
    path=local_dir+'/'+'1426610475'
    print path
    proc_folder(path)
    # print local_dir
    # make_folder()
    # archive_folder('1426610475')

    # decode

    # proc_tm_folder()

