from common.env import Env
from daqmanager.client.archive import archive_folder, make_folder

__company__ = 'Boulder Environmental Sciences and Technology'
__project__ = ''
__author__ = 'Y. Shao'
__created__ = '3/17/2015' '10:30 AM'

### API for daqmanager ###



if __name__ == '__main__':
    cfg=Env().getConfig()
    local_dir=cfg['local_dir']
    # print local_dir
    # make_folder()
    # archive_folder('1426610475')

    