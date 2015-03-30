import shutil
import numpy as np
import datetime
import struct
import os
from PyQt4.QtCore import pyqtSignal, SIGNAL, QThread
from common.sqliteutils import DaqDB
from common.env import Env

def unpackex(n,func):
    # print func(n).encode('hex')
    return int(func(n).encode('hex'),16)

def HI32(args):
    st= struct.pack('L',args)
    # print 'hl'
    # print st.encode('hex')
    # print 'h1'
    # print st[0:4].encode('hex')
    # print 'h1b'
    h2=st[0:1]
    h1=st[1:2]
    h4=st[2:3]
    h3=st[3:4]
    c= h1+h2+h3+h4
    # print c.encode('hex')
    # print st[4:8].encode('hex')+st[0:4].encode('hex')
    return c


def convert(rec):
    ""
    crec=[None] * 100
    crec[0]=hex(rec[0])
    crec[1]=hex(rec[1])
    crec[2]=hex(rec[2])

    return crec

class DecodeInuTask(QThread):
    signalNumOfRecords=pyqtSignal(int)
    signalCommit=pyqtSignal()

    HEADER_STAT="3D3D"
    HEADER_INU="FFFA"
    HEADER_GPS="FF01"
    HEADER_TIME="41374146"
    TAIL_TIME="41374246"

    DB_COMMIT_INTERVAL=500

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

    INU_FORMAT= [
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


    STAT_FORMAT= ['>2s',
               'LHH',
               '2s',
                ]

    STAT_TIME_FORMAT= [
               '>B',
               'BBBBBBBBBBBBBB',
               'B'
                ]

    inu_fmt="".join(INU_FORMAT)
    stat_fmt="".join(STAT_FORMAT)

    def calc_struct_size(self,lFormats):
        # lFormats=self.lFormat
        # print 'calc_struct'
        # print lFormats
        total=0
        for format in lFormats:
            # print "".join(format)
            total += struct.calcsize("".join(format))
        # print total
        return total

    def __del__(self):
        self.db.close()
        self.pdb.close()

    def __init__(self,recp):
        ""
        QThread.__init__(self)
        self.numRecords=0
        self.currBytes=0
        self.totalBytes=0
        self.currFile=""
        self.db=DaqDB(recp)
        self.pdb=DaqDB("../../common/daq.db")

        ### dataframe attrib ###
        self.INU_SIZE= self.calc_struct_size([self.INU_FORMAT])
        self.STAT_SIZE=self.calc_struct_size([self.STAT_FORMAT])
        self.STAT_TIME_SIZE=self.calc_struct_size([self.STAT_TIME_FORMAT])

        # self.connect(self,SIGNAL("task_decode()"),self.parse_inu,file)

    def commit(self):
        ""
        self.db.commit()
                        # self.numRecords=num_recs
                        # self.currBytess=
        # self.emit(SIGNAL("decoded_sets()"))
        self.signalCommit.emit()
        self.signalNumOfRecords.emit(self.numRecords)


    ### find valid header ###
    def seek_until(self,fh,start_pos):
      pre=start_pos
      while (pre < self.file_size):
        bytes1=fh.read(1).encode("hex").upper()
        bytes2=fh.read(1).encode("hex").upper()
        fh.seek(-1,1)

        if bytes1+bytes2 == self.HEADER_INU:
          fh.seek(-1,1)
          break
        if bytes1+bytes2 == self.HEADER_TIME:
          fh.seek(-1,1)
          break
        else:
          pre+=1

      return bytes1+bytes2,fh.tell()

    # Inu Version
    def get_next_record(self,fh,file_size,start,margin=4):
        pos=start

        # b=fh.read(1)
        dr=''
        ### while not exceeding file size
        while(pos < file_size):

            dr1=fh.read(1)
            dr2=fh.read(1)
            fh.seek(-1,1)
            hex1=dr1.encode("hex").upper()
            hex2=dr2.encode("hex").upper()

            dr=dr+dr1
            symb=hex1+hex2
            b=False

            # print readahead.encode('hex')
            if symb in self.HEADER_INU:

                fh.seek(-1,1)
                dr=fh.read(self.INU_SIZE)
                # b=True

                ### deal with legacy timestamp ###
                readahead=fh.read(2).encode('hex').upper()
                fh.seek(-2,1)
                # print readahead.encode('hex')
                if readahead == symb:
                    ""
                    b=True
                else:
                    ""
                    dr=dr+fh.read(12)
                    readahead2=fh.read(2).encode('hex').upper()
                    fh.seek(-2,1)
                    if readahead2 == symb:
                        b=True

            ### 3rd condition exists for extended data, toss for now
                # print dr.encode('hex'), len(dr),readahead,readahead2

            elif symb in self.HEADER_STAT:
                fh.seek(-1,1)
                dr=fh.read(self.STAT_SIZE)
                b=True
                # print 'stat'
                # print dr.encode('hex')
                # print len(dr)

            ### offset by 1 to prevent repetition in symb matching
            if b:
                if len(dr) in [self.INU_SIZE,self.STAT_SIZE,84]:

                    fh.seek(-1,1)
                    break

        ### frame size condition
        if symb == self.HEADER_INU:
            dr=dr
        elif symb == self.HEADER_STAT:
            # fh.seek(1,1)
            dr=dr
        # print recordType
        # return hex1+hex2,dr[:-1]
        return symb,dr


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

        # print idx
        # print idx2
        # print idx3
        # print idx4
        # print size
        # print self.STAT_TIME_SIZE*2
        # print ndr[idx +8:idx+8+self.STAT_TIME_SIZE*2]

        if size == self.STAT_TIME_SIZE*2:

            # print ndr
            # print ndr[idx3 +8:idx3+8+self.STAT_TIME_SIZE*2]
            statTime=ndr[idx3 +8:idx3+8+self.STAT_TIME_SIZE*2]

        ### remove sections ###
        nndr=ndr[0:idx]+ndr[idx2+4:idx3]+ndr[idx4+8:]


        statTime=statTime.decode('hex')
        stat=stat.decode('hex')
        nndr=nndr.decode('hex')
        return nndr,stat,statTime

    # remove legacy timestamp
    def extract_timestamp(self,dr):
        ndr=dr.encode('hex')
        i=ndr.find(self.HEADER_STAT.lower())

        ### byte is 0xhh###
        tm=ndr[i:i+24]
        data=ndr[:i]+ndr[i+24:]
        tm=tm.decode('hex')

        data=data.decode('hex')

        return data,tm

    # clean off artifiacts
    def reject_artifacts(self,dr):
        ""
        ndr=dr.encode("hex")
        ndr=ndr.replace("e7e7","")
        ndr=ndr.decode("hex")

        return ndr



    def commit_decoding_results(self):
        rec={}
        # rec.update({'fileName':self.file,'file_index':self.file_index,'fileSize':self.file_size,'recordsRejected':self.bad_recs,'recordsUploaded':self.num_recs})
        rec.update({'file_name':self.file,'file_index':self.file_index,'packet_len':self.file_size,'bIdx':self.num_recs})
        self.pdb.insert_dict('decoder',rec)
        self.pdb.commit()

    def parse_inu(self,file,file_index):
        ""

        self.file=file
        self.file_index=file_index
        self.file_size=os.stat(file).st_size
        print "Opening file %s size %s" % (file, self.file_size)

        with open(file,'rb') as fh:
          recordType,pos_s=self.seek_until(fh,0)

          self.num_recs=0
          self.bad_recs=0

          recBuffer=[]
          while(True):
            try:
                pos_s=fh.tell()
                self.file_pos=pos_s
                if pos_s+self.INU_SIZE > self.file_size:
                    break

                recordType,chunk=self.get_next_record(fh,self.file_size,pos_s)

                chunk=self.reject_artifacts(chunk)
                # print chunk.encode('hex')
                length=len(chunk)

                ### decoding ###
                ### toss unhandled frame size
                if length not in [self.INU_SIZE,self.STAT_SIZE,84]:
                    ### bad records
                    self.bad_recs += 1
                    rec={}
                    rec.update({'file_index':file_index,'file_name':file,'bIdx':pos_s,'packet_len':length})
                    self.db.insert_dict("decoder",rec)
                    self.pdb.commit()

                    self.seek_until(fh,pos_s)

                ### stats
                if length == self.STAT_SIZE:
                    ### good records
                    self.num_recs += 1
                    if recordType == self.HEADER_STAT:
                        recStats=struct.unpack(self.stat_fmt,chunk)


                    rechash={}
                    rechash.update({
                        'rIdx':recStats[2],'wIdx':recStats[3],'counter':recStats[1]
                    })

                    counter=unpackex(recStats[1],HI32)
                    rechash.update({'counter':counter})

                    rechash.update({'file_index':file_index,  'packet_len':length,'file_pos':self.file_pos})
                    # print rechash
                    recBuffer.append(rechash)
                ### data + stats
                elif length == self.INU_SIZE+self.STAT_SIZE:
                    # print length
                    ### good records
                    self.num_recs += 1

                    ### trasnform data ###
                    crec=convert(rec)

                    cData,cStats=self.extract_timestamp(chunk)

                    if len(cData) == self.INU_SIZE and len(cStats) == self.STAT_SIZE:
                        rec=struct.unpack(self.inu_fmt,cData)
                        recStats=struct.unpack(self.stat_fmt,cStats)

                        rechash={}
                        rechash.update({
                                'PRE':crec[0], 'BID':crec[1], 'MID':crec[2], 'LEN':rec[3],
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

                        rechash.update({
                            'rIdx':recStats[2],'wIdx':recStats[3],'counter':recStats[1]
                        })


                        ### new ###
                        counter=unpackex(recStats[1],HI32)
                        rechash.update({'counter':counter})


                        rechash.update({'file_index':file_index,  'packet_len':length,'file_pos':self.file_pos})
                        recBuffer.append(rechash)


                ### data
                # elif length == self.INU_SIZE:
                elif length == self.INU_SIZE:
                    ### good records
                    self.num_recs += 1

                    if recordType == self.HEADER_INU:
                        rec=struct.unpack(self.inu_fmt,chunk)
                        # print self.inu_fmt

                    ### trasnform data ###
                    crec=convert(rec)
                    ### add in processor info ###
                    timestamp=''
                    rechash={}

                    rechash.update({
                            'PRE':crec[0], 'BID':crec[1], 'MID':crec[2], 'LEN':hex(rec[3]),
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

                    rechash.update({'file_index':file_index,  'packet_len':length,'file_pos':self.file_pos})
                    recBuffer.append(rechash)

                ### commit interval ###
                if self.num_recs % self.DB_COMMIT_INTERVAL == 0 and self.num_recs > 0 :
                    # print recBuffer
                    for rec in recBuffer:
                        self.db.insert_dict("inu",rec)
                    print "commit %s" % self.num_recs
                    self.commit()

            except Exception,e:
                print "read error: ",str(Exception.__class__),str(e)
                # print self.STAT_SIZE
                # print self.INU_SIZE

        ### add decoding results
        self.commit_decoding_results()

    #convert raw counts into proper numerical
    def apply_scaling(self,dr):
        ""
        ndr  = [i for i in range(self.INU_SIZE)]
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
    # os.remove('../inu.db')
    # shutil.copy('../daq.db','../inu.db')
    # task=DecodeInuTask()
    # task.parse_inu("../client/data/20000101_000203.imu",0)

    filep="../client/data/20000101_000203.imu"
    name=os.path.splitext(os.path.basename(filep))[0]
    recp='%s/%s' % ('c:/datasets/buffer','%s.recI' % name)
    # os.remove('../enc.db')
    # shutil.copy('../daq.db','../enc.db')
    try:
        os.remove(recp)
    except:
        pass

    shutil.copy('../../common/daq.db',recp)

    task=DecodeInuTask(recp)
    # task.calc_struct_size()
    task.parse_inu(filep,0)

class DataUtils():
    def __init__(self,cfg,fdr):
        ""
        self.cfg=cfg



    def create_db_buffer(self):
        ""
    def decode_inu(self,filep,idx):
        ### create_buffer ###
        bufferp='%s/%sinu.db' (fdr,filen)
        cfg=Env().getConfig()
        homep=Env().getpath('HOME')
        dbp=homep+'/common/daq.db'
        shutil.copy(dbp,bufferp)
        task=DecodeInuTask()
        task.parse_inu(filep,idx)

