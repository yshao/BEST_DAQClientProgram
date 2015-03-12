#!/usr/local/bin/python
__author__ = 'Ping'

## @package checkinutil
#  Formal check in script
#
#
import os
from utils import *
import datetime
import string
import sys
import re

## Options
#
#
#

PATH_SVN_WORK_BRANCH="file://192.168.1.223/data/YuPing/Repo/branches/trunk"
PATH_SVN_MAIN_TRUNK="file://192.168.1.223/data/svnrepo/trunk"

PATH_WORK_DESKTOP="//RADEGAST/Users/Ping/Workspace/DAQ"
PATH_WORK_LAPTOP="c:/Users/shand/Workspace/DAQ"

CONFIG_CHECKIN="check_in.xml"

path_export_temp="C:/tempdir/export"



def script_common(func):
    func.attr="common"
    # if gLogger.exists():
    #     gLogger.debug()
    return func


@script_common
def svn_update(dirname):
    path_svn="c:/bin/Apache-Subversion-1.8.8/bin/svn.exe"
    cmd_sw=["update"]
    token_list=["At revision"]
    call_command_and_parse2(path_svn,cmd_sw,token_list)



def checkin_trunk(trunk,svn_path):
    os.chdir(trunk)
    cmd_list=["svn ci -m ''"]
    token_list=[""]
    call_command_and_parse2(cmd_list,token_list)
    # msg = string.join([trunk,"checking in to",svn_path])
    # logger.debug(msg)
    os.chdir(starting_dir)

def svn_export():

def svn_commit():
    path_svn="c:/bin/Apache-Subversion-1.8.8/bin/svn.exe"
    cmd_sw=["ci -m ''"]
    token_list=["At revision"]
    print " ".join(path_svn,cmd_sw)

#     call_command_and_parse2(path_svn,cmd_sw,token_list)
#
# def call_command_and_parse2(cmd_path,cmd_sw_list,token_list):
#     cmd = " ".join(cmd_path,cmd_sw_list,token_list)
#     subproc = subprocess.Popen(" ".join(cmd), stdout=subprocess.PIPE)
#     try:
#         out,err = subproc.communicate()
#         parse_list = parse_command2(out,token_list)
#         result= cmd+" - [OUTPUT]: PASSED - "+"\n".join(parse_list)
#         logger.debug(result)
#     except:
#         result= cmd +" - [OUTPUT]: FAILED - "+"\n".join(parse_list)
#         logger.warn(result)

 gLogger=create_logger()


 svn_update(PATH_SVN_MAIN_TRUNK)
 svn_commit(PATH_SVN_WORK_BRANCH)

 gLogger.debug("update work trunks")
 #
 svn update(PATH_WORK_DESKTOP)
 svn commit(PATH_WORK_DESKTOP)

 # /Workspace
 svn update(PATH_WORK_LAPTOP)
 svn commit(PATH_WORK_DESKTOP)

 gLogger.debug("pass compile test - YES")

def merge_trunks():
 svn_export(PATH_SVN_MAIN_TRUNK,path_export_temp)
 svn_export(PATH_SVN_WORK_BRANCH,path_export_temp)
 svn_diff(path_export_temp)
 check_config(CONFIG_CHECKIN,"Diff")
 run_gtest(path_export_temp)
 svn_commit_to(path_export_temp,PATH_SVN_MAIN_TRUNK)


def check_config():

def get_svn_log():


def main():
    #input

    #input

    #input

    #input
        get_svn_log()

main()

