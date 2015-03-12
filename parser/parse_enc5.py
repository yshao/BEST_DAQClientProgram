# PRACO_decoder


import sys
import struct
from test.common.sqliteutils import *
from datautils import *

def usage():
    print "Usage: daq_parse [options] file_directory"
    print "       Options:"
    print "         -v  Logger output on/off"
    print "         -d  File directory to read raw files"
    print "         -f  Individual file to parse"
    sys.exit(1)

TAILSYMBC="3C3C"
HEADER_STAT_DUMP_INIT="A7E8"
HEADER_STAT_DUMP_DATA="A7E1"
HEADER_ENC_DUMP="A7FC"


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

        # print dr.encode("hex")

    return dr


def remove_tuple(original_tuple, element_to_remove):
    new_tuple = []
    for s in list(original_tuple):
        if not s == element_to_remove:
            new_tuple.append(s)
    return tuple(new_tuple)

# clean off artifiacts
def reject_artifacts(dr):
    ""
    dr=dr.encode("hex")
    dr=dr.replace("e7e7","")
    dr=dr.decode("hex")

    return dr

def reject_headers(dr):
    ""
    dr=dr.encode("hex")
    dr=dr.replace("a6a5","")
    dr=dr.replace("a7a5","")
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

# import math.pi

#convert raw counts into proper numerical
def apply_scaling(dr):
    ""
    ndr  = [i for i in range(120)]
    #header
    # 0     mo1
    # 1     mo2
    # 2     enc
    ndr[0] = dr[0]
    ndr[1] = dr[1]
    ndr[2] = dr[2] * 360. / 2**12
    # 3     14
    # 4     x
    num=int(hex(dr[4])+struct.pack('<H',dr[5]).encode('hex'),0)
    ndr[5] = SH_temp_conversion(num)

    # 6     11
    # 7     x
    num=int(hex(dr[7])+struct.pack('<H',dr[8]).encode('hex'),0)
    ndr[8] = dr[8] * 5000. / 2**16

    # 9     24
    # 10    x
    num=int(hex(dr[10])+struct.pack('<H',dr[11]).encode('hex'),0)
    ndr[11] = SH_temp_conversion(num)

    # 12    21
    # 13    x
    num=int(hex(dr[13])+struct.pack('<H',dr[14]).encode('hex'),0)
    ndr[14] = dr[14] * 5000. / 2**16

    # 15    34
    # 16    x
    num=int(hex(dr[16])+struct.pack('<H',dr[17]).encode('hex'),0)
    ndr[17] = SH_temp_conversion(num)

    # 18    31
    # 19    x
    num=int(hex(dr[19])+struct.pack('<H',dr[20]).encode('hex'),0)
    ndr[20] = dr[20] * 5000. / 2**16

    # 21    45
    # 22    x
    num=int(hex(dr[22])+struct.pack('<H',dr[23]).encode('hex'),0)
    ndr[23] = SH_humidity_conversion(num)

    # 24    55
    # 25    x
    num=int(hex(dr[25])+struct.pack('<H',dr[26]).encode('hex'),0)
    ndr[26] = SH_humidity_conversion(num)

    # 27    65
    # 28    x
    num=int(hex(dr[28])+struct.pack('<H',dr[29]).encode('hex'),0)
    ndr[29] = SH_humidity_conversion(num)

    # 30    75
    # 31    x
    num=int(hex(dr[31])+struct.pack('<H',dr[32]).encode('hex'),0)
    ndr[32] = SH_humidity_conversion(num)

    # 33    mo1
    # 34    mo2
    # 35    enc
    ndr[33] = dr[33]
    ndr[34] = dr[34]
    ndr[35] = dr[35] * 360. / 2**12

    # 36    13
    # 37    x
    num=int(hex(dr[37])+struct.pack('<H',dr[38]).encode('hex'),0)
    ndr[38] = dr[38] * 5000. / 2**16

    # 39    23
    # 40    x
    num=int(hex(dr[40])+struct.pack('<H',dr[41]).encode('hex'),0)
    ndr[41] = dr[41] * 5000. / 2**16

    # 42    33
    # 43    x
    num=int(hex(dr[43])+struct.pack('<H',dr[44]).encode('hex'),0)
    ndr[44] = dr[44] * 5000. / 2**16

    # 45    mo1
    # 46    mo2
    # 47    enc
    ndr[45] = dr[45]
    ndr[46] = dr[46]
    ndr[47] = dr[47] * 360. / 2**12

    # 48    11
    # 49    x
    num=int(hex(dr[49])+struct.pack('<H',dr[50]).encode('hex'),0)
    ndr[50] = dr[50] * 5000. / 2**16

    # 51    21
    # 52    x
    num=int(hex(dr[52])+struct.pack('<H',dr[53]).encode('hex'),0)
    ndr[53] = dr[53] * 5000. / 2**16

    # 54    31
    # 55    x
    num=int(hex(dr[55])+struct.pack('<H',dr[56]).encode('hex'),0)
    ndr[56] = dr[56] * 5000. / 2**16

    # 67    mo1
    # 58    mo2
    # 59    enc
    ndr[57] = dr[57]
    ndr[58] = dr[58]
    ndr[59] = dr[59] * 360. / 2**12

    # 60    15
    # 61    x
    num=int(hex(dr[61])+struct.pack('<H',dr[62]).encode('hex'),0)
    ndr[62] = SH_humidity_conversion(num)

    # 63    13
    # 64    x
    num=int(hex(dr[64])+struct.pack('<H',dr[65]).encode('hex'),0)
    ndr[65] = dr[65] * 5000. / 2**16

    # 66    25
    # 67    x
    num=int(hex(dr[67])+struct.pack('<H',dr[68]).encode('hex'),0)
    ndr[68] = SH_humidity_conversion(num)

    # 69    23
    # 70    x
    num=int(hex(dr[70])+struct.pack('<H',dr[71]).encode('hex'),0)
    ndr[71] = dr[71] * 5000. / 2**16

    # 72    35
    # 73    x
    num=int(hex(dr[73])+struct.pack('<H',dr[74]).encode('hex'),0)
    ndr[74] = SH_humidity_conversion(num)

    # 75    33
    # 76    x
    num=int(hex(dr[76])+struct.pack('<H',dr[77]).encode('hex'),0)
    ndr[77] = dr[77] * 5000. / 2**16

    # 78    44
    # 79    x
    num=int(hex(dr[79])+struct.pack('<H',dr[80]).encode('hex'),0)
    ndr[80] = SH_temp_conversion(num)

    # 81    54
    # 82    x
    num=int(hex(dr[82])+struct.pack('<H',dr[83]).encode('hex'),0)
    ndr[83] = SH_temp_conversion(num)

    # 84    64
    # 85    x
    num=int(hex(dr[85])+struct.pack('<H',dr[86]).encode('hex'),0)
    ndr[86] = SH_temp_conversion(num)

    # 87    74
    # 88    x
    num=int(hex(dr[88])+struct.pack('<H',dr[89]).encode('hex'),0)
    ndr[89] = SH_temp_conversion(num)

    # 90    mo1
    # 91    mo2
    # 92    enc
    ndr[90] = dr[90]
    ndr[91] = dr[91]
    ndr[92] = dr[92] * 360. / 2**12

    # 93    11
    # 94    x
    num=int(hex(dr[94])+struct.pack('<H',dr[95]).encode('hex'),0)
    ndr[95] = dr[95] * 5000. / 2**16

    # 96    21
    # 97    x
    num=int(hex(dr[97])+struct.pack('<H',dr[98]).encode('hex'),0)
    ndr[98] = dr[98] * 5000. / 2**16

    # 99    31
    # 100    x
    num=int(hex(dr[40])+struct.pack('<H',dr[100]).encode('hex'),0)
    ndr[101] = dr[101] * 5000. / 2**16

    # 102   mo1
    # 103   mo2
    # 104   enc
    ndr[102] = dr[102]
    ndr[103] = dr[103]
    ndr[104] = dr[104] * 360. / 2**12

    # 105    13
    # 106   x
    num=int(hex(dr[106])+struct.pack('<H',dr[107]).encode('hex'),0)
    ndr[107] = dr[107] * 5000. / 2**16

    # 108    23
    # 109    x
    num=int(hex(dr[109])+struct.pack('<H',dr[110]).encode('hex'),0)
    ndr[110] = dr[110] * 5000. / 2**16

    # 111    33
    # 112    x
    num=int(hex(dr[112])+struct.pack('<H',dr[13]).encode('hex'),0)
    ndr[113] = dr[113] * 5000. / 2**16

    ndr[114] = dr[114]
    ndr[115] = dr[115]
    ndr[116] = dr[116]
    ndr[117] = TAILSYMBC
    #dr[31] = file_index
    # dr[43] = convert_timestamp(dr[43])
    return ndr

  # current state machine
  # symb enc mo 14 11 24 21 34 31 45 55 65 75
  # symb enc mo 13 23 33
  # symb enc mo 11 21 31
  # symb enc mo 15 13 25 23 35 33 44 54 64 74
  # symb enc mo 11 21 31
  # symb enc mo 13 23 33
  # symb rIdx wIdx counter tailsymb

