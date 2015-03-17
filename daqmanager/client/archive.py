import datetime
from common.env import Env
from daqmanager.client.utils import tm_to_epoch, get_localepoch, make_tarfile
from daqmanager.remote.remote import Remote

__company__ = 'Boulder Environmental Sciences and Technology'
__project__ = ''
__author__ = 'Y. Shao'
__created__ = '3/16/2015' '6:37 PM'


def archive_folder(tm):
    cfg=Env().getCOnfig()
    local_dir=cfg['local_dir']

    tm=get_localepoch()

    path='%s/%s' % (local_dir,tm)
    filep=make_tarfile(path,'%s.tar.gz' % tm)
    # make_tar(tm,filep)

    remote=Remote('dataserver')
    remote.upload([filep])
    # remote.run() optional
