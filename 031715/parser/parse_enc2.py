# MPR encoder - tested on mpr_newfw.enc


import sys
import struct
from test.common.sqliteutils import *

def usage():
    print "Usage: daq_parse [options] file_directory"
    print "       Options:"
    print "         -v  Logger output on/off"
    print "         -d  File directory to read raw files"
    print "         -f  Individual file to parse"
    sys.exit(1)


TAILSYMBC="A5A5"
DB_COMMIT_INTERVAL=5

def get_next_record(fh,file_size,start,estimate,margin=6):
    pos_s=start
    dr=fh.read(estimate - margin)

    while(pos_s+estimate < file_size):
        dr1=fh.read(2)
        hexsymb=dr1.encode("hex").upper()
        # print hexsymb

        dr=dr+dr1
        if hexsymb == TAILSYMBC:
            #TODO: modify encoder firmware to be the same as rad
            # dr=dr+fh.read(4)
            break

    return dr

# clean off artifiacts
def reject_artifacts(dr):
    ""
    dr=dr.encode("hex")
    dr=dr.replace("e7e7","")
    dr=dr.decode("hex")

    return dr

# find the end of first header
def seek_until(fh,file_size):
  pre=0
  while (pre < file_size):
    bytes=fh.read(2).encode("hex").upper()
    # print bytes
    if bytes == TAILSYMBC:
      break
    else:
      pre+=2

  return fh.tell()

#convert raw counts into proper numerical
def apply_scaling(dr):
    ""
    ndr  = [i for i in range(42)]
    ndr[0] = dr[0] * 360. / 2**32
    ndr[1] = dr[1] * 5000. / 2**16
    ndr[2] = dr[2] * 5000. / 2**16
    ndr[3] = dr[3] * 5000. / 2**16
    ndr[4] = dr[4] * 5000. / 2**16
    ndr[5] = dr[5] * 5000. / 2**16
    ndr[6] = dr[6] * 5000. / 2**16
    ndr[7] = dr[7] * 5000. / 2**16
    ndr[8] = dr[8] * 5000. / 2**16
    ndr[9] = dr[9] * 5000. / 2**16
    ndr[10] = dr[10] * 5000. / 2**16

    ndr[11] = dr[11] * 5000. / 2**32
    ndr[12] = dr[11] * 5000. / 2**16
    ndr[13] = dr[13] * 5000. / 2**16
    ndr[14] = dr[14] * 5000. / 2**16

    ndr[15] = dr[15] * 5000. / 2**32
    ndr[16] = dr[16] * 5000. / 2**16
    ndr[17] = dr[17] * 5000. / 2**16
    ndr[18] = dr[18] * 5000. / 2**16

    ndr[19] = dr[19] * 5000. / 2**32
    ndr[20] = dr[20] * 5000. / 2**16
    ndr[21] = dr[21] * 5000. / 2**16
    ndr[22] = dr[22] * 5000. / 2**16
    ndr[23] = dr[23] * 5000. / 2**16
    ndr[24] = dr[24] * 5000. / 2**16
    ndr[25] = dr[25] * 5000. / 2**16
    ndr[26] = dr[26] * 5000. / 2**16
    ndr[27] = dr[27] * 5000. / 2**16
    ndr[28] = dr[28] * 5000. / 2**16
    ndr[29] = dr[29] * 5000. / 2**16

    ndr[30] = dr[30] * 5000. / 2**32
    ndr[31] = dr[31] * 5000. / 2**16
    ndr[32] = dr[32] * 5000. / 2**16
    ndr[33] = dr[33] * 5000. / 2**16

    ndr[34] = dr[34] * 5000. / 2**32
    ndr[35] = dr[35] * 5000. / 2**16
    ndr[36] = dr[36] * 5000. / 2**16
    ndr[37] = dr[37] * 5000. / 2**16

    ndr[38] = dr[38] * 5000. / 2**16
    ndr[39] = dr[39] * 5000. / 2**16
    ndr[40] = dr[40] * 5000. / 2**32

    ndr[41] = TAILSYMBC
    #dr[31] = file_index
    # dr[43] = convert_timestamp(dr[43])
    return ndr

  # current state machine
  # symb enc 14 11 24 21 34 31 45 55 65 75
  # symb enc 13 23 33
  # symb enc 11 21 31
  # symb enc 15 13 25 23 35 33 44 54 64 74
  # symb enc 11 21 31
  # symb enc 13 23 33
  # symb rIdx wIdx
  # symb counter

