import inspect
import os
import tarfile
import time
import datetime

__company__ = 'Boulder Environmental Sciences and Technology'
__project__ = ''
__author__ = 'Y. Shao'
__created__ = '3/17/2015' '10:02 AM'

def epoch_to_tm(epoch):
    ""
    print epoch
    return time.strftime("%Y%m%d %H:%M:%S %p",time.gmtime(epoch))

def daqtm_to_epoch(tm):
    ""
    # print tm
    filen=os.path.basename(tm)

    filen=filen[:-4]
    pattern='%Y%m%d_%H%M%S'
    # print filen
    print 'Y',filen
    epoch = int(time.mktime(time.strptime(filen, pattern)))
    return epoch


def tm_to_epoch(dt,pattern):
    # pattern='%Y%m%d %H:%M:%S %p'
    # print dt
    epoch = int(time.mktime(time.strptime(dt, pattern)))
    print epoch
    return epoch


def get_localtime():
    tm=datetime.datetime.now().timetuple()
    return time.strftime("%Y%m%d %H:%M:%S %p",tm)

def get_localepoch():
    return tm_to_epoch(datetime.datetime.now().strftime('%Y%m%d %H:%M:%S %p'))
# print datetime.datetime.now().strftime('%Y%m%d %H:%M:%S %p')

def extract_tarfile(fname):
    if (fname.endswith("tar.gz")):
        tar = tarfile.open(fname)
        tar.extractall()
        tar.close()
        print "Extracted in Current Directory"
        return True
    else:
        print "Not a tar.gz file: '%s '" % fname
        return False


def make_tarfile(output_filename, source_dir):
    with tarfile.open(output_filename, "w") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))

    return output_filename

def p_mname():
    return (inspect.currentframe().f_back.f_code.co_name)

