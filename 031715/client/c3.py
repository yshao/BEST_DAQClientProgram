### get all
import datetime
import os
import ftputil
from best.common.configutils import Config

config=Config("../config.xml")
host=config.get("IP_ARCHIVAL")
user=config.get("REMOTE_USER")
password=config.get("REMOTE_PASSWORD")

folder="test1"
localdir=os.path.join(config.get("LOCAL_DATA_DIR"),folder)
log=config.get("FTP_LOG")
size=config.get("FILE_LEN_IMU")

log = open(log,"a")
print "logging into FTP" # print
host= ftputil.FTPHost('localhost','devadmin','password') # ftp host info

try:
    recursive = host.walk("/package/FlashDisk/Data",topdown=True,onerror=None) # recursive search
    # print recursive
    for root,dirs,files in recursive:
        # dir= dirs[0]
        # print files
        # print dirs

        for name in files:
                # print dirs
                # print name
                fpath=host.path.join(root,name)
                print fpath
                if host.path.isfile(fpath):

                    statinfo = host.stat(fpath)
                    # print host.stat(fpath).mtime
                    file_mtime = datetime.datetime.utcfromtimestamp(statinfo.st_mtime)
                    file_size = statinfo.st_size
                    # print 'Files with pattern: %s and epoch mtime is: %s ' % (video_list, statinfo.st_mtime)
                    print 'Last Modified: %s' % datetime.datetime.utcfromtimestamp(statinfo.st_mtime)
                    print 'Size: %' % file_size
                    # if file_mtime >= utc_datetime_less24H:
                    if file_size >= size-10:
                        # for fname in video_list:
                        #     fpath = host.path.join(root, fname)
                        #     if host.path.isfile(fpath):
                        host.download_if_newer(fpath, os.path.join(localdir, name), 'b')


except Exception,e:
               print "Error: %s occurred" % (e)

host.close