DAQ_FORMAT_LIST=["<2sLsBHsBHsBHsBHsBHsBHsBHsBHsBHsBH",
                   "2sLsBHsBHsBH",
                   "2sLsBHsBHsBH",
                   "2sLsBHsBHsBHsBHsBHsBHsBHsBHsBHsBH",
                   "2sLsBHsBHsBH",
                   "2sLsBHsBHsBH",
                   "2sHH",
                   "2sL"
            ]


# STATE MACHINE CALIB
CAL_FORMAT_LIST=["<2sHHHHH",
            "HHHHHHHH",
            "HHHHHHHH",
            "H2sHHHHHH",
            "HHHH2sHHH",
            "HHHHHHHH",
            "HHHH2sHHH",
            "HHHHHHHH",
            "HHHHHHHH",
            "HHH2sHHHH",
            "HHHH2sHHH",
            "HHHHHHHH",
            "HHHH2sHH2sL"]

fmt="".join(DAQ_FORMAT_LIST)
DAQ_BUFFER_SIZE= struct.calcsize(fmt)

fmt="".join(CAL_FORMAT_LIST)
CAL_BUFFER_SIZE= struct.calcsize(fmt)

db=DaqDB("daq.db")

def main():
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
            print pos_s

            if pos_s+DAQ_BUFFER_SIZE > file_size:
                break

            chunk=get_next_record(fh,file_size,pos_s,DAQ_BUFFER_SIZE)
            chunk=reject_artifacts(chunk)

            length=len(chunk)
            rec=struct.unpack(fmt,chunk)
            rec=apply_scaling(rec)
            
            timestamp=''
            rechash={}
            
            rechash.update({"encoder":rec[1], 'c1_a4':rec[1], 'c1_a1':rec[1], 'c2_a4':rec[1], 'c2_a1':rec[1],
                           'c3_a4':rec[1], 'c3_a1':rec[1], 'c4_a5':rec[1], 'c5_a5':rec[1], 'c6_a5':rec[1],
                           'c7_a5':rec[1]})
            rechash.update({'file_index':file_index, 'timestamp':timestamp, 'packet_len':length})
            db.insert_dict("enc",rechash)

            rechash={}
            rechash.update({'encoder':rec[1], 'c1_a3':rec[1], 'c2_a3':rec[1], 'c3_a3':rec[1]})
            rechash.update({'file_index':file_index, 'timestamp':timestamp, 'packet_len':length})
            db.insert_dict("enc",rechash)

            rechash={}
            rechash.update({'encoder':rec[1], 'c1_a1':rec[1], 'c2_a1':rec[1], 'c3_a1':rec[1]})
            rechash.update({'file_index':file_index, 'timestamp':timestamp, 'packet_len':length})
            db.insert_dict("enc",rechash)

            rechash={}
            rechash.update({'encoder':rec[1], 'c1_a5':rec[1], 'c1_a3':rec[1], 'c2_a5':rec[1], 'c2_a3':rec[1],
                           'c3_a5':rec[1], 'c3_a3':rec[1], 'c4_a4':rec[1], 'c5_a4':rec[1], 'c6_a4':rec[1],
                           'c7_a4':rec[1]})
            rechash.update({'file_index':file_index, 'timestamp':timestamp, 'packet_len':length})
            db.insert_dict("enc",rechash)

            rechash={}
            rechash.update({'encoder':rec[1], 'c1_a1':rec[1], 'c2_a1':rec[1], 'c3_a1':rec[1]})
            rechash.update({'file_index':file_index, 'timestamp':timestamp, 'packet_len':length})
            db.insert_dict("enc",rechash)

            rechash={}
            rechash.update({'encoder':rec[1], 'c1_a3':rec[1], 'c2_a3':rec[1], 'c3_a3':rec[1]})
            rechash.update({'file_index':file_index, 'timestamp':timestamp, 'packet_len':length})
            db.insert_dict("enc",rechash)

            # if i % DB_COMMIT_INTERVAL == 0 and i > 0:
            #     db.commit()
            #     print "commit %s" % i

        except Exception,e:
          print "read error: "+ str(e)

    print "records found %s" % i
    recdict=({})



main()