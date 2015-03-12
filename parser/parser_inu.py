import sys
from collections import namedtuple
import struct
import numpy as np
from test.common.sqliteutils import *


# INU structure
# c_double = DWORD
#
# original ctypes structure definition
#   PRE     byte        = FA
#   BID     byte        = FF
#   MID     byte        = 32
#   LEN     byte        = 43
#   DATA    26 bytes    = accx accy accz magx magy magz gyrx gyry gryz temp 3F3F FFFF FFFF FFFF FFFF inu_counter
#   CS      byte

  # cols = ['pre','bid','mid','len',
  #           'accx', 'accy', 'accz', 'magx', 'magy', 'magz', 'gyrx', 'gyry', 'gyrz', 'temperature1',
  #           '1','2','3','4','5','6','7','8','9','10','11','12','13','14',
  #           'a1','counter','cs','file_index','timestamp']


TIMESTAMP_HEAD='A7AF'
TIMESTAMP_TAIL='A7BF'

TAILSYMBD="3D3D"
DB_COMMIT_INTERVAL=5

def get_next_record(fh,file_size,start,estimate,margin=6):
    pos_s=start
    dr=fh.read(estimate - margin)

    while(pos_s+estimate < file_size):
        dr1=fh.read(2)
        hexsymb=dr1.encode("hex").upper()
        # print hexsymb

        dr=dr+dr1
        if hexsymb == TAILSYMBD:
            # dr=dr+fh.read(4)
            break

        # print dr.encode("hex")

    return dr

# find the end of first header
def seek_until(fh,file_size,pattern):
  pre=0
  while (pre < file_size):
    bytes=fh.read(2).encode("hex").upper()
    # print bytes
    if bytes == pattern:
      break
    else:
      pre+=2

  return fh.tell()


def extract_timestamp(dr):
    ""

    return timestamp


#convert raw counts into proper numerical
def apply_scaling(dr):
    ""
    ndr  = [i for i in range(120)]
    #header
    ndr[0] = dr[0] * 360. / 2**32
    ndr[1] = dr[1]
    ndr[2] = dr[2]


    return ndr

INU_FORMAT_LIST=["BBBB",
            "BBBBBBBBBBBB",
            "BB",
            "BBBBBBBB",
            "BBBBB"]

inu_fmt="".join(INU_FORMAT_LIST)
DAQ_BUFFER_SIZE= struct.calcsize(inu_fmt)

db=DaqDB("daq.db")

def parse_inu():
  file_index=-1
  i=-1
  for file in np.sort(glob.glob(os.path.join("data", '*.enc'))):
    file_index += 1

    file_size=os.stat(file).st_size
    print "Opening file %s size %s" % (file, file_size)

    with open(file,'rb') as fh:
      pos_s=seek_until(fh,file_size)

      i=0
      while(1):
        i += 1
        try:
            pos_s=fh.tell()

            if pos_s+DAQ_BUFFER_SIZE > file_size:
                break

            chunk=get_next_record(fh,file_size,pos_s,DAQ_BUFFER_SIZE)
            # chunk=reject_artifacts(chunk)

            length=len(chunk)
            rec=struct.unpack(inu_fmt,chunk)
            # rec=reject_headers(rec)
            # rec=remove_tuple(rec,'\xa6\xa5')
            # rec=remove_tuple(rec,'\xa7\xa5')
            timestamp=extract_timestamp(rec)
            rec=apply_scaling(rec)

            timestamp=''
            rechash={}
            rechash.update({"encoder_counter":rec[0], "motor_output":rec[1],
                            'c1_a4':rec[5], 'c1_a1':rec[8], 'c2_a4':rec[11], 'c2_a1':rec[14],
                           'c3_a4':rec[17], 'c3_a1':rec[20], 'c4_a5':rec[23], 'c5_a5':rec[26], 'c6_a5':rec[29],
                           'c7_a5':rec[32]})
            rechash.update({'file_index':file_index,  'packet_len':length})
            db.insert_dict("inu",rechash)

            if i % DB_COMMIT_INTERVAL == 0 and i > 0:
                db.commit()
                print "commit %s" % i
                update_progress(outPBar,pos_s,file_size)

        except Exception,e:
          print "read error: "+ str(e)

    print "records found %s" % i

import re

def extract_timestamp(dr):
    ""
    hex_dr=dr.encode("hex")
    match_group= re.match(r'HEADER_TIMESTAMP(.*)TAIL_TIMESTAMP',hex_dr)

    dr=dr.decode("hex")

    return match_group.group()

def update_progress(widget,pos_now,total_size):
    # widget.display((pos_now / total_size) * 100)
    percent = (pos_now / total_size) * 100
    print percent
    if percent == 100:
        return True

parse_inu()