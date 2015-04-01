import struct
import os
from PyQt4.QtCore import pyqtSignal, SIGNAL, QThread
import shutil
import sqlite3
from common.sqliteutils import DaqDB
from daqmanager.client.utils import tm_to_epoch


def H12(a):

    return struct.pack('L')

def H32(args):
    return struct.pack('L',args)

def H16(a):
    ""

def convert(rec):

    crec=[None] * 100

    counter=rec[88]
    crec[88]=unpackex(counter,H32)

    ### encoder
    for x in [0,17,32,35,38,41,44,61,76,79,82,85]:
        crec[x]=unpackex(rec[x],H32)

    ### sensor

    return crec

def unpackex(n,func):
    return int(func(n).encode('hex'),16)

class DecodeRadTask(QThread):
    # signalNumOfRecords=pyqtSignal(int)
    # signalCommit=pyqtSignal()

    TAILSYMBA="3A3A"
    TAILSYMBB="3B3B"
    DB_COMMIT_INTERVAL=500
    # cols = ['ch1_1','ch2_1','ch3_1','ch4_1','ch5_1','ch6_1','ch7_1','ch8_1','ch9_1','ch10_1','ch11_1','ch12_1','hKey_1',
    #         'ch1_2','ch2_2','ch3_2','ch4_2','ch5_2','ch6_2','ch7_2','ch8_2','ch9_2','ch10_2','ch11_2','ch12_2','hKey_2',
    #         'counter','temp','wIdx','rIdx','tailsymb']
    fmt_list_A=[ 'HHHHHHHHHHHH2s',
                 'HHHHHHHHHHHH2s',
                 'HHHHHHHHHHHH2s',
                 'HHHHHHHHHHHH2s',
                 'LHHH2s']

    # cols = ['ch1_1','ch2_1','ch3_1','ch4_1','ch5_1','ch6_1','ch7_1','ch8_1','ch9_1','ch10_1','ch11_1','ch12_1','tailsymb',
    #         'ch1_2','ch2_2','ch3_2','ch4_2','ch5_2','ch6_2','ch7_2','ch8_2','ch9_2','ch10_2','ch11_2','ch12_2','tailsymb',
    #         'counter','tailsymb','wIdx','rIdx','tailsymb']
    fmt_list_B=[ 'HHHHHHHHHHHH2s',
                 'HHHHHHHHHHHH2s',
                 'HHHHHHHHHHHH2s',
                 'HHHHHHHHHHHH2s',
                 'L2sHH2s']

    fmtA="".join(fmt_list_A)
    fmtB="".join(fmt_list_B)

    DAQ_BUFFER_SIZE= struct.calcsize(fmtA)  ### same size for both

    def __del__(self):
        ""
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

        # self.connect(self,SIGNAL("task_decode()"),self.parse_rad,file)

    def commit(self):
        ""
        self.db.commit()
                        # self.numRecords=num_recs
                        # self.currBytess=
        # self.emit(SIGNAL("decoded_sets()"))
        # self.signalCommit.emit("")
        # self.signalNumOfRecords.emit(self.numRecords)


    # find the end of first header
    def seek_until(self,fh,file_size,start_pos):
      pre=start_pos
      while (pre < file_size):
        bytes=fh.read(2).encode("hex").upper()
        # print bytes
        if bytes == self.TAILSYMBA or bytes == self.TAILSYMBB:
          break
        else:
          pre+=2

      return fh.tell()


    def get_next_record(self,fh,file_size,start,estimate,margin=6):
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

            ### found record
            if hexsymb == self.TAILSYMBA:
                # print len(dr)
                # if len(dr) > 20:
                # dr=dr+fh.read(4)
                    break
            elif hexsymb == self.TAILSYMBB:
                fh.seek(-8,1)
                byte=fh.read(2).encode('hex').upper()
                # print byte
                # print hex(fh.tell())
                # print dr.encode('hex')
                fh.read(6)
                if byte == self.TAILSYMBB:
                    # print byte
                    # fh.read(6)
                    break

        return hexsymb,dr

    # clean off artifiacts
    def reject_artifacts(self,dr):
        ""
        ndr=dr.encode("hex")

        ndr=ndr.replace("e7e7","")

        ndr=ndr.decode("hex")

        return ndr

    def parse_rad(self,file,file_index):
        ""
        file_size=os.stat(file).st_size
        print "Opening file %s size %s" % (file, file_size)
        #glog("Opening file %s size %s" % (file, file_size))

        with open(file,'rb') as fh:
          pos_s=self.seek_until(fh,file_size,0)

          # eob=False
          num_recs=0
          while(True):
            try:
                pos_s=fh.tell()
                self.file_pos=pos_s
                self.file_pos=hex(pos_s)

                ### break out
                if pos_s+self.DAQ_BUFFER_SIZE >= file_size:
                    # print 'HI'
                    break
                # print file_size - pos_s -16
                if file_size - pos_s - 16 < self.DAQ_BUFFER_SIZE:
                    break

                recordType,chunk=self.get_next_record(fh,file_size,pos_s,self.DAQ_BUFFER_SIZE)
                chunk=self.reject_artifacts(chunk)

                ### check chunk is valid
                length=len(chunk)
                if length != self.DAQ_BUFFER_SIZE:
                    self.seek_until(fh,file_size,pos_s)
                else:

                    if recordType == self.TAILSYMBB:
                        rec=struct.unpack(self.fmtB,chunk)
                    elif recordType == self.TAILSYMBA:
                        rec=struct.unpack(self.fmtA,chunk)

                    # rec=self.apply_scaling(rec)

                    ### add in processor info ###
                    timestamp='_'
                    rechash={}
                    if recordType == self.TAILSYMBA:
                        rechash.update({"ch1":rec[0], 'ch2':rec[1], 'ch3':rec[2], 'ch4':rec[3], 'ch5':rec[4],
                                        'ch6':rec[5], 'ch7':rec[6], 'ch8':rec[7], 'ch9':rec[8], 'ch10':rec[9],
                                        'ch11':rec[10], 'ch12':rec[11], 'hKey':rec[12]})
                        rechash.update({'file_pos':self.file_pos})
                        self.db.insert_dict("rad",rechash)

                        rechash.update({"ch1":rec[13], 'ch2':rec[14], 'ch3':rec[15], 'ch4':rec[16], 'ch5':rec[17],
                                        'ch6':rec[18], 'ch7':rec[19], 'ch8':rec[20], 'ch9':rec[21], 'ch10':rec[22],
                                        'ch11':rec[23], 'ch12':rec[24], 'hKey':rec[25]})
                        rechash.update({'file_pos':self.file_pos})
                        self.db.insert_dict("rad",rechash)

                        rechash.update({"ch1":rec[26], 'ch2':rec[27], 'ch3':rec[28], 'ch4':rec[29], 'ch5':rec[30],
                                        'ch6':rec[31], 'ch7':rec[32], 'ch8':rec[33], 'ch9':rec[34], 'ch10':rec[35],
                                        'ch11':rec[36], 'ch13':rec[37], 'hKey':rec[38]})
                        rechash.update({'file_pos':self.file_pos})
                        self.db.insert_dict("rad",rechash)

                        rechash.update({"ch1":rec[39], 'ch2':rec[40], 'ch3':rec[41], 'ch4':rec[42], 'ch5':rec[43],
                                        'ch6':rec[44], 'ch7':rec[45], 'ch8':rec[46], 'ch9':rec[47], 'ch10':rec[48],
                                        'ch11':rec[49], 'ch12':rec[50], 'hKey':rec[51]})
                        rechash.update({'file_pos':self.file_pos})
                        self.db.insert_dict("rad",rechash)

                        rechash.update({"counter":rec[52], 'temp':rec[53], 'rIdx':rec[54], 'wIdx':rec[55], 'tailsymb':rec[56]})
                        rechash.update({'file_index':file_index, 'timestamp':timestamp, 'packet_len':length, 'file_pos':self.file_pos})
                        self.db.insert_dict("rad",rechash)

                    elif recordType == self.TAILSYMBB:
                        rechash.update({"ch13":rec[0], 'ch14':rec[1], 'ch15':rec[2], 'ch16':rec[3], 'ch17':rec[4],
                                        'ch18':rec[5], 'ch19':rec[6], 'ch20':rec[7], 'ch21':rec[8], 'ch22':rec[9],
                                        'ch23':rec[10], 'ch24':rec[11], 'hKey':rec[12]})
                        rechash.update({'file_pos':self.file_pos})
                        self.db.insert_dict("rad",rechash)


                        rechash.update({"ch13":rec[13], 'ch14':rec[14], 'ch15':rec[15], 'ch16':rec[16], 'ch17':rec[17],
                                        'ch18':rec[18], 'ch19':rec[19], 'ch20':rec[20], 'ch21':rec[21], 'ch22':rec[22],
                                        'ch23':rec[23], 'ch24':rec[24], 'hKey':rec[25]})
                        rechash.update({'file_pos':self.file_pos})
                        self.db.insert_dict("rad",rechash)

                        rechash.update({"ch13":rec[26], 'ch14':rec[27], 'ch15':rec[28], 'ch16':rec[29], 'ch17':rec[30],
                                        'ch18':rec[31], 'ch19':rec[32], 'ch20':rec[33], 'ch21':rec[34], 'ch22':rec[35],
                                        'ch23':rec[36], 'ch24':rec[37], 'hKey':rec[38]})
                        rechash.update({'file_pos':self.file_pos})
                        self.db.insert_dict("rad",rechash)

                        rechash.update({"ch13":rec[39], 'ch14':rec[40], 'ch15':rec[41], 'ch16':rec[42], 'ch17':rec[43],
                                        'ch18':rec[44], 'ch19':rec[45], 'ch20':rec[46], 'ch21':rec[47], 'ch22':rec[48],
                                        'ch23':rec[49], 'ch24':rec[50], 'hKey':rec[51]})
                        rechash.update({'file_pos':self.file_pos})
                        self.db.insert_dict("rad",rechash)

                        rechash.update({"counter":rec[52], 'temp':rec[53], 'rIdx':rec[54], 'wIdx':rec[55], 'tailsymb':rec[56]})
                        rechash.update({'file_index':file_index, 'timestamp':timestamp, 'packet_len':length, 'file_pos':self.file_pos})
                        self.db.insert_dict("rad",rechash)

                    num_recs += 1

                    if num_recs % self.DB_COMMIT_INTERVAL == 0 and num_recs > 0 :
                        print "commit %s" % num_recs
                        self.db.commit()
                        # self.numRecords=num_recs
                        # self.currBytess=
                        # self.emit(SIGNAL("decoded_sets()"))


                # if i % DB_COMMIT_INTERVAL == 0 and i > 0:
                #     db.commit()
                #     print "commit %s" % i
                self.db.commit()


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


