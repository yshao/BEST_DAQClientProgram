import binascii
import sys
import struct
from best.commonsqliteutils import *


def usage():
    print "Usage: daq_parse [options] file_directory"
    print "       Options:"
    print "         -v  Logger output on/off"
    print "         -d  File directory to read raw files"
    print "         -f  Individual file to parse"
    sys.exit(1)


TAILSYMBA="3A3A"
TAILSYMBB="3B3B"
DB_COMMIT_INTERVAL=5


def get_next_record(fh,file_size,start,estimate,margin=6):
    pos_s=start
    dr=fh.read(estimate - margin)

    while(pos_s+estimate < file_size):
        dr1=fh.read(2)
        hexsymb=dr1.encode("hex").upper()
        # print hexsymb

        dr=dr+dr1
        if hexsymb == TAILSYMBA or hexsymb == TAILSYMBB:
            #TODO: modify encoder firmware to be the same as rad
            # dr=dr+fh.read(4)
            break

    return dr

# clean off artifiacts
def reject_artifacts(dr):
    ""
    dr=dr.encode("hex")
    # print dr
    dr=dr.replace("e7e7","")
    # print dr
    dr=dr.decode("hex")

    return dr

# find the end of first header
def seek_until(fh,file_size):
  pre=0
  while (pre < file_size):
    bytes=fh.read(2).encode("hex").upper()
    # print bytes
    if bytes == TAILSYMBA or bytes == TAILSYMBB:
      break
    else:
      pre+=2

  return fh.tell()

#convert raw counts into proper numerical
def apply_scaling(dr):
    ndr  = [i for i in range(32)]
    ndr[0] = dr[0] * 5000. / 2**16
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
    ndr[11] = dr[11] * 5000. / 2**16
    # print dr[12]
    # ndr[12] = map( lambda x: {0x1234 : 1, 0x4444 : 2, }.get(x,100)  , [dr[12]])[0]
    print format(dr[12],'#04x')
    ndr[12]=format(dr[12],'#04x')[-3:-2]

    ndr[13] = dr[13] * 5000. / 2**16
    ndr[14] = dr[14] * 5000. / 2**16
    ndr[15] = dr[15] * 5000. / 2**16
    ndr[16] = dr[16] * 5000. / 2**16
    ndr[17] = dr[17] * 5000. / 2**16
    ndr[18] = dr[18] * 5000. / 2**16
    ndr[19] = dr[19] * 5000. / 2**16
    ndr[20] = dr[20] * 5000. / 2**16
    ndr[21] = dr[21] * 5000. / 2**16
    ndr[22] = dr[22] * 5000. / 2**16
    ndr[23] = dr[23] * 5000. / 2**16
    ndr[24] = dr[24] * 5000. / 2**16
    # print dr[25]
    # ndr[25] = map( lambda x: {0x1234 : 1, 0x4444 : 2}.get(x, 100), [dr[25]])[0]
    print format(dr[25],'#04x')
    ndr[25] = format(dr[25],'#04x')[-3:-2]

    ndr[26] = dr[26]
    ndr[27] = dr[27] * 5000. / 2**16
    ndr[28] = dr[28]
    ndr[29] = dr[29]
    ndr[30] = dr[30].encode("hex")

    #ndr[31] = convert_timestamp(dr[31])

    #ndr[31] = file_index


    return ndr


import csv

def convert_to_csv(db):
    # conn = sqlite3.connect(dbfile)
    # conn.text_factory = str ## my current (failed) attempt to resolve this
    cur = db.cursor()
    data = cur.execute("SELECT * FROM mytable")

    with open('output.csv', 'wb') as f:
        writer = csv.writer(f)
        # headers
        writer.writerow([
                         'ch1_1','ch1_2','ch1_3','ch1_4','ch1_5','ch1_6',',ch1_7',
                         'ch1_8','ch1_9','ch1_10','ch1_11','ch1_12','hKey_1',
                         'ch2_1','ch2_2','ch2_3','ch2_4','ch2_5','ch2_6',',ch2_7',
                         'ch2_8','ch2_9','ch2_10','ch2_11','ch2_12','hKey_2',
                         'counter','temp','rIdx','wIdx','tailsymb','file_index','timestamp'
                         ])
        #
        writer.writerows(data)

    # db.export_to_csv


