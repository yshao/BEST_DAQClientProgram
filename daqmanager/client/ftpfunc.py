import os
import re
import ftplib
import time
from common.env import Env
from common.utils import get_timestamp

def touch(fname, times=None):
    with open(fname, 'a'):
        os.utime(fname, times)


def upload_time(ip,tm):
    cfg=Env().getConfig()
    try:
        ftp_upload(ip,cfg['praco_username'],cfg['praco_password'],tm)
    except:
        pass
    # time.sleep(2)


# local_dir='c:/datasets'

class FtpClient(object):
    newline = "\n"
    def __init__(self,host_url,username,password):
        ""
        self.ftp=ftplib.FTP(host_url,username,password)
        # username = username + self.newline
        # password = username + self.newline
        self.path='/FlashDisk/Data'
        self.ftp.chdir("/FlashDisk/Data")

    def list(self):
        data=[]
        self.ftp.dir(data.append)

        fl=[]
        for line in data:
            # print "-", line
            fl.append(re.split(' *',line)[3])

        return data

    def show_list(self):
        data=[]
        self.ftp.dir(data.append)

        fl=[]
        for line in data:
            print "-", line
            # fl.append(re.split(' *',line)[3])

        # return data

    def ftp_download(self,local_dir):
        fl=self.list

        for f in fl:
            # print f
            with open('%s/%s'%(local_dir,f),'wb') as fh:
                print 'RETR %s/%s' % (self.path,f)
                self.ftp.retrbinary('RETR %s/%s' % (self.path,f), fh.write)

        # ftp.quit()
        return fl

    def close(self):
        self.ftp.quit()



def ftp_download(ip,user,pwd,local_dir):
    ftp = ftplib.FTP(ip)
    print ip
    ftp.login(user, pwd)

    path='/FlashDisk/Data'
    data = []
    ftp.cwd(path)
    ftp.dir(data.append)
    # local_dir

    fl=[]
    for line in data:
        # print "-", line
        fl.append(re.split(' *',line)[3])

    for f in sorted(fl):
        # print
        with open('%s/%s'%(local_dir,f),'wb') as fh:
            print 'RETR %s/%s' % (path,f)
            ftp.retrbinary('RETR %s/%s' % (path,f), fh.write)


    ftp.quit()
    return fl

def ftp_list(ip,user,pwd):
    ftp = ftplib.FTP(ip)
    ftp.login(user, pwd)

    path='/FlashDisk/Data'
    data = []
    ftp.cwd(path)
    ftp.dir(data.append)


    fl=[]
    for line in data:
        # print "-", line
        fl.append(re.split(' *',line)[3])

    return fl

def ftp_delete(ip,user,pwd):
    ftp = ftplib.FTP(ip)
    ftp.login(user, pwd)

    path='/FlashDisk/Data'
    data = []
    ftp.cwd(path)
    ftp.dir(data.append)
    # print data


    fl=[]
    for line in data:
        # print "-", line
        fl.append(re.split(' *',line)[3])

    for f in fl:
        ftp.delete(f)

def ftp_upload(ip,user,pwd,filep):
    ftp = ftplib.FTP(ip)
    ftp.login(user, pwd)

    path='/FlashDisk/Data'
    # data = []
    ftp.cwd(path)

    ftp.storlines("STOR " + filep, open(filep, 'r'))

    ftp.quit()
    # return fl


### poll list
# if __name__ == '__main__':
#     cfg=Env().getConfig()
#     print cfg



# if __name__ == '__main__':
# #     cfg=Env().getConfig()
# #     tm=get_timestamp()
# #     tm=tm.replace('-','_')
# #     touch(tm)
# #     cfg=Env().getConfig()
# #     # ftp_upload(cfg['archival_ip'],cfg['praco_username'],cfg['praco_password'],tm)
# #

#     print cfg['encoder_ip']
#     print cfg['archival_ip']

#### download ####
    # try:
    #     os.mkdir('./data')
    # except:
    #     pass
    # try:
    #     ftp_download(cfg['archival_ip'],cfg['praco_username'],cfg['praco_password'],'./data')
    # except:
    #     pass
    # try:
    #     ftp_download(cfg['encoder_ip'],cfg['praco_username'],cfg['praco_password'],'./data')
    # except:
    #     pass

### delte

    # # ftp_delete(cfg['archival_ip'],cfg['praco_username'],cfg['praco_password'])
    # ftp_delete(cfg['encoder_ip'],cfg['praco_username'],cfg['praco_password'])
    # ftp_delete(cfg['archival_ip'],cfg['praco_username'],cfg['praco_password'])
    # # print ftp_list(cfg['archival_ip'],cfg['praco_username'],cfg['praco_password'])
    #
    # ftp_upload(cfg['archival_ip'],cfg['praco_username'],cfg['praco_password'],tm)




