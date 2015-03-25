from common.env import Env
from common.utils import get_timestamp
from daqmanager.client.ftpfunc import touch, ftp_upload

cfg=Env().getConfig()
tm=get_timestamp()
tm=tm.replace('-','_')
touch(tm)
cfg=Env().getConfig()
print cfg['encoder_ip']
try:
    ftp_upload(cfg['encoder_ip'],cfg['praco_username'],cfg['praco_password'],tm)
except:
    pass
