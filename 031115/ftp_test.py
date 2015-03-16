# Download some files from the login directory.
import ftputil
from common.env import Env

cfg=Env().getConfig()

d={}
for k in cfg.keys():
    if k[-2:] == 'ip':
        name=k[:-3]
        d[k]={}
        d[k]['ip']=cfg[k]
        d[k]['folder']=name

pwd=cfg['praco_password']
user=cfg['praco_username']

local=cfg['local_dir']

### move files into folders ###
for ip in enumerate(d):
    print "transferring from %s" % ip
    with ftputil.FTPHost(ip, user, pwd) as host:
        names = host.listdir(host.curdir)
        for name in names:
            if host.path.isfile(name):
                # Remote name, local name, binary mode
                host.download(name, name)

