__author__ = 'Ping'

import os
from os import *
from os.path import *
from zlib import *
import datetime
import time

def list_files(mypath):
    onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
    return onlyfiles

def calc_crc32(path_file):
    fo=open(path_file,"rb")
    return crc32(fo.read())


def get_size(path_dir):
    os.path.getsize(path_dir)

def get_timestamp():
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d_%H%M%S')
    return st