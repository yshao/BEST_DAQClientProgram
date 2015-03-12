import sys
from collections import namedtuple
import struct
import numpy as np
from best.commonsqliteutils import *


# INU structure
#
# original ctypes structure definition
#   PRE     byte        = FA
#   BID     byte        = FF
#   MID     byte        = 32
#   LEN     byte        = 43
#   DATA    26 bytes    =   accx accy accz magx magy magz gyrx gyry gryz
#                           temp
# Press         - U2
# press stat    - U1
# ITOW          - U4
# LAT           - I4
# LON           - I4
# ALT           - I4
# VEL_N         - I4
# VEL_E         - I4
# VEL_D         - I4
# Hacc          - U4
# Vacc          - U4
# Sacc          - U4
# bGPS          - GPS
# TS            - U2

# Status    byte
#   CS      byte

#                           tailsymb


TAILSYMBD="3D3D"
DB_COMMIT_INTERVAL=5

# clean off artifiacts
def reject_artifacts(dr):
    ""
    dr=dr.encode("hex")
    # print dr
    dr=dr.replace("e7e7","")
    # print dr
    dr=dr.decode("hex")

    return dr

def reject_headers(dr):
    ""
    dr=dr.encode("hex")
    print dr
    dr=dr.decode("hex")

    return dr


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
    hex_dr=dr.encode("hex")
    match_group= re.match(r'HEADER_TIMESTAMP(.*)TAIL_TIMESTAMP',hex_dr)

    dr=dr.decode("hex")

    return match_group.group()


#convert raw counts into proper numerical
def apply_scaling(dr):
    ""
    ndr  = [i for i in range(120)]
    #header
    ndr[0] = dr[0]
    ndr[1] = dr[1]
    ndr[2] = dr[2]
    ndr[3] = dr[3]

    ndr[4] = dr[4]
    ndr[5] = dr[5]
    ndr[6] = dr[6]
    ndr[7] = dr[7]
    ndr[8] = dr[8]
    ndr[9] = dr[9]
    ndr[10] = dr[10]
    ndr[11] = dr[11]
    ndr[12] = dr[12]
    ndr[13] = dr[13]

    ndr[14] = dr[14]
    ndr[15] = dr[15]
    ndr[16] = dr[16]
    ndr[17] = dr[17]

    ndr[18] = dr[18]
    ndr[19] = dr[19]
    ndr[20] = dr[20]
    ndr[21] = dr[21]
    ndr[22] = dr[22]
    ndr[23] = dr[23]
    ndr[24] = dr[24]
    ndr[25] = dr[25]
    ndr[26] = dr[26]
    ndr[27] = dr[27]
    # ndr[28] = dr[28]

    # ndr[29] = dr[29]
    # ndr[30] = dr[30]

    return ndr


INU_FORMAT_LIST= [
            'BBBB',
            'HHHHHHHHH',
            'HBI',
            'iiiiii',
            'III',
            'B',
            'B',
            '4s'
            ]

inu_fmt="".join(INU_FORMAT_LIST)
DAQ_BUFFER_SIZE= struct.calcsize(inu_fmt)

db=DaqDB("daq.db")

def parse_inu(queue):
  file_index=-1
  i=-1
  for file in np.sort(glob.glob(os.path.join("data", '*.inu'))):
    file_index += 1

    file_size=os.stat(file).st_size
    print "Opening file %s size %s" % (file, file_size)

    with open(file,'rb') as fh:
      pos_s=seek_until(fh,file_size,"3D3D")

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
            print length
            print DAQ_BUFFER_SIZE

            rec=reject_headers(chunk)

            rec=struct.unpack(inu_fmt,chunk)

            # timestamp=extract_timestamp(rec)
            rec=apply_scaling(rec)

            timestamp=''
            rechash={}

            rechash.update({
                    'PRE':rec[0], 'BID':rec[1], 'MID':rec[2], 'LEN':rec[3],
                    "accX":rec[4], "accY":rec[5], "accZ":rec[6],
                    'gyrX':rec[7], 'gyrY':rec[8], 'gyrZ':rec[9],
                    'magX':rec[10], 'magY':rec[11], 'magZ':rec[12],
                    # 'temp':rec[13],
                    'Press':rec[13],'pPrs':rec[14],'ITOW':rec[15],
                    'LAT':rec[16],'LON':rec[17],'ALT':rec[18],'VEL_N':rec[19],'VEL_E':rec[20],'VEL_D':rec[21],
                    'Hacc':rec[22],'Vacc':rec[23],'Sacc':rec[24],
                    'bGPS':rec[25],
                    # 'TS':rec[27],
                    'STATUS':rec[26],'CS':rec[27],
                    'tailsymb':rec[28]

                    })
            rechash.update({'counter':1000,'wIdx':0,'rIdx':0,'tailsymb':rec[30]})
            rechash.update({'file_index':file_index,  'packet_len':length})
            db.insert_dict("inu",rechash)

            if i % DB_COMMIT_INTERVAL == 0 and i > 0:
                db.commit()
                # print "commit %s" % i

                queue.put("commit %s" % i)
                queue.put(update_progress(pos_s,file_size))

        except Exception,e:
          print "read error: "+ str(e)

    # print "records found %s" % i
    queue.put("records found %s" % i)

    return "OK"

import re

def extract_timestamp(dr):
    ""
    hex_dr=dr.encode("hex")
    match_group= re.match(r'HEADER_TIMESTAMP(.*)TAIL_TIMESTAMP',hex_dr)

    dr=dr.decode("hex")

    return match_group.group()

def update_progress(pos_now,total_size):
    # widget.display((pos_now / total_size) * 100)
    percent = (pos_now / total_size) * 100
    print percent
    if percent == 100:
        return True

from multiprocessing import Queue
q=Queue()
parse_inu(q)

# import time
# time.sleep(6)
#
#
# def t3():
#     for i in range(10):
#         print "running 3"
#         time.sleep(1)