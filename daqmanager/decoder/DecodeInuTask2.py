import numpy as np
import datetime
import struct
import os
# from PyQt4.QtCore import pyqtSignal, SIGNAL, QThread
from common.sqliteutils import DaqDB

class DecodeInuTask():
    # signalNumOfRecords=pyqtSignal(int)
    # signalCommit=pyqtSignal()

    TAILSYMBD="3D3D"
    HEADER_INU="FFFA"
    HEADER_GPS="FF01"
    HEADER_TIME="41374146"
    TAIL_TIME="41374246"

    DB_COMMIT_INTERVAL=5

# GPS structure
#
#
#
#
#


# INU structure
#
#   PRE     byte        = FA        1
#   BID     byte        = FF        1
#   MID     byte        = 32        1
#   LEN     byte        = 43    = 67    1
#   DATA    26 bytes    =   accx accy accz magx magy magz gyrx gyry gryz
#                           temp
#                             2 2 2 2 2 2 2 2 2 2
# Press         - U2        2
# press stat    - U1        1
# ITOW          - U4        4

# LAT           - I4        4
# LON           - I4        4
# ALT           - I4        4
# VEL_N         - I4        4
# VEL_E         - I4        4
# VEL_D         - I4        4

# Hacc          - U4        4
# Vacc          - U4        4
# Sacc          - U4        4

# bGPS          - GPS       1
# TS            - U2        2

