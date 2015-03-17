from common.env import Env
from common.sysutils import run_command

__company__ = 'Boulder Environmental Sciences and Technology'
__project__ = ''
__author__ = 'Y. Shao'
__created__ = '3/16/2015' '10:32 AM'

def load_config():
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


def check_network():
    def is_connected(d):
        if 'unreachable' in d:
            print 'offline'
        else:
            print 'online'

    cfg=Env().getConfig()

    b=False
    # while (not b):

    ip=cfg['archival_ip']
    print "Check archival %s -w 3" % ip
    r=run_command('ping %s' % ip)
    b1= is_connected(r)
    ip=cfg['encoder_ip']
    print "Check encoder %s -w 3" % ip
    r=run_command('ping %s' % ip)
    b2= is_connected(r)
    is_connected(r)
    b= b1 and b2

    print "Check archival %s -w 3" % ip
    r=run_command('ping %s' % ip)
    b1= is_connected(r)
    ip=cfg['encoder_ip']
    print "Check encoder %s -w 3" % ip
    r=run_command('ping %s' % ip)
    b2= is_connected(r)

    ip=cfg['switch1']
    print "Check switch1 %s" % ip
    r=run_command('ping %s -w 3' % ip)
    b3= is_connected(r)

    ip=cfg['switch2']
    print "Check switch2 %s -w 3" % ip
    r=run_command('ping %s' % ip)
    b4= is_connected(r)
    ip=cfg['switch3']
    print "Check switch3 %s -w 3" % ip
    r=run_command('ping %s' % ip)
    b5= is_connected(r)

    b= b1 and b2 and b3 and b4 and b5

    for k in cfg['radiometer'].keys():
        ip=cfg['radiometer'][k]
        print "Check %s %s" % (k,ip)
        r=run_command('ping %s' % ip)
        is_connected(r)
        br= is_connected(r)

        b= b and br
    if b:
        print "Network fully on"
    else:
        print "Network not ready"
    return b