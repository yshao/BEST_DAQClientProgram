import binascii
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


TAILSYMB="A5A5"


def get_next_record(fh,file_size,start,symb,estimate,margin=6):
    # hexsymb= ''.join(chr(int(TAILSYMB[i:i+2], 16)) for i in range(0, len(TAILSYMB), 2))

    pos_s=fh.tell()
    dr=fh.read(estimate - margin)

    while(pos_s+estimate < file_size):
        dr1=fh.read(2)
        hexsymb=dr1.encode("hex").upper()
        # print hexsymb

        dr=dr+dr1
        if TAILSYMB == hexsymb:
            # TODO: change firmware then change this tailsymb
            dr=dr+fh.read(4)

            break
        # else:
            # ### filter E7E7
            # if hexsymb == 0xE7E7:
            #     "buffer empty"
            # elif hexsymb == 0xA5A7:
            #     "encoder"
            # elif hexsymb == 0xA5A6:
            #     "status"
            # elif hexsymb == 0xA5A5:
            #     "tailsymbol"
            #
            # else:
            #     dr=dr+dr1

    return dr

import base64

def reject_artifacts(dr):
    ""
    print dr
    print dr.encode("hex")
    dr=dr.encode("hex")
    dr=dr.replace("e7e7","")
    print dr
    dr=dr.decode("hex")
    print dr

    return dr



#convert raw counts into proper numerical
def apply_scaling(dr):
    ""
    dr[0] = dr[0] * 360. / 2^31
    dr[1] = dr[1] * 5000. / 2^15
    dr[2] = dr[2] * 5000. / 2^15
    dr[3] = dr[3] * 5000. / 2^15
    dr[4] = dr[4] * 5000. / 2^15
    dr[5] = dr[5] * 5000. / 2^15
    dr[6] = dr[6] * 5000. / 2^15
    dr[7] = dr[7] * 5000. / 2^15
    dr[8] = dr[8] * 5000. / 2^15
    dr[9] = dr[9] * 5000. / 2^15
    dr[10] = dr[10] * 5000. / 2^15

    dr[11] = dr[11] * 5000. / 2^31
    dr[12] = dr[11] * 5000. / 2^15
    dr[13] = dr[13] * 5000. / 2^15
    dr[14] = dr[14] * 5000. / 2^15

    dr[15] = dr[15] * 5000. / 2^31
    dr[16] = dr[16] * 5000. / 2^15
    dr[17] = dr[17] * 5000. / 2^15
    dr[18] = dr[18] * 5000. / 2^15

    dr[19] = dr[19] * 5000. / 2^31
    dr[20] = dr[20] * 5000. / 2^15
    dr[21] = dr[21] * 5000. / 2^15
    dr[22] = dr[22] * 5000. / 2^15
    dr[23] = dr[23] * 5000. / 2^15
    dr[24] = dr[24] * 5000. / 2^15
    dr[25] = dr[25] * 5000. / 2^15
    dr[26] = dr[26] * 5000. / 2^15
    dr[27] = dr[27] * 5000. / 2^15
    dr[28] = dr[28] * 5000. / 2^15
    dr[29] = dr[29] * 5000. / 2^15

    dr[30] = dr[30] * 5000. / 2^31
    dr[31] = dr[31] * 5000. / 2^15
    dr[32] = dr[32] * 5000. / 2^15
    dr[33] = dr[33] * 5000. / 2^15

    dr[34] = dr[34] * 5000. / 2^31
    dr[35] = dr[35] * 5000. / 2^15
    dr[36] = dr[36] * 5000. / 2^15
    dr[37] = dr[37] * 5000. / 2^15

    dr[38] = dr[38] * 5000. / 2^15
    dr[39] = dr[39] * 5000. / 2^15
    dr[40] = dr[40] * 5000. / 2^31

    #dr[30] = TAILBYM

    #dr[31] = file_index
    dr[43] = convert_timestamp(dr[43])

    return dr


def main():
  db=DaqDB("daq.db")

  # find first header
  DB_COMMIT_INTERVAL=50

  # STATE MACHINE DAQ
  DAQ_BUFFER_SIZE=208
  # DAQ_FORMAT_LIST=["<HH2sHHHHH",
  #           "HHHHHHHH",
  #           "HHHHHHHH",
  #           "H2sHHHHHH",
  #           "HHHH2sHHH",
  #           "HHHHHHHH",
  #           "HHHH2sHHH",
  #           "HHHHHHHH",
  #           "HHHHHHHH",
  #           "HHH2sHHHH",
  #           "HHHH2sHHH",
  #           "HHHHHHHH",
  #           "HHHH2sHH2s"]

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
  CAL_BUFFER_SIZE=208
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

  ### does not correspond to stat machine
  cols = ['c1_a1','c1_a3','c1_a4','c1_a5','c1_a6','c1_a7','c1_a8','c1_a9','c1_aA','c1_aD','c1_aE','c1_aF',
          'c2_a1','c2_a3','c2_a4','c2_a5','c2_a6','c2_a7','c2_a8','c2_a9','c2_aA','c2_aD','c2_aE','c2_aF',
          'c3_a1','c3_a3','c3_a4','c3_a5','c3_a6','c3_a7','c3_a8','c3_a9','c3_aA',
          'c4_a4','c4_a3','c4_aE','c4_a5',                'c4_a8','c4_a9',                        'c4_aF',
          'c5_a5',        'c5_aE',                                                'c5_aD',
          'c6_a5','c6_a4','c6_aE',                                                'c6_aD',
          'c7_a4','c7_a5','c7_aE',                                                'c7_aD',
          'encoder_counter','motor_out','counter','wIdx','rIdx','tailsymb',
          'file_index','timestamp','packet_len'
            ]
  fmt="".join(DAQ_FORMAT_LIST)

  print struct.calcsize(fmt)
  file_index=-1
  i=-1
  for file in np.sort(glob.glob(os.path.join("data", '*.enc'))):
    file_index += 1

    file_size=os.stat(file).st_size
    print "Opening file %s size %s" % (file, file_size)

    with open(file,'rb') as fh:
      # get to header
      eob=False
      i=0
      while(1):
        i += 1
        try:
            pos_s=fh.tell()

            if pos_s+DAQ_BUFFER_SIZE > file_size:
                break

            chunk=get_next_record(fh,file_size,pos_s,TAILSYMB,DAQ_BUFFER_SIZE)

            cleaned_chunk=reject_artifacts(chunk)
            # pos_s=fh.tell()
            # pos_e= (i+1)*DAQ_BUFFER_SIZE
            # print pos_s,"-",pos_e,"-"
            # if pos_e > os.stat(file).st_size:
            #     num_bytes= os.stat(file).st_size - pos_s
            #     eob=True
            #
            #     chunk=fh.read(num_bytes)
            # else:
            #     chunk=fh.read(DAQ_BUFFER_SIZE)

            length=len(cleaned_chunk)
            rec=struct.unpack(fmt,cleaned_chunk)
            ### add in processor info ###
            rec = rec + (file_index,)
            rec = rec + ("_",)
            rec = rec + (length,)
            print rec
            print rec[0]
            print rec[1]

            timestamp='_'

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


            if i % DB_COMMIT_INTERVAL == 0:
                db.commit()



        except Exception,e:
          print "read error: "+ str(e)

        print "records found %s" % i


main()