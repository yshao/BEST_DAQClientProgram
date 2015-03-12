import binascii
import sys
import struct
import os
from best.common.sqliteutils import DaqDB


# def usage():
#     print "Usage: daq_parse [options] file_directory"
#     print "       Options:"
#     print "         -v  Logger output on/off"
#     print "         -d  File directory to read raw files"
#     print "         -f  Individual file to parse"
#     sys.exit(1)


TAILSYMBA="3A3A"
TAILSYMBB="3B3B"
DB_COMMIT_INTERVAL=5

import struct

#1245427 = 0x1300f3
b= struct.pack('>I', 1245427)
print b.encode('hex')

c= struct.pack('<I', 1245427)
print c.encode('hex')




def get_next_record(fh,file_size,start,estimate,margin=6):
    pos_s=start
    dr=fh.read(estimate - margin)

    while(pos_s+estimate < file_size):
        dr1=fh.read(2)
        hexsymb=dr1.encode("hex").upper()

        ### found delineation page, skip entire page ###
        # 8A1A7A2A6A3A5A4A4A5A3A6A2A7A1A8A
        # or
        # 8B1B7B2B6B3B5B4B4B5B3B6B2B7B1B8B

        if hexsymb == "8A1A" or hexsymb == "8B1B":
            symb2=fh.read(2).encode("hex").upper()
            if symb2 == "7A2A" or symb2 == "7B2B":
                fh.read(6)


        else:
            dr=dr+dr1

        if hexsymb == TAILSYMBA or hexsymb == TAILSYMBB:
            # dr=dr+fh.read(4)
            break

    return hexsymb,dr

# clean off artifiacts
def reject_artifacts(dr):
    ""
    ndr=dr.encode("hex")
    print ndr
    ndr=codecs.encode(dr,'hex_codec')
    print ndr
    ndr=binascii.hexlify(dr)
    print ndr

    ndr=dr.encode()

    ndr=ndr.replace("e7e7","")

    print ndr
    ndr=ndr.decode("hex")

    print ndr
    print dr.encode("base64")

    return ndr

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

  # print fh.tell()
  return fh.tell()

#convert raw counts into proper numerical
def apply_scaling(dr):
    print dr
    ndr  = [i for i in range(DAQ_BUFFER_SIZE)]
    ndr[0] = dr[0]   * 2500. / 2**12
    ndr[1] = dr[1]   * 2500. / 2**12
    ndr[2] = dr[2]   * 2500. / 2**12
    ndr[3] = dr[3]   * 2500. / 2**12
    ndr[4] = dr[4]   * 2500. / 2**12
    ndr[5] = dr[5]   * 2500. / 2**12
    ndr[6] = dr[6]   * 2500. / 2**12
    ndr[7] = dr[7]   * 2500. / 2**12
    ndr[8] = dr[8]   * 2500. / 2**12
    ndr[9] = dr[9]   * 2500. / 2**12
    ndr[10] = dr[10] * 2500. / 2**12

    ndr[11] = dr[11] * 2500. / 2**12
    # ndr[12] = map( lambda x: {0x1234 : 1, 0x4444 : 2, }.get(x,100)  , [dr[12]])[0]
    print dr[0]
    print dr[10]
    print dr[11]
    # print dr[12].bit_length()
    print bin(dr[12])
    print dr[12]
    # print struct.unpack('B', ndr[12])
    # ndr[12] = int.from_bytes(dr[12],'little')



    # ndr[12] = ord(dr[12][1])

    ndr[13] = dr[13] * 2500. / 2**12
    ndr[14] = dr[14] * 2500. / 2**12
    ndr[15] = dr[15] * 2500. / 2**12
    ndr[16] = dr[16] * 2500. / 2**12
    ndr[17] = dr[17] * 2500. / 2**12
    ndr[18] = dr[18] * 2500. / 2**12
    ndr[19] = dr[19] * 2500. / 2**12
    ndr[20] = dr[20] * 2500. / 2**12
    ndr[21] = dr[21] * 2500. / 2**12
    ndr[22] = dr[22] * 2500. / 2**12
    ndr[23] = dr[23] * 2500. / 2**12
    ndr[24] = dr[24] * 2500. / 2**12

    # ndr[25] = map( lambda x: {0x1234 : 1, 0x4444 : 2}.get(x, 100), [dr[25]])[0]
    # print format(dr[25],'#04x')
    # ndr[25] = int(dr[25][2:4])
    ndr[25] = int.from_bytes(dr[25],'little')


    ndr[26] = dr[26] * 2500. / 2**12
    ndr[27] = dr[27] * 2500. / 2**12
    ndr[28] = dr[28] * 2500. / 2**12
    ndr[29] = dr[29] * 2500. / 2**12
    ndr[30] = dr[30] * 2500. / 2**12
    ndr[31] = dr[31] * 2500. / 2**12
    ndr[32] = dr[32] * 2500. / 2**12
    ndr[33] = dr[33] * 2500. / 2**12
    ndr[34] = dr[34] * 2500. / 2**12
    ndr[35] = dr[35] * 2500. / 2**12
    ndr[36] = dr[36] * 2500. / 2**12
    ndr[37] = dr[37] * 2500. / 2**12
    # print dr[25]
    # ndr[25] = map( lambda x: {0x1234 : 1, 0x4444 : 2}.get(x, 100), [dr[25]])[0]
    # print format(dr[25],'#04x')
    ndr[38] = int.from_bytes(dr[38],'little')

    ndr[39] = dr[39] * 2500. / 2**12
    ndr[40] = dr[40] * 2500. / 2**12
    ndr[41] = dr[41] * 2500. / 2**12
    ndr[42] = dr[42] * 2500. / 2**12
    ndr[43] = dr[43] * 2500. / 2**12
    ndr[44] = dr[44] * 2500. / 2**12
    ndr[45] = dr[45] * 2500. / 2**12
    ndr[46] = dr[46] * 2500. / 2**12
    ndr[47] = dr[47] * 2500. / 2**12
    ndr[48] = dr[48] * 2500. / 2**12
    ndr[49] = dr[49] * 2500. / 2**12
    ndr[50] = dr[50] * 2500. / 2**12
    # print dr[25]
    # ndr[25] = map( lambda x: {0x1234 : 1, 0x4444 : 2}.get(x, 100), [dr[25]])[0]
    # print format(dr[25],'#04x')
    ndr[51] = int.from_bytes(dr[51],'little')


    ndr[52] = dr[52]   # counter
    ndr[53] = dr[53] * 5000. / 2**16 #temp
    ndr[54] = dr[54]
    ndr[55] = dr[55]
    ndr[56] = dr[56].encode("hex")

    #ndr[31] = convert_timestamp(dr[31])

    #ndr[31] = file_index

    print ndr
    return ndr