DAQ_FORMAT_LIST=["<2sHHLsBHsBHsBHsBHsBHsBHsBHsBHsBHsBH",
                   "2sHHLsBHsBHsBH",
                   "2sHHLsBHsBHsBH",
                   "2sHHLsBHsBHsBHsBHsBHsBHsBHsBHsBHsBH",
                   "2sHHLsBHsBHsBH",
                   "2sHHLsBHsBHsBH",
                   "2sHHL2s"
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

daq_fmt="".join(DAQ_FORMAT_LIST)
DAQ_BUFFER_SIZE= struct.calcsize(daq_fmt)

cal_fmt="".join(CAL_FORMAT_LIST)
CAL_BUFFER_SIZE= struct.calcsize(cal_fmt)

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
            # print pos_s

            if pos_s+DAQ_BUFFER_SIZE > file_size:
                break

            chunk=get_next_record(fh,file_size,pos_s,DAQ_BUFFER_SIZE)
            # timestamp=extract_timestamp(chunk)
            chunk=reject_artifacts(chunk)


            length=len(chunk)
            rec=struct.unpack(daq_fmt,chunk)
            # rec=reject_headers(rec)
            rec=remove_tuple(rec,'\xa6\xa5')
            rec=remove_tuple(rec,'\xa7\xa5')
            rec=apply_scaling(rec)

            # narray=db.get_data('select * from c1_7 where c1_7 != ""')
            # calib[0] = narray.average() #C1
            #
            # narray=db.get_data('select * from c1_8 where c1_8 != ""')
            # calib[1] = narray.average() #C2
            #
            # narray=db.get_data('select * from c1_9 where c1_9 != ""')
            # calib[0] = narray.average() #C3
            #
            # narray=db.get_data('select * from c1_a where c1_a != ""')
            # calib[0] = narray.average() #C4
            #
            #
            # # apply pressure conversion
            # calib=db.get_data()
            # pressure_conversion(calib,)

            
            timestamp=''
            rechash={}
            
            rechash.update({"mo1":rec[0], "mo2":rec[1], "encoder_counter":rec[2],
                            'c1_a4':rec[5], 'c1_a1':rec[8], 'c2_a4':rec[11], 'c2_a1':rec[14],
                           'c3_a4':rec[17], 'c3_a1':rec[20], 'c4_a5':rec[23], 'c5_a5':rec[26], 'c6_a5':rec[29],
                           'c7_a5':rec[32]})
            rechash.update({'file_index':file_index,  'packet_len':length})
            db.insert_dict("enc",rechash)
            db.commit()

            rechash={}
            rechash.update({"mo1":rec[33], "mo2":rec[34], 'encoder_counter':rec[35],
                            'c1_a3':rec[38], 'c2_a3':rec[41], 'c3_a3':rec[44]})
            rechash.update({'file_index':file_index, 'packet_len':length})
            db.insert_dict("enc",rechash)
            db.commit()

            rechash={}
            rechash.update({"mo1":rec[45], "mo2":rec[46], 'encoder_counter':rec[47],
                            'c1_a1':rec[50], 'c2_a1':rec[53], 'c3_a1':rec[56]})
            rechash.update({'file_index':file_index,  'packet_len':length})
            db.insert_dict("enc",rechash)
            db.commit()

            rechash={}
            rechash.update({"mo1":rec[57], "mo2":rec[58], 'encoder_counter':rec[59],
                            'c1_a5':rec[62], 'c1_a3':rec[65], 'c2_a5':rec[68], 'c2_a3':rec[71],
                           'c3_a5':rec[74], 'c3_a3':rec[77], 'c4_a4':rec[80], 'c5_a4':rec[83], 'c6_a4':rec[86],
                           'c7_a4':rec[89]})
            rechash.update({'file_index':file_index,  'packet_len':length})
            db.insert_dict("enc",rechash)
            db.commit()

            rechash={}
            rechash.update({"mo1":rec[90], "mo2":rec[91], 'encoder_counter':rec[92],
                            'c1_a1':rec[95], 'c2_a1':rec[98], 'c3_a1':rec[101]})
            rechash.update({'file_index':file_index,  'packet_len':length})
            db.insert_dict("enc",rechash)
            db.commit()

            rechash={}
            rechash.update({"mo1":rec[102], "mo2":rec[103], 'encoder_counter':rec[104],
                            'c1_a3':rec[107], 'c2_a3':rec[110], 'c3_a3':rec[113]})
            rechash.update({'file_index':file_index, 'packet_len':length})
            db.insert_dict("enc",rechash)
            db.commit()

            rechash={}
            rechash.update({'counter':rec[114], 'wIdx':rec[115], 'rIdx':rec[116], 'tailsymb':rec[117],
                            'timestamp':timestamp})
            rechash.update({'file_index':file_index, 'packet_len':length})
            db.insert_dict("enc",rechash)
            db.commit()

            if i % DB_COMMIT_INTERVAL == 0 and i > 0:
                # db.commit()
                print "commit %s" % i
                # update_progress()

        except Exception,e:
          print "read error: "+ str(e)

    print "records found %s" % i
    recdict=({})

import re

def extract_timestamp(dr):
    ""
    hex_dr=dr.encode("hex")
    # print hex_dr
    match_group= re.match(r'HEADER_TIMESTAMP(.*)TAIL_TIMESTAMP',hex_dr)

    dr=dr.decode("hex")

    return match_group.group()

def update_progress(widget,pos_now,total_size):
    # widget.display((pos_now / total_size) * 100)
    percent = (pos_now / total_size) * 100
    print percent
    if percent == 100:
        return True

main()