# EPOCH2000 = tm_to_epoch('20000101_000000','%Y%m%d_%H%M%S')
# name=os.path.splitext(os.path.basename(file))[0]
# tm=tm_to_epoch(name,'%Y%m%d_%H%M%S')
# tmFile=(tm - EPOCH2000) * 1000

if __name__ == '__main__':
    EPOCH2000 = tm_to_epoch('20000101_000000','%Y%m%d_%H%M%S')

    file="c:/datasets/1427841838/data/20000101_001333.rad"
    name=os.path.splitext(os.path.basename(file))[0]
    recp='%s/%s' % ('c:/datasets','%s.recR22' % name)
    print name
    ctime=os.stat(file).st_ctime
    mtime=os.stat(file).st_mtime
    tm=tm_to_epoch(name,'%Y%m%d_%H%M%S')
    tmFile=(tm - EPOCH2000) * 1000
    tmSt=ctime - EPOCH2000
    tmEnd=mtime - EPOCH2000

    print ctime, mtime, tm
    print EPOCH2000, tmSt,tmEnd,tmFile

    # try:
    #     os.remove(recp)
    # except:
    #     pass
    #
    # shutil.copy('../../common/daq.db',recp)
    #
    # task=DecodeRadTask(recp)
    #
    # task.parse_rad(file,0)
    # task.db.commit()
    # task.db.close()

    ### insert first stamp ###
    con = sqlite3.connect(recp)
    con.execute('update rad set counter=? where rowId=1',(tmFile,))
    con.commit()

    import numpy as np
    import pandas.io.sql as psql
    # con = sqlite3.connect(bufferp)
    with con:
        dr = psql.frame_query("SELECT counter  from rad", con)

    # s=pd.Series(dr)
    dr.fillna(np.nan)
    aTime=np.array(dr.interpolate())
    mlist=[(val[0],i+1) for i,val in enumerate(aTime)]

    con.executemany('UPDATE rad SET counter=? WHERE rowId=?', mlist)
    con.commit()