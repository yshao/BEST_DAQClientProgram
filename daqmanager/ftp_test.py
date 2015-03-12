import sys
import os
import ftplib
import ftputil
import fnmatch

import numpy as np

### get current folder ###
from stat import S_ISREG, ST_CTIME, ST_MODE
import os, sys, time

# path to the directory (relative or absolute)
dirpath = sys.argv[1] if len(sys.argv) == 2 else r'.'

# get all entries in the directory w/ stats
entries = (os.path.join(dirpath, fn) for fn in os.listdir(dirpath))
entries = ((os.stat(path), path) for path in entries)

# leave only regular files, insert creation date
entries = ((stat[ST_CTIME], path)
           for stat, path in entries if S_ISREG(stat[ST_MODE]))
#NOTE: on Windows `ST_CTIME` is a creation date
#  but on Unix it could be something else
#NOTE: use `ST_MTIME` to sort by a modification date

for cdate, path in sorted(entries):
    # print time.ctime(cdate), os.path.basename(path)
    print os.path.basename(path)

### get ftp file list
ftpEntries=[]
### filter existing ###
sync=list(set(entries) - set(ftpEntries))

### get all

# log = open("C:/..../ftp_name.txt","a")
# print "logging into FTP" # print
# host = ftputil.FTPHost('address','Uname','Pass') # ftp host info
# recursive = host.walk("/WORLDVIEW",topdown=True,onerror=None) # recursive search
# for root,dirs,files in recursive:
#     totalFilesCount =files.len() -1
#     for idx,name in enumerate(np.sort(files)):
#         if idx == totalFilesCount:
#             break
#         else:   ### skip the last one
#             fullpath = os.path.join(root, name)
#             size = FTP.size(fullpath)
#             writepath = fullpath + " " +size + "\n"
#             log.write(writepath)



# ftp.sendcmd("TYPE i")    # Switch to Binary mode
# ftp.size("/some/file")   # Get size of file