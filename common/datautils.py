__author__ = 'Ping'

import shutil
import os
from time import *
from subprocess import *
from pandas import DataFrame
import scipy

PATH_DATA="n:/YuPing/data/encoder"
PATH_PROGRAM="C:/Users/Ping/Workspace/DAQ"

def get_timestamp():
    return strftime('%Y%m%d_%H%M%S',gmtime())

def get_sw_revision():
    output = "261"
    # p1 = Popen(["svn info"], stdout=PIPE)
    # p2 = Popen(["grep \"Revision\""], stdin=p1.stdout, stdout=PIPE)
    # p3 = Popen(["awk \"print $2}\""], stdin=p2.stdout)
    # output = p3.communicate()[0]
    return output


class Repo:
    _repo_path=PATH_DATA

    def create_data_folder(self):
        foldername=self._repo_path+"/"+ get_timestamp()+"_rev"+get_sw_revision()
        os.mkdir(foldername)

    def set_repo_path(self,path):
        self._repo_path = path


class DataConverter:
    buffer

    def __init__(self):
        ""
    def connect(self,db,table):
        ""

    def dump_to_mat(self,path_matfile):
        scipy.io.savemat(path_matfile, mdict={'buffer': self.buffer})
    def dump_to_csv(self,path_csv):
        DataFrame.to_csv(path_csv)