# cols = ['ch1_1','ch2_1','ch3_1','ch4_1','ch5_1','ch6_1','ch7_1','ch8_1','ch9_1','ch10_1','ch11_1','ch12_1','hKey_1',
#         'ch1_2','ch2_2','ch3_2','ch4_2','ch5_2','ch6_2','ch7_2','ch8_2','ch9_2','ch10_2','ch11_2','ch12_2','hKey_2',
#         'counter','temp','wIdx','rIdx','tailsymb']
fmt_list_A=['<HHHHHHHHHHHH2s',
             'HHHHHHHHHHHH2s',
             'HHHHHHHHHHHH2s',
             'HHHHHHHHHHHH2s',
             'LHHH2s']

# cols = ['ch1_1','ch2_1','ch3_1','ch4_1','ch5_1','ch6_1','ch7_1','ch8_1','ch9_1','ch10_1','ch11_1','ch12_1','tailsymb',
#         'ch1_2','ch2_2','ch3_2','ch4_2','ch5_2','ch6_2','ch7_2','ch8_2','ch9_2','ch10_2','ch11_2','ch12_2','tailsymb',
#         'counter','tailsymb','wIdx','rIdx','tailsymb']
fmt_list_B=['<HHHHHHHHHHHH2s',
             'HHHHHHHHHHHH2s',
             'HHHHHHHHHHHH2s',
             'HHHHHHHHHHHH2s',
             'L2sHH2s']



fmtA="".join(fmt_list_A)
fmtB="".join(fmt_list_B)

DAQ_BUFFER_SIZE= struct.calcsize(fmtA)  ### same size for both

import codecs

