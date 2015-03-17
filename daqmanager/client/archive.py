import datetime
import os
from common.env import Env
from daqmanager.client.utils import tm_to_epoch, get_localepoch, make_tarfile, p_mname
from daqmanager.remote.remote import Remote

__company__ = 'Boulder Environmental Sciences and Technology'
__project__ = ''
__author__ = 'Y. Shao'
__created__ = '3/16/2015' '6:37 PM'


def make_folder():
    tm=get_localepoch()
    cfg=Env().getConfig()
    local_dir=cfg['local_dir']

    path='%s/%s' % (local_dir,tm)
    os.mkdir(path)

def archive_folder(tm):
    cfg=Env().getConfig()
    local_dir=cfg['local_dir']

    # tm=get_localepoch()

    try:
        path='%s/%s' % (local_dir,tm)
        filep=make_tarfile('%s.tar.gz' % tm,path)
        print filep

        # remote=Remote('dataserver')
        # remote.upload([filep])
    # remote.run() optional
        return True

    except Exception, e:
        print '%s' % e,p_mname()
        # pass
        return False

