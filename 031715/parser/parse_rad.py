import struct
from test.common.utils import *



def parse_imu(file):
 files_imu=os.list_files(REPO_DATA_PATH,"*.imu")
 for file_imu in files_imu:
  infile = open(file_imu,'rb')

  try:
    buff = infile.read()
  finally:
    infile.close

def parse_enc(file):

 files_enc=os.list_files(REPO_DATA_PATH,"*.enc")
 for file_enc in files_enc:
  infile = open(file_enc,'rb')

  try:
    buff = infile.read()
  finally:
    infile.close

REPO_DATA_PATH="c:/DataRepo"
import shutil

class ParseThread(object):
 def __init__(self):
     self._parseOn=False
     Thread.__init__(self)

 def run(self):
     self._parseOn=True


 def parse_rad(self,file):

   files_rad=os.list_files(REPO_DATA_PATH+"/","*.rad")

   for file_rad in files_rad:
       # while(self._parseOn=1 && file_rad.eof()):
       while(self._parseOn & file_rad.eof()):

         infile = open(file_rad,'rb')

       try:
         buff = infile.read()
       finally:
         infile.close

         infile.read_packet()
         infile.seek(0x00,0)
         print "Save Signature: " + infile.read(0x18)
         print "Save Version: " + str(struct.unpack('>i',buff[0x18:0x18+4])[0])
         infile.seek(0x1C,0)
         print "The letter R: " + infile.read(0x01)
         infile.seek(0x1D,0)
         print "Character Name: " + infile.read(0x20)
         infile.seek(0x3D,0)
         print "Save Game Name: " + infile.read(0x1E)
         print "Save game day: " + str(struct.unpack('>i',buff[0x5B:0x5B+4])[0])
         print "Save game month: " + str(struct.unpack('>i',buff[0x5D:0x5D+4])[0])
         print "Save game year: " + str(struct.unpack('>i', buff[0x5F:0x5F+4])[0])

       shutil.move(file_rad,REPO_DATA_PATH+"/Processed")



# dataB to sql -
def dump_to_sql():
    "INSERT "

# ********************************
# join data
# ********************************
def join_data():
    ""

    ""

# ********************************
# sql windowing and get
# ********************************
def sql_window_select():
    ""


# ********************************
# basic sql
# ********************************
def sql_select():
    ""