numRecords=0
currBytes=0
totalBytes=0
def parse_rad(file,db,file_index):
    ""
    num_recs=-1

    file_size=os.stat(file).st_size
    print "Opening file %s size %s" % (file, file_size)
    #self.totalBytes=file_size
    # f=open(file,'r',enco)

    # print f.read(100)

    with open(file,'rb') as fh:
      pos_s=seek_until(fh,file_size)


      eob=False
      num_recs=0
      while(True):
        num_recs += 1
        try:
            pos_s=fh.tell()
            # print pos_s

            if pos_s+DAQ_BUFFER_SIZE > file_size:
                break

            recordType,chunk=get_next_record(fh,file_size,pos_s,DAQ_BUFFER_SIZE)
            chunk=reject_artifacts(chunk)

            length=len(chunk)
            if recordType == TAILSYMBB:
                rec=struct.unpack(fmtB,chunk)
            elif recordType == TAILSYMBA:
                rec=struct.unpack(fmtA,chunk)

            rec=apply_scaling(rec)

            ### add in processor info ###
            timestamp='_'
            rechash={}
            if recordType == TAILSYMBA:
                rechash.update({"ch1":rec[0], 'ch2':rec[1], 'ch3':rec[2], 'ch4':rec[3], 'ch5':rec[4],
                                'ch6':rec[5], 'ch7':rec[6], 'ch8':rec[7], 'ch9':rec[8], 'ch10':rec[9],
                                'ch11':rec[10], 'ch12':rec[11], 'hKey':rec[12]})
                db.insert_dict("rad",rechash)

                rechash.update({"ch1":rec[13], 'ch2':rec[14], 'ch3':rec[15], 'ch4':rec[16], 'ch5':rec[17],
                                'ch6':rec[18], 'ch7':rec[19], 'ch8':rec[20], 'ch9':rec[21], 'ch10':rec[22],
                                'ch11':rec[23], 'ch12':rec[24], 'hKey':rec[25]})
                db.insert_dict("rad",rechash)

                rechash.update({"ch1":rec[26], 'ch2':rec[27], 'ch3':rec[28], 'ch4':rec[29], 'ch5':rec[30],
                                'ch6':rec[31], 'ch7':rec[32], 'ch8':rec[33], 'ch9':rec[34], 'ch10':rec[35],
                                'ch11':rec[36], 'ch13':rec[37], 'hKey':rec[38]})
                db.insert_dict("rad",rechash)

                rechash.update({"ch1":rec[39], 'ch2':rec[40], 'ch3':rec[41], 'ch4':rec[42], 'ch5':rec[43],
                                'ch6':rec[44], 'ch7':rec[45], 'ch8':rec[46], 'ch9':rec[47], 'ch10':rec[48],
                                'ch11':rec[49], 'ch12':rec[50], 'hKey':rec[51]})
                # db.insert_dict("rad",rechash)

                rechash.update({"counter":rec[52], 'temp':rec[53], 'rIdx':rec[54], 'wIdx':rec[55], 'tailsymb':rec[56]})
                rechash.update({'file_index':file_index, 'timestamp':timestamp, 'packet_len':length})
                db.insert_dict("rad",rechash)

            elif recordType == TAILSYMBB:
                rechash.update({"ch13":rec[0], 'ch14':rec[1], 'ch15':rec[2], 'ch16':rec[3], 'ch17':rec[4],
                                'ch18':rec[5], 'ch19':rec[6], 'ch20':rec[7], 'ch21':rec[8], 'ch22':rec[9],
                                'ch23':rec[10], 'ch24':rec[11], 'hKey':rec[12]})
                db.insert_dict("rad",rechash)


                rechash.update({"ch13":rec[13], 'ch14':rec[14], 'ch15':rec[15], 'ch16':rec[16], 'ch17':rec[17],
                                'ch18':rec[18], 'ch19':rec[19], 'ch20':rec[20], 'ch21':rec[21], 'ch22':rec[22],
                                'ch23':rec[23], 'ch24':rec[24], 'hKey':rec[25]})
                db.insert_dict("rad",rechash)

                rechash.update({"ch13":rec[26], 'ch14':rec[27], 'ch15':rec[28], 'ch16':rec[29], 'ch17':rec[30],
                                'ch18':rec[31], 'ch19':rec[32], 'ch20':rec[33], 'ch21':rec[34], 'ch22':rec[35],
                                'ch23':rec[36], 'ch24':rec[37], 'hKey':rec[38]})
                db.insert_dict("rad",rechash)

                rechash.update({"ch13":rec[39], 'ch14':rec[40], 'ch15':rec[41], 'ch16':rec[42], 'ch17':rec[43],
                                'ch18':rec[44], 'ch19':rec[45], 'ch20':rec[46], 'ch21':rec[47], 'ch22':rec[48],
                                'ch23':rec[49], 'ch24':rec[50], 'hKey':rec[51]})
                db.insert_dict("rad",rechash)

                rechash.update({"counter":rec[52], 'temp':rec[53], 'rIdx':rec[54], 'wIdx':rec[55], 'tailsymb':rec[56]})
                rechash.update({'file_index':file_index, 'timestamp':timestamp, 'packet_len':length})
                db.insert_dict("rad",rechash)


            if num_recs % DB_COMMIT_INTERVAL == 0 and num_recs > 0 :
                print "commit %s" % num_recs
                db.commit()
                # self.numRecords=num_recs
                # self.currBytess=


            # if i % DB_COMMIT_INTERVAL == 0 and i > 0:
            #     db.commit()
            #     print "commit %s" % i

        except Exception,e:
          print "read error: "+ str(e)

    # if signal != None:
    #     ""
    # else:
    #     print "records found %s" % i
    # recdict=({})


### test one file parse ###

# for file in np.
folder="data/single"
folder="data/multi"

db=DaqDB("daq.db")

file="data/single/rawrad.rad"
idx=0
parse_rad(file,db,idx)



### test multifile parse ###
# folder="data/multi"
# for idx,file in enumerate(np.sort(glob.glob(os.path.join(folder, '*.rad')))):
#
#     if parse_rad(file,db,signal=PBar)


