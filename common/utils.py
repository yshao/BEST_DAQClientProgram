__author__ = 'Ping'

import zipfile
import logging
import os
import ctypes
import subprocess
import time
import re
import ftplib
import shutil
import io, xmltodict


# definitions
MB=1024*1024*8

# init configs
INI_ZIPFILE_NAMING="%Y%m%d%H%M%S"
INI_SDDISK_SIZE= MB * 1000
INI_TIMEFORMAT="%Y%m%d%H%M%S"
INI_FILE_LEN=MB*4
INI_FILE_NAMING="%Y%m%d%H%M%S"




FILEEXT_ENC="enc"
FILEEXT_INU_MTIG="inumti"
FILEEXT_INU_RAZOR="inuraz"
FILEEXT_RAD="rad"


FILE_CONFIG="config.xml"
FILE_TIMESTAMP="timestamp.csv"
FILE_MARKEDFILE="marked_file.csv"


def xml_load_config(xmlfile):
    infile=io.open(xmlfile,"r")
    return xmltodict.parse(infile.read())

def xml_save(xmlfile):
    outfile=io.open(xmlfile,"w")
    outfile.write(xmltodict.unparse(io,pretty=True))


def zip(path_zip,dir_pkg):
    path_cmd="C:/Program Files/7-Zip/7z.exe"
    cmd_list = ["a -tzip",path_zip, dir_pkg,"-r"]
    token_list=["Everything is Ok"]
    exec_cmd(path_cmd,cmd_list,token_list)


def exec_cmd(cmd_path,cmd_sw_list,token_list):
    cmd = cmd_path + " ".join(cmd_sw_list)
    subproc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    try:
        out,err = subproc.communicate()
        parse_list = parse_command2(out,token_list)
        result= cmd+" - [OUTPUT]: PASSED - "+"\n".join(parse_list)
    except:
        result= cmd +" - [OUTPUT]: FAILED - "+"\n".join(parse_list)


def convert_data(data,type):
  if type== "hex":
        data_16 = data.encode('hex')
        return data_16
  elif type== "base64":
        data_64 = data.encode('base64')
        return data_64
  elif type == "bin":
        data_16 = data.encode('hex')
        data_2 = bin(int(data_16,16))
        return data_2

def get_timestamp():
    timestr = time.strftime("%Y%m%d-%H%M%S")
    return timestr

def create_logger(script_name,start_message):
    logger = logging.getLogger(script_name)
    hdlr = logging.FileHandler(script_name+".log")
    logger.debug("Creating Logger for "+script_name)
    logger.addHandler(hdlr)
    logger.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()

    logger.info("")
    logger.info("****************************************************************************")
    logger.info(start_message)
    logger.info("****************************************************************************")

    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    hdlr.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(ch)

    return logger

from easylogger import *

def create_logger_2(s_log,s_start_message,num_file_size):
    logger = get_logger(s_log)
    hdlr = logging.handlers.RotatingFileHandler(s_log+".log",maxBytes=num_file_size)
    logger.debug("Creating Logger for "+s_log)
    logger.append_handlers(hdlr)
    logger.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()

    logger.info("")
    logger.info("****************************************************************************")
    logger.info(s_start_message)
    logger.info("****************************************************************************")

    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    hdlr.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.append_handlers(ch)

    return logger


def countdown(n):
 print('Starting to count from', n)
 while n > 0:
    yield n
    n -= 1
 print('Done!')

def count_down(seconds):
    count=0
    while count < seconds:
        time.sleep(1)
        print "count " + str(seconds - count) + "\n"
        count = count + 1

def rm(filename):
    if os.path.isfile(filename):
        os.remove(filename)


def createLogger(name,log_file):
    logger = logging.getLogger(name)
    # logger.setLevel(logging.DEBUG)

    # create file handler which logs even debug messages
    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.DEBUG)

    # create console handler with a higher log level
    # ch = logging.StreamHandler()
    # ch.setLevel(logging.ERROR)
    logger.info("Creating logger for",name,"in",log_file)
    return logger,fh

def add_c_file(filename):
    print "INFO","Adding file",filename


def exec_script(pyscript):
    msg,err=call_command(["python", pyscript])

    if (not err):
        return msg,"\nDONE!!!"
    else:
        return "FAILED!!!"

def call_command(list):
    print list
    subproc = subprocess.Popen(list, stdout=subprocess.PIPE)
    return subproc.communicate()


def timeout_command(command, timeout):
    """call shell-command and either return its output or kill it
    if it doesn't normally exit within timeout seconds and return None"""
    import subprocess, datetime, os, time, signal
    start = datetime.datetime.now()
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    while process.poll() is None:
      time.sleep(0.1)
      now = datetime.datetime.now()
      if (now - start).seconds> timeout:
        os.kill(process.pid, signal.SIGKILL)
        os.waitpid(-1, os.WNOHANG)
        return None
    return process.stdout.read(), process.stderr.read()

def parse_command(msg):
    match = re.search(msg)

def parse_command2(output,tokens):
    result=[]
    for row in output.split('\n'):
        for token in tokens:
            if re.match(token,row):
                result.append(row)

    return result

def zipfile_unzip(source_filename, dest_dir):
    with zipfile.ZipFile(source_filename) as zf:
        for member in zf.infolist():
            # Path traversal defense copied from
            # http://hg.python.org/cpython/file/tip/Lib/http/server.py#l789
            words = member.filename.split('/')
            path = dest_dir
            for word in words[:-1]:
                drive, word = os.path.splitdrive(word)
                head, word = os.path.split(word)
                if word in (os.curdir, os.pardir, ''): continue
                path = os.path.join(path, word)
            zf.extract(member, path)

def ftp_send(src_file,targ_addr,ip,user,passwd):
    try:
        session = ftplib.FTP(ip,user, passwd)
        file = open(src_file,'rb')                  # file to send
        session.storbinary('STOR '+targ_addr, file)     # send the file
        file.close()                                    # close file and FTP
        session.quit()
        return "Passed!!!"
    except:
        return "Error!!!"


def ignore_list(path, files):
	ign = []
	for fname in files:
		fullFileName = os.path.normpath(path) + os.sep + fname
		if not os.path.isdir(fullFileName) \
		   and not fname.endswith('exe'):
			ign.append(fname)
	return ign

def copy_exe(src, dest):
    try:

        shutil.copytree(src=src,dst=dest,ignore=ignore_list)
        # print glob.glob(DEST_DIR+'/*')

    except OSError as e:
        # If the error was caused because the source wasn't a directory
        if e.errno == 20:
            shutil.copy(src, dest)
        else:
            print('Directory not copied. Error: %s' % e)


class BinStructReader:
    def __init__(self,struct):
        self.struct=struct

    def parse(self,bin_io):
        return self.struct.parse(bin_io)

    def build(self,struct_io):
        return self.struct.build(struct_io)


def create_logger_2(s_log,s_start_message):
    return create_logger(s_log,s_start_message)