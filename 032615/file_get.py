import os
from common.env import Env
from daqmanager.client.utils import tm_to_epoch, epoch_to_tm

name='file_get.py'
stats=os.stat(name)
d={}
# class
# d[name]
d[name]={}
d[name]['mtime']=stats.st_mtime

d[name]['ctime']=stats.st_ctime

d[name]['size']=stats.st_size

dd=d[name]

print epoch_to_tm(dd['mtime'])
print epoch_to_tm(dd['ctime'])

cfg=Env().getConfig()

cfg[]