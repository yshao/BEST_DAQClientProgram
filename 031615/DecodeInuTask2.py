import binascii
import sys
import struct
import os
from PyQt4.QtCore import pyqtSignal, SIGNAL, QThread
from best.common.sqliteutils import DaqDB

class DecodeInuTask(QThread):
    signalNumOfRecords=pyqtSignal(int)
    signalCommit=pyqtSignal()

    TAILSYMBD="3D3D"
    HEADER_INU="FFAF"

    DB_COMMIT_INTERVAL=5
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
    INU_FORMAT_LIST= [
               '>BBBB',
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

    def __init__(self):
        ""
        self.numRecords=0
        self.currBytes=0
        self.totalBytes=0
        self.currFile=""
        self.db=DaqDB("inu.db")

        self.connect(self,SIGNAL("task_decode()"),self.parse_inu,file)

    def commit(self):
        ""
        self.db.commit()
                        # self.numRecords=num_recs
                        # self.currBytess=
        # self.emit(SIGNAL("decoded_sets()"))
        self.signalCommit.emit("")
        self.signalNumOfRecords.emit(self.numRecords)


    # find the end of first header
    def seek_until(self,fh,file_size,start_pos):
      pre=start_pos
      while (pre < file_size):
        bytes=fh.read(2).encode("hex").upper()

        if bytes == self.TAILSYMBD:
          break
        else:
          pre+=2

      return fh.tell()

    # Inu Version
    def get_next_record(self,fh,file_size,start,estimate,margin=6):
        pos=start
        dr=fh.read(estimate - margin)

        while(pos+estimate < file_size):
            dr1=fh.read(2)
            hexsymb=dr1.encode("hex").upper()

            dr=dr+dr1
            if hexsymb == self.TAILSYMBD:
                pos=fh.tell()

                stat=fh.read(8)
                if stat[-2:-1] == self.TAILSYMBD:
                    dr=dr+stat
                    break
                else:
                    fh.seek(pos)

        return hexsymb,dr

    def get_inu_records(self,df,ldr):
        pos=0
        dr=ldr
        ndr=list()

        size=len(df)

        with io.BinaryIO(df) as sh:
            while pos+ self.DAQ_BUFFER_SIZE < size:
                dr1=sh.read(2)
                hexsymb=dr1.encode("hex").upper()

                dr=dr+dr1
                if hexsymb == self.TAILSYMBD:
                    pos=sh.tell()
                    stat=sh.read(68)

                    if stat[-2:-1] == self.HEADER_INU:
                        ndr.append(stat)
                        dr=None
                        sh.seek(pos-2)

                    else:
                        sh.seek(pos)

            dr=dr+sh.read(size-pos)

        return ndr,dr


    # clean off artifiacts
    def reject_artifacts(self,dr):
        ""
        ndr=dr.encode("hex")
        ndr=ndr.replace("e7e7","")
        ndr=ndr.decode("hex")

        return ndr

    def parse_inu(self,file,db,file_index):
        ""
        file_size=os.stat(file).st_size
        print "Opening file %s size %s" % (file, file_size)
        ldr=None
        with open(file,'rb') as fh:
          pos_s=self.seek_until(fh,file_size,0)

          num_recs=0
          while(True):
            num_recs += 1
            try:
                pos_s=fh.tell()

                if pos_s+self.DAQ_BUFFER_SIZE > file_size:
                    break

                recordType,chunk=self.get_next_record(fh,file_size,pos_s,self.DAQ_BUFFER_SIZE)
                chunk=self.reject_artifacts(chunk)

                nrec,ldr=self.get_inu_records(chunk,ldr)

                ### check chunk is valid

                for rec in nrec:
                    length=len(rec)
                    if length != self.DAQ_BUFFER_SIZE:
                        self.seek_until(fh,file_size,pos_s)
                    else:
                        if recordType == self.TAILSYMBD:
                            rec=struct.unpack(self.inu_fmt,chunk)


                        # rec=self.apply_scaling(rec)

                        ### add in processor info ###
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


                        if num_recs % self.DB_COMMIT_INTERVAL == 0 and num_recs > 0 :
                            print "commit %s" % num_recs
                            self.commit()

            except Exception,e:
              print "read error: "+ str(e)


    #convert raw counts into proper numerical
    def apply_scaling(self,dr):
        ""
        ndr  = [i for i in range(self.DAQ_BUFFER_SIZE)]
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
        # print dr[0]
        # print dr[10]
        # print dr[11]
        # print dr[12].bit_length()
        # print bin(dr[12])
        # print dr[12]
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
        # ndr[25] = int.from_bytes(dr[25],'little')


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
        # ndr[38] = int.from_bytes(dr[38],'little')

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
        # ndr[51] = int.from_bytes(dr[51],'little')


        ndr[52] = dr[52]   # counter
        ndr[53] = dr[53] * 5000. / 2**16 #temp
        ndr[54] = dr[54]
        ndr[55] = dr[55]
        ndr[56] = dr[56].encode("hex")

        #ndr[31] = convert_timestamp(dr[31])

        #ndr[31] = file_index

        print ndr
        return ndr


if __name__ == '__main__':
    task=DecodeInuTask()
    task.parse_inu("data/20000101_000157.imu",0)

import io