from fabric.context_managers import settings
import psutil
import sys
from common.env import Env
from sysutils import run_command

__company__ = 'Boulder Environmental Sciences and Technology'
__project__ = ''
__author__ = 'Y. Shao'
__created__ = '2/25/2015' '1:50 PM'


env=Env()
cfg=env.getConfig()

# print cfg

host='%s@%s' %(cfg['smap_server_username'],cfg['smap_server_host'])
pwd=cfg['smap_server_password']
# print host,pwd

### Remote API is ubuntu server centric ###

### psutil ###
def get_connections():
    p=psutil.Process()
    d= p.get_cpu_times()
    return d

def get_disk_partitions():
    ""
    return psutil.Process().disk_partitions()

def get_stats():
    ""

def get_ps():
    ""

def get_net_connections():
    ""
    return psutil.Process().net_connections()

def get_up_time():
    ""
    return psutil.Process().boot_time()

def get_pids():
    ""
    return psutil.Process().pids()




def ctrl_daemon(daemon,*arg):
    p=psutil.Process()
    ## find daemon
    print "running %s %s" %(daemon,cmd)

    # filep=
    run_command('python %s %s'%(daemon,cmd))

def check_daemon(daemon):
    p=psutil.Process

    return True

if __name__ == '__main__':
    cmd=sys.argv[1]
    params=sys.argv[2:]
    # print 'calling:',cmd,params

    if cmd in locals():
        func = locals()[cmd]
        res=func(*params)
        print res
        # store as object
        # with open('finish.txt', 'wb') as fh:
        #     fh.write()
        sys.exit(0)