fmt_list=['!HHHHHHHHHHHHH',
        'HHHHHHHHHHHHH',
        'LHHH2s']
# cols = ['ch1_1','ch2_1','ch3_1','ch4_1','ch5_1','ch6_1','ch7_1','ch8_1','ch9_1','ch10_1','ch11_1','ch12_1','hKey_1',
#         'ch1_2','ch2_2','ch3_2','ch4_2','ch5_2','ch6_2','ch7_2','ch8_2','ch9_2','ch10_2','ch11_2','ch12_2','hKey_2',
#         'counter','temp','wIdx','rIdx','tailsymb',
#         'file_index','timestamp']
fmt="".join(fmt_list)

DAQ_BUFFER_SIZE= struct.calcsize(fmt)

db=DaqDB("daq.db")

import best.commonconfigutils

config=Config("C:/Users/Ping/Workspace/DAQ/test/common/config.xml.")

def main():
  file_index = -1
  i=-1
  for file in np.sort(glob.glob(os.path.join(config.get("LOCAL_DIR"), '*.rad'))):
    file_index += 1

    file_size=os.stat(file).st_size
    print "Opening file %s size %s" % (file, file_size)

    with open(file,'rb') as fh:
      pos_s=seek_until(fh,file_size)


      eob=False
      i=0
      while(1):
        i += 1
        try:
            pos_s=fh.tell()
            # print pos_s

            if pos_s+DAQ_BUFFER_SIZE > file_size:
                break

            chunk=get_next_record(fh,file_size,pos_s,DAQ_BUFFER_SIZE)
            chunk=reject_artifacts(chunk)

            length=len(chunk)
            rec=struct.unpack(fmt,chunk)

            rec=apply_scaling(rec)

            ### add in processor info ###
            timestamp='_'
            rechash={}

            rechash.update({"ch1_1":rec[0], 'ch2_1':rec[1], 'ch3_1':rec[2], 'ch4_1':rec[3], 'ch5_1':rec[4],
                            'ch6_1':rec[5], 'ch7_1':rec[6], 'ch8_1':rec[7], 'ch9_1':rec[8], 'ch10_1':rec[9],
                            'ch11_1':rec[10], 'ch12_1':rec[11], 'hKey_1':rec[12]})
            # rechash.update({'file_index':file_index, 'timestamp':timestamp, 'packet_len':length})
            # db.insert_dict("rad",rechash)


            rechash.update({"ch1_2":rec[13], 'ch2_2':rec[14], 'ch3_2':rec[15], 'ch4_2':rec[16], 'ch5_2':rec[17],
                            'ch6_2':rec[18], 'ch7_2':rec[19], 'ch8_2':rec[20], 'ch9_2':rec[21], 'ch10_2':rec[22],
                            'ch11_2':rec[23], 'ch12_2':rec[24], 'hKey_2':rec[25]})
            # rechash.update({'file_index':file_index, 'timestamp':timestamp, 'packet_len':length})
            # db.insert_dict("rad",rechash)

            rechash.update({"counter":rec[26], 'temp':rec[27], 'rIdx':rec[28], 'wIdx':rec[29], 'tailsymb':rec[30]})
            rechash.update({'file_index':file_index, 'timestamp':timestamp, 'packet_len':length})

            #TODO: check to see if database is locked
            db.insert_dict("rad",rechash)

            if i % DB_COMMIT_INTERVAL == 0 and i > 0:
                db.commit()
                print "commit %s" % i

        except Exception,e:
          print "read error: "+ str(e)

    print "records found %s" % i
    # recdict=({})


  # convert_to_csv(db)

main()