# Status    byte            1
#   CS      byte            1

    INU_FORMAT_LIST= [
               '<BBBB',
                'HHHHHHHHH',
                'H'
                'HBI',
                'iiiiii',
                'III',
                'BH'
                'B',
                'B',
                ]

    STAT_FORMAT_LIST= [
               '>LHH'
                ]

    STAT_TIME_FORMAT_LIST= [
               '>B',
               'BBBBBBBBBBBBBB',
               'B'
                ]

    inu_fmt="".join(INU_FORMAT_LIST)
    stat_fmt="".join(STAT_FORMAT_LIST)
    statTime_fmt="".join(STAT_TIME_FORMAT_LIST)
    DAQ_BUFFER_SIZE= struct.calcsize(inu_fmt)
    STAT_SIZE=struct.calcsize(stat_fmt)
    STAT_TIME_SIZE=struct.calcsize(statTime_fmt)
    # print STAT_TIME_SIZE

    def __del__(self):
        self.db.close()
        self.pdb.close()

    def __init__(self):
        ""
        # QThread.__init__(self)
        self.numRecords=0
        self.currBytes=0
        self.totalBytes=0
        self.currFile=""
        self.db=DaqDB("../inu.db")
        self.pdb=DaqDB("../daq.db")

        # self.db.dump_tables()

        # self.connect(self,SIGNAL("task_decode()"),self.parse_inu,file)

    def commit(self):
        ""
        self.db.commit()


    # find the end of first header
    def seek_until(self,fh,start_pos):
      pre=start_pos
      while (pre < self.file_size):
        bytes1=fh.read(1).encode("hex").upper()
        bytes2=fh.read(1).encode("hex").upper()
        fh.seek(-1,1)

        if bytes1+bytes2 == self.HEADER_INU:
          fh.seek(-1,1)
          break
        else:
          pre+=1

      return fh.tell()

    # Inu Version
    def get_next_record(self,fh,file_size,start,estimate,margin=6):
        pos=start
        dr=fh.read(estimate - margin)

        while(pos+estimate < file_size):

            dr1=fh.read(1)
            dr2=fh.read(1)
            fh.seek(-1,1)
            hex1=dr1.encode("hex").upper()
            hex2=dr2.encode("hex").upper()

            dr=dr+dr1

            if hex1+hex2 == self.HEADER_INU:
                fh.seek(-1,1)
                break

        return hex1+hex2,dr[:-1]

    def convert_timestamp(bytes,):
        timef=np.frombuffer(bytes, dtype=np.int16)
        date= datetime.datetime(timef[0],timef[1],timef[3],timef[4],timef[5],timef[6])
        return date

    def detect_symbol(self,df):
        ndr=df.encode('hex')

        ### detect stats ###
        idx=ndr.find(self.HEADER_INU)
        idx2=ndr.find(self.HEADER_INU,idx+4)
        stat=""
        size=idx2-idx-4

        if size == self.STAT_SIZE*2:
            stat=ndr[idx +4,idx+4+self.STAT_SIZE*2]

        ### detect time ###
        idx3=ndr.find(self.HEADER_TIME)
        idx4=ndr.find(self.TAIL_TIME,idx3+8)
        statTime=""
        size=idx4-idx3-8

        print idx
        print idx2
        print idx3
        print idx4
        print size
        print self.STAT_TIME_SIZE*2
        # print ndr[idx +8:idx+8+self.STAT_TIME_SIZE*2]
        if size == self.STAT_TIME_SIZE*2:
            print ndr
            print ndr[idx3 +8:idx3+8+self.STAT_TIME_SIZE*2]
            statTime=ndr[idx3 +8:idx3+8+self.STAT_TIME_SIZE*2]

        ### remove sections ###
        nndr=ndr[0:idx]+ndr[idx2+4:idx3]+ndr[idx4+8:]


        statTime=statTime.decode('hex')
        stat=stat.decode('hex')
        nndr=nndr.decode('hex')
        return nndr,stat,statTime


    # clean off artifiacts
    def reject_artifacts(self,dr):
        ""
        ndr=dr.encode("hex")
        ndr=ndr.replace("e7e7","")
        ndr=ndr.decode("hex")

        return ndr

    def commit_decoding_results(self):
        print 'commiting...'
        rec={}
        rec.update({'fileName':self.file,'file_index':self.file_index,'fileSize':self.file_size,'recordsRejected':self.bad_recs,'recordsUploaded':self.num_recs})
        self.pdb.insert_dict(rec)
        self.pdb.commit()

    def parse_inu(self,file,file_index):
        ""

        self.file_size=os.stat(file).st_size
        print "Opening file %s size %s" % (file, self.file_size)

        with open(file,'rb') as fh:
          pos_s=self.seek_until(fh,0)

          self.num_recs=0
          self.bad_recs=0

          while(True):
            try:
                pos_s=fh.tell()

                if pos_s+self.DAQ_BUFFER_SIZE > self.file_size:
                    break

                recordType,chunk=self.get_next_record(fh,self.file_size,pos_s,self.DAQ_BUFFER_SIZE)
                chunk=self.reject_artifacts(chunk)

                chunk,stat,statTime=self.detect_symbol(chunk)


                ### check chunk is valid

                length=len(chunk)
                if length != self.DAQ_BUFFER_SIZE:
                    self.bad_recs = self.bad_recs+1
                    rec={}
                    rec.update({'file_index':file_index,'file_name':file,'bIdx':pos_s,'packet_len':length})
                    self.db.insert_dict("decoder",rec)
                    self.pdb.commit()

                    self.seek_until(fh,pos_s)
                else:
                    print 'ending'
                    if recordType == self.HEADER_INU:
                        rec=struct.unpack(self.inu_fmt,chunk)

                    ### add in processor info ###
                    timestamp=''
                    rechash={}

                    rechash.update({
                            'PRE':rec[0], 'BID':rec[1], 'MID':rec[2], 'LEN':rec[3],
                            "accX":rec[4], "accY":rec[5], "accZ":rec[6],
                            'gyrX':rec[7], 'gyrY':rec[8], 'gyrZ':rec[9],
                            'magX':rec[10], 'magY':rec[11], 'magZ':rec[12],
                            'temp':rec[13],
                            'Press':rec[14],'bPrs':rec[15],'ITOW':rec[16],
                            'LAT':rec[17],'LON':rec[18],'ALT':rec[19],'VEL_N':rec[20],'VEL_E':rec[21],'VEL_D':rec[22],
                            'Hacc':rec[23],'Vacc':rec[24],'Sacc':rec[25],
                            'bGPS':rec[26],
                            'TS':rec[27],
                            'STATUS':rec[28],'CS':rec[29],
                            # 'tailsymb':rec[28]

                            })

                    if stat != "":
                        statrec=struct.unpack(self.stat_fmt,stat)
                        rechash.update({'counter':statrec[0],'wIdx':statrec[1],'rIdx':statrec[2]})

                    if statTime != "":
                        statTRec=struct.unpack(self.statTime_fmt,statTime)[2:]
                        timestamp=self.convert_time(statTRec)

                        rechash.update({'counter':timestamp})

                    rechash.update({'file_index':file_index,  'packet_len':length})
                    self.db.insert_dict("inu",rechash)

                    self.num_recs += 1

                    print 'pre commit'
                    if self.num_recs % self.DB_COMMIT_INTERVAL == 0 and self.num_recs > 0 :
                        print "commit %s" % self.num_recs
                        self.commit()

            except Exception,e:
              print "read error: "+ str(e)

        ### add decoding results
        self.commit_decoding_results()

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

        # print ndr
        return ndr


if __name__ == '__main__':
    task=DecodeInuTask()
    p='C:/datasets/03162015/archival_ip_192_168_38_46/20000101_000623.imu'
    task.parse_inu(p,0)

