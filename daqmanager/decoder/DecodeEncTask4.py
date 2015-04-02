import struct
import os
from PyQt4.QtCore import pyqtSignal, SIGNAL, QThread
import shutil
import array
from common.env import Env
from common.sqliteutils import DaqDB
import itertools
from datautils import *

def hex_to_int32(data):
    return unpackex(data,H32)

def unpackex(n,func):
    return int(func(n).encode('hex'),16)

def H12(a):
    return struct.pack()

def H24(args):
    # print args
    # print struct.pack('L',args)
    return struct.pack('L',args)
    # print struct.pack(args)

def H32(args):
    # print args
    return struct.pack('L',args)


def H16(a):
    return struct.pack('')

class DecodeEncTask(QThread):
    # QThread.__init__(self)
    signalNumOfRecords=pyqtSignal(int)
    signalCommit=pyqtSignal()

    TAILSYMBC="3C3C"

    DB_COMMIT_INTERVAL=5

    # 1000 = enc mo1 mo2 counter rIdx wIdx
    # each row = 100 ms, each col = 10 ms
    #
    # total state machine time = 540ms
    # current state machine
    #   1000 15 25 35 45 55 65 85
    #   1000
    #   1000
    #   1000
    #   1000 14 24 34 44 54 64 84
    #   1000
    #   1000
    #   1000
    #   1000 12 22 32 42 52 62
    #   1000
    #   1000
    #   1000
    #   1000 16 26 36 46 56 66
    #   1000

    #   1000
    #   1000
    #   1000
    #   1000
    #   1000 12 22 32 42 52 62
    #   1000
    #   1000
    #   1000
    #   1000 16 26 36 46 56 66
    #   1000

    #   1000
    #   1000
    #   1000
    #   1000
    #   1000 12 22 32 42 52 62
    #   1000
    #   1000
    #   1000
    #   1000 16 26 36 46 56 66
    #   1000

    #   1000
    #   1000
    #   1000
    #   1000
    #   1000 12 22 32 42 52 62
    #   1000
    #   1000
    #   1000
    #   1000 16 26 36 46 56 66
    #   1000

    #   1000
    #   1000
    #   1000
    #   1000
    #   1000 12 22 32 42 52 62
    #   1000
    #   1000
    #   1000
    #   1000 16 26 36 46 56 66
    #   1000

    #   rIdx wIdx counter 3C3C

    DAQ_FORMAT_LIST=[ ">LHHHHL","sHBsHBsHBsHBsHBsHBsHB",
                       "LHHHHL",
                       "LHHHHL",
                       "LHHHHL",
                       "LHHHHL","sHBsHBsHBsHBsHBsHBsHB",
                       "LHHHHL",
                       "LHHHHL",
                       "LHHHHL",
                       "LHHHHL","sHBsHBsHBsHBsHBsHB",
                       "LHHHHL",
                       "LHHHHL",
                       "LHHHHL",
                       "LHHHHL","sHBsHBsHBsHBsHBsHB",
                       "LHHHHL",

                       "LHHHHL",
                       "LHHHHL",
                       "LHHHHL",
                       "LHHHHL",
                       "LHHHHL","sHBsHBsHBsHBsHBsHB",
                       "LHHHHL",
                       "LHHHHL",
                       "LHHHHL",
                       "LHHHHL","sHBsHBsHBsHBsHBsHB",
                       "LHHHHL",

                       "LHHHHL",
                       "LHHHHL",
                       "LHHHHL",
                       "LHHHHL",
                       "LHHHHL","sHBsHBsHBsHBsHBsHB",
                       "LHHHHL",
                       "LHHHHL",
                       "LHHHHL",
                       "LHHHHL","sHBsHBsHBsHBsHBsHB",
                       "LHHHHL",

                       "LHHHHL",
                       "LHHHHL",
                       "LHHHHL",
                       "LHHHHL",
                       "LHHHHL","sHBsHBsHBsHBsHBsHB",
                       "LHHHHL",
                       "LHHHHL",
                       "LHHHHL",
                       "LHHHHL","sHBsHBsHBsHBsHBsHB",
                       "LHHHHL",

                       "LHHHHL",
                       "LHHHHL",
                       "LHHHHL",
                       "LHHHHL",
                       "LHHHHL","sHBsHBsHBsHBsHBsHB",
                       "LHHHHL",
                       "LHHHHL",
                       "LHHHHL",
                       "LHHHHL","sHBsHBsHBsHBsHBsHB",
                       "LHHHHL",

                       "HHL2s",
                ]


    # STATE MACHINE CALIB
    CAL_FORMAT_LIST=[">2sHHHHH",
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


    # def calc_struct_size(self):
    #     lFormats=self.lFormat
    #     total=0
    #     for format in lFormats:
    #         total += struct.calcsize("".join(format))
    #     print total

    def __del__(self):
        ""
        # self.db.close(self)

    def __init__(self,recp):
        ""
        QThread.__init__(self)
        self.numRecords=0
        self.currBytes=0
        self.totalBytes=0
        self.currFile=""
        self.db=DaqDB(recp)
        self.pdb=DaqDB("../../common/daq.db")
        
        # self.connect(self,SIGNAL("task_decode()"),self.parse_enc,file)

    def getDB(self):
        return self.db

    def commit(self):
        ""
        self.db.commit()
                        # self.numRecords=num_recs
                        # self.currBytess=
        # self.emit(SIGNAL("decoded_sets()"))
        # self.signalCommit.emit()
        # self.signalNumOfRecords.emit(self.numRecords)


    # find the end of first header
    def seek_until(self,fh,file_size,start_pos):
      pre=start_pos
      while (pre < file_size):
        bytes=fh.read(2).encode("hex").upper()

        if bytes == self.TAILSYMBC:
          break
        else:
          pre+=2

      return fh.tell()


    def get_next_record(self,fh,file_size,start,estimate,margin=6):
        pos_s=start
        dr=fh.read(estimate - margin)

        while(pos_s+estimate <= file_size):

            dr1=fh.read(2)
            hexsymb=dr1.encode("hex").upper()

            dr=dr+dr1
            pos=fh.tell()
            if hexsymb == self.TAILSYMBC:
                break

        return hexsymb,dr

    # clean off artifiacts
    def reject_artifacts(self,dr):
        ""
        ndr=dr.encode("hex")
        ndr=ndr.replace("e7e7","")
        # print ndr
        # print len(ndr)
        #
        # a=ndr[0:424]
        # b=ndr[896:920]
        # disgard=ndr[424:1246]
        #
        # c= a+b
        # print c
        ndr=ndr.decode("hex")


        return ndr

    def remove_tuple(self,original_tuple, element_to_remove):
        new_tuple = []
        for s in list(original_tuple):
            if not s == element_to_remove:
                new_tuple.append(s)
        return tuple(new_tuple)

    def convert_resolution(self,dr):
        ""
        ndr=list()
        cdr = itertools.chain(dr)



    # 1000 = enc mo1 mo2 counter rIdx wIdx
    # each row = 100 ms, each col = 10 ms
    #
    # total state machine time = 540ms
    # current state machine
    #   1000 15 25 35 45 55 65 85
    #   1000
    #   1000
    #   1000
    #   1000 14 24 34 44 54 64 84
    #   1000
    #   1000
    #   1000
    #   1000 12 22 32 42 52 62
    #   1000
    #   1000
    #   1000
    #   1000 16 26 36 46 56 66
    #   1000

    #   1000
    #   1000
    #   1000
    #   1000
    #   1000 12 22 32 42 52 62
    #   1000
    #   1000
    #   1000
    #   1000 16 26 36 46 56 66
    #   1000

    #   1000
    #   1000
    #   1000
    #   1000
    #   1000 12 22 32 42 52 62
    #   1000
    #   1000
    #   1000
    #   1000 16 26 36 46 56 66
    #   1000

    #   1000
    #   1000
    #   1000
    #   1000
    #   1000 12 22 32 42 52 62
    #   1000
    #   1000
    #   1000
    #   1000 16 26 36 46 56 66
    #   1000

    #   1000
    #   1000
    #   1000
    #   1000
    #   1000 12 22 32 42 52 62
    #   1000
    #   1000
    #   1000
    #   1000 16 26 36 46 56 66
    #   1000

    #   rIdx wIdx counter 3C3C

    #   hum values are 12bit
    #   pres values are 24bit
    # 2 - temp
    # 6 - pres
    #
    # 4 - temp
    # 5 - hum

        ndr.append(hex_to_int32(cdr.next()));ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(hex_to_int32(cdr.next()));
        ndr.append(cdr.next());ndr.append(hex_to_int11([cdr.next(),cdr.next()]))
        ndr.append(cdr.next());ndr.append(hex_to_int11([cdr.next(),cdr.next()]))
        ndr.append(cdr.next());ndr.append(hex_to_int11([cdr.next(),cdr.next()]))
        ndr.append(cdr.next());ndr.append(hex_to_int11([cdr.next(),cdr.next()]))
        ndr.append(cdr.next());ndr.append(hex_to_int11([cdr.next(),cdr.next()]))
        ndr.append(cdr.next());ndr.append(hex_to_int11([cdr.next(),cdr.next()]))
        ndr.append(cdr.next());ndr.append(hex_to_int11([cdr.next(),cdr.next()]))

        ndr.append(hex_to_int32(cdr.next()));ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(hex_to_int32(cdr.next()));
        ndr.append(hex_to_int32(cdr.next()));ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(hex_to_int32(cdr.next()));
        ndr.append(hex_to_int32(cdr.next()));ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(hex_to_int32(cdr.next()));

        ndr.append(hex_to_int32(cdr.next()));ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(hex_to_int32(cdr.next()));
        ndr.append(cdr.next());ndr.append(hex_to_int11([cdr.next(),cdr.next()]))
        ndr.append(cdr.next());ndr.append(hex_to_int11([cdr.next(),cdr.next()]))
        ndr.append(cdr.next());ndr.append(hex_to_int11([cdr.next(),cdr.next()]))
        ndr.append(cdr.next());ndr.append(hex_to_int11([cdr.next(),cdr.next()]))
        ndr.append(cdr.next());ndr.append(hex_to_int11([cdr.next(),cdr.next()]))
        ndr.append(cdr.next());ndr.append(hex_to_int11([cdr.next(),cdr.next()]))
        ndr.append(cdr.next());ndr.append(hex_to_int11([cdr.next(),cdr.next()]))

        ndr.append(hex_to_int32(cdr.next()));ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(hex_to_int32(cdr.next()));
        ndr.append(hex_to_int32(cdr.next()));ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(hex_to_int32(cdr.next()));
        ndr.append(hex_to_int32(cdr.next()));ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(hex_to_int32(cdr.next()));

        ndr.append(hex_to_int32(cdr.next()));ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(hex_to_int32(cdr.next()));
        ndr.append(cdr.next());ndr.append(hex_to_int24([cdr.next(),cdr.next()]))
        ndr.append(cdr.next());ndr.append(hex_to_int24([cdr.next(),cdr.next()]))
        ndr.append(cdr.next());ndr.append(hex_to_int24([cdr.next(),cdr.next()]))
        ndr.append(cdr.next());ndr.append(hex_to_int24([cdr.next(),cdr.next()]))
        ndr.append(cdr.next());ndr.append(hex_to_int24([cdr.next(),cdr.next()]))
        ndr.append(cdr.next());ndr.append(hex_to_int24([cdr.next(),cdr.next()]))

        ndr.append(hex_to_int32(cdr.next()));ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(hex_to_int32(cdr.next()));
        ndr.append(hex_to_int32(cdr.next()));ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(hex_to_int32(cdr.next()));
        ndr.append(hex_to_int32(cdr.next()));ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(hex_to_int32(cdr.next()));

        ndr.append(hex_to_int32(cdr.next()));ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(hex_to_int32(cdr.next()));
        ndr.append(cdr.next());ndr.append(hex_to_int24([cdr.next(),cdr.next()]))
        ndr.append(cdr.next());ndr.append(hex_to_int24([cdr.next(),cdr.next()]))
        ndr.append(cdr.next());ndr.append(hex_to_int24([cdr.next(),cdr.next()]))
        ndr.append(cdr.next());ndr.append(hex_to_int24([cdr.next(),cdr.next()]))
        ndr.append(cdr.next());ndr.append(hex_to_int24([cdr.next(),cdr.next()]))
        ndr.append(cdr.next());ndr.append(hex_to_int24([cdr.next(),cdr.next()]))

        ndr.append(hex_to_int32(cdr.next()));ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(hex_to_int32(cdr.next()));

        ### 140 ###

        ndr.append(hex_to_int32(cdr.next()));ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(hex_to_int32(cdr.next()));
        ndr.append(hex_to_int32(cdr.next()));ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(hex_to_int32(cdr.next()));
        ndr.append(hex_to_int32(cdr.next()));ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(hex_to_int32(cdr.next()));
        ndr.append(hex_to_int32(cdr.next()));ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(hex_to_int32(cdr.next()));

        ndr.append(hex_to_int32(cdr.next()));ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(hex_to_int32(cdr.next()));
        ndr.append(cdr.next());ndr.append(hex_to_int24([cdr.next(),cdr.next()]))
        ndr.append(cdr.next());ndr.append(hex_to_int24([cdr.next(),cdr.next()]))
        ndr.append(cdr.next());ndr.append(hex_to_int24([cdr.next(),cdr.next()]))
        ndr.append(cdr.next());ndr.append(hex_to_int24([cdr.next(),cdr.next()]))
        ndr.append(cdr.next());ndr.append(hex_to_int24([cdr.next(),cdr.next()]))
        ndr.append(cdr.next());ndr.append(hex_to_int24([cdr.next(),cdr.next()]))

        ndr.append(hex_to_int32(cdr.next()));ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(hex_to_int32(cdr.next()));
        ndr.append(hex_to_int32(cdr.next()));ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(hex_to_int32(cdr.next()));
        ndr.append(hex_to_int32(cdr.next()));ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(hex_to_int32(cdr.next()));

        ndr.append(hex_to_int32(cdr.next()));ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(hex_to_int32(cdr.next()));
        ndr.append(cdr.next());ndr.append(hex_to_int24([cdr.next(),cdr.next()]))
        ndr.append(cdr.next());ndr.append(hex_to_int24([cdr.next(),cdr.next()]))
        ndr.append(cdr.next());ndr.append(hex_to_int24([cdr.next(),cdr.next()]))
        ndr.append(cdr.next());ndr.append(hex_to_int24([cdr.next(),cdr.next()]))
        ndr.append(cdr.next());ndr.append(hex_to_int24([cdr.next(),cdr.next()]))
        ndr.append(cdr.next());ndr.append(hex_to_int24([cdr.next(),cdr.next()]))

        ndr.append(hex_to_int32(cdr.next()));ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(hex_to_int32(cdr.next()));

        ### 240 ###

        ndr.append(hex_to_int32(cdr.next()));ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(hex_to_int32(cdr.next()));
        ndr.append(hex_to_int32(cdr.next()));ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(hex_to_int32(cdr.next()));
        ndr.append(hex_to_int32(cdr.next()));ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(hex_to_int32(cdr.next()));
        ndr.append(hex_to_int32(cdr.next()));ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(hex_to_int32(cdr.next()));

        ndr.append(hex_to_int32(cdr.next()));ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(hex_to_int32(cdr.next()));
        ndr.append(cdr.next());ndr.append(hex_to_int24([cdr.next(),cdr.next()]))
        ndr.append(cdr.next());ndr.append(hex_to_int24([cdr.next(),cdr.next()]))
        ndr.append(cdr.next());ndr.append(hex_to_int24([cdr.next(),cdr.next()]))
        ndr.append(cdr.next());ndr.append(hex_to_int24([cdr.next(),cdr.next()]))
        ndr.append(cdr.next());ndr.append(hex_to_int24([cdr.next(),cdr.next()]))
        ndr.append(cdr.next());ndr.append(hex_to_int24([cdr.next(),cdr.next()]))

        ndr.append(hex_to_int32(cdr.next()));ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(hex_to_int32(cdr.next()));
        ndr.append(hex_to_int32(cdr.next()));ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(hex_to_int32(cdr.next()));
        ndr.append(hex_to_int32(cdr.next()));ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(hex_to_int32(cdr.next()));

        ndr.append(hex_to_int32(cdr.next()));ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(hex_to_int32(cdr.next()));
        ndr.append(cdr.next());ndr.append(hex_to_int24([cdr.next(),cdr.next()]))
        ndr.append(cdr.next());ndr.append(hex_to_int24([cdr.next(),cdr.next()]))
        ndr.append(cdr.next());ndr.append(hex_to_int24([cdr.next(),cdr.next()]))
        ndr.append(cdr.next());ndr.append(hex_to_int24([cdr.next(),cdr.next()]))
        ndr.append(cdr.next());ndr.append(hex_to_int24([cdr.next(),cdr.next()]))
        ndr.append(cdr.next());ndr.append(hex_to_int24([cdr.next(),cdr.next()]))

        ndr.append(hex_to_int32(cdr.next()));ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(hex_to_int32(cdr.next()));

        ### 340 ###

        ndr.append(hex_to_int32(cdr.next()));ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(hex_to_int32(cdr.next()));
        ndr.append(hex_to_int32(cdr.next()));ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(hex_to_int32(cdr.next()));
        ndr.append(hex_to_int32(cdr.next()));ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(hex_to_int32(cdr.next()));
        ndr.append(hex_to_int32(cdr.next()));ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(hex_to_int32(cdr.next()));

        ndr.append(hex_to_int32(cdr.next()));ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(hex_to_int32(cdr.next()));
        ndr.append(cdr.next());ndr.append(hex_to_int24([cdr.next(),cdr.next()]))
        ndr.append(cdr.next());ndr.append(hex_to_int24([cdr.next(),cdr.next()]))
        ndr.append(cdr.next());ndr.append(hex_to_int24([cdr.next(),cdr.next()]))
        ndr.append(cdr.next());ndr.append(hex_to_int24([cdr.next(),cdr.next()]))
        ndr.append(cdr.next());ndr.append(hex_to_int24([cdr.next(),cdr.next()]))
        ndr.append(cdr.next());ndr.append(hex_to_int24([cdr.next(),cdr.next()]))

        ndr.append(hex_to_int32(cdr.next()));ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(hex_to_int32(cdr.next()));
        ndr.append(hex_to_int32(cdr.next()));ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(hex_to_int32(cdr.next()));
        ndr.append(hex_to_int32(cdr.next()));ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(hex_to_int32(cdr.next()));

        ndr.append(hex_to_int32(cdr.next()));ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(hex_to_int32(cdr.next()));
        ndr.append(cdr.next());ndr.append(hex_to_int24([cdr.next(),cdr.next()]))
        ndr.append(cdr.next());ndr.append(hex_to_int24([cdr.next(),cdr.next()]))
        ndr.append(cdr.next());ndr.append(hex_to_int24([cdr.next(),cdr.next()]))
        ndr.append(cdr.next());ndr.append(hex_to_int24([cdr.next(),cdr.next()]))
        ndr.append(cdr.next());ndr.append(hex_to_int24([cdr.next(),cdr.next()]))
        ndr.append(cdr.next());ndr.append(hex_to_int24([cdr.next(),cdr.next()]))

        ndr.append(hex_to_int32(cdr.next()));ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(hex_to_int32(cdr.next()));

        ### 440 ###

        ndr.append(hex_to_int32(cdr.next()));ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(hex_to_int32(cdr.next()));
        ndr.append(hex_to_int32(cdr.next()));ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(hex_to_int32(cdr.next()));
        ndr.append(hex_to_int32(cdr.next()));ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(hex_to_int32(cdr.next()));
        ndr.append(hex_to_int32(cdr.next()));ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(hex_to_int32(cdr.next()));

        ndr.append(hex_to_int32(cdr.next()));ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(hex_to_int32(cdr.next()));
        ndr.append(cdr.next());ndr.append(hex_to_int24([cdr.next(),cdr.next()]))
        ndr.append(cdr.next());ndr.append(hex_to_int24([cdr.next(),cdr.next()]))
        ndr.append(cdr.next());ndr.append(hex_to_int24([cdr.next(),cdr.next()]))
        ndr.append(cdr.next());ndr.append(hex_to_int24([cdr.next(),cdr.next()]))
        ndr.append(cdr.next());ndr.append(hex_to_int24([cdr.next(),cdr.next()]))
        ndr.append(cdr.next());ndr.append(hex_to_int24([cdr.next(),cdr.next()]))

        ndr.append(hex_to_int32(cdr.next()));ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(hex_to_int32(cdr.next()));
        ndr.append(hex_to_int32(cdr.next()));ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(hex_to_int32(cdr.next()));
        ndr.append(hex_to_int32(cdr.next()));ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(hex_to_int32(cdr.next()));

        ndr.append(hex_to_int32(cdr.next()));ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(hex_to_int32(cdr.next()));
        ndr.append(cdr.next());ndr.append(hex_to_int24([cdr.next(),cdr.next()]))
        ndr.append(cdr.next());ndr.append(hex_to_int24([cdr.next(),cdr.next()]))
        ndr.append(cdr.next());ndr.append(hex_to_int24([cdr.next(),cdr.next()]))
        ndr.append(cdr.next());ndr.append(hex_to_int24([cdr.next(),cdr.next()]))
        ndr.append(cdr.next());ndr.append(hex_to_int24([cdr.next(),cdr.next()]))
        ndr.append(cdr.next());ndr.append(hex_to_int24([cdr.next(),cdr.next()]))

        ndr.append(hex_to_int32(cdr.next()));ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(hex_to_int32(cdr.next()));

        ### 540 ###

        ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(hex_to_int32(cdr.next()));ndr.append(cdr.next());

        return ndr

    def insert_stat(self,irec):
        ""
        rechash={'mo1':''}

        # print 'stat',irec.next(),irec.next(),irec.next(),irec.next(),irec.next(),irec.next()
        rechash.update({ 'encoder_counter':irec.next(), "mo1":irec.next(), "mo2":irec.next(),"rIdx":irec.next(),"wIdx":irec.next(),"counter":irec.next()})
        self.db.insert_dict("enc",rechash)
        return irec

    def insert_14(self,irec):
        irec=self.insert_stat(irec)

        rechash={}
        irec.next();rechash.update({ 'c1_s5':irec.next()})
        irec.next();rechash.update({ 'c2_s5':irec.next()})
        irec.next();rechash.update({ 'c3_s5':irec.next()})
        irec.next();rechash.update({ 'c4_s5':irec.next()})
        irec.next();rechash.update({ 'c5_s5':irec.next()})
        irec.next();rechash.update({ 'c6_s5':irec.next()})
        irec.next();rechash.update({ 'c8_s5':irec.next()})
        self.db.insert_dict("enc",rechash)

        irec=self.insert_stat(irec)
        irec=self.insert_stat(irec)
        irec=self.insert_stat(irec)

        irec=self.insert_stat(irec)
        rechash={}
        irec.next();rechash.update({ 'c1_s4':irec.next()})
        irec.next();rechash.update({ 'c2_s4':irec.next()})
        irec.next();rechash.update({ 'c3_s4':irec.next()})
        irec.next();rechash.update({ 'c4_s4':irec.next()})
        irec.next();rechash.update({ 'c5_s4':irec.next()})
        irec.next();rechash.update({ 'c6_s4':irec.next()})
        irec.next();rechash.update({ 'c8_s4':irec.next()})
        self.db.insert_dict("enc",rechash)

        irec=self.insert_stat(irec)
        irec=self.insert_stat(irec)
        irec=self.insert_stat(irec)

        irec=self.insert_stat(irec)
        rechash={}
        irec.next();rechash.update({ 'c1_s2':irec.next()})
        irec.next();rechash.update({ 'c2_s2':irec.next()})
        irec.next();rechash.update({ 'c3_s2':irec.next()})
        irec.next();rechash.update({ 'c4_s2':irec.next()})
        irec.next();rechash.update({ 'c5_s2':irec.next()})
        irec.next();rechash.update({ 'c6_s2':irec.next()})
        self.db.insert_dict("enc",rechash)

        irec=self.insert_stat(irec)
        irec=self.insert_stat(irec)
        irec=self.insert_stat(irec)

        irec=self.insert_stat(irec)
        rechash={}
        irec.next();rechash.update({ 'c1_s6':irec.next()})
        irec.next();rechash.update({ 'c2_s6':irec.next()})
        irec.next();rechash.update({ 'c3_s6':irec.next()})
        irec.next();rechash.update({ 'c4_s6':irec.next()})
        irec.next();rechash.update({ 'c5_s6':irec.next()})
        irec.next();rechash.update({ 'c6_s6':irec.next()})
        self.db.insert_dict("enc",rechash)

        irec=self.insert_stat(irec)

        return irec


    def insert_10(self,irec):
        irec=self.insert_stat(irec)
        irec=self.insert_stat(irec)
        irec=self.insert_stat(irec)
        irec=self.insert_stat(irec)

        irec=self.insert_stat(irec)
        rechash={}
        irec.next();rechash.update({ 'c1_s2':irec.next()})
        irec.next();rechash.update({ 'c2_s2':irec.next()})
        irec.next();rechash.update({ 'c3_s2':irec.next()})
        irec.next();rechash.update({ 'c4_s2':irec.next()})
        irec.next();rechash.update({ 'c5_s2':irec.next()})
        irec.next();rechash.update({ 'c6_s2':irec.next()})
        self.db.insert_dict("enc",rechash)

        irec=self.insert_stat(irec)
        irec=self.insert_stat(irec)
        irec=self.insert_stat(irec)

        irec=self.insert_stat(irec)
        rechash={}
        irec.next();rechash.update({ 'c1_s6':irec.next()})
        irec.next();rechash.update({ 'c2_s6':irec.next()})
        irec.next();rechash.update({ 'c3_s6':irec.next()})
        irec.next();rechash.update({ 'c4_s6':irec.next()})
        irec.next();rechash.update({ 'c5_s6':irec.next()})
        irec.next();rechash.update({ 'c6_s6':irec.next()})
        self.db.insert_dict("enc",rechash)

        irec=self.insert_stat(irec)

        return irec

    def parse_enc(self,file,file_index):
        ""
        self.file=file
        self.file_index=file_index
        self.file_size=os.stat(file).st_size
        print "Opening file %s size %s" % (file, self.file_size)

        if self.file_size < self.DAQ_BUFFER_SIZE:
            exit

        file_size=self.file_size
        with open(file,'rb') as fh:
          pos_s=self.seek_until(fh,file_size,0)

          self.num_recs=0
          self.bad_recs=0
          self.currBytes=0
          while(True):
            # try:

                pos_s=fh.tell()

                self.file_pos=pos_s

                ### break out
                if pos_s+self.DAQ_BUFFER_SIZE >= file_size:
                    # print 'HI'
                    break
                # print file_size - pos_s -16
                if file_size - pos_s -16 < self.DAQ_BUFFER_SIZE:
                    break

                recordType,chunk=self.get_next_record(fh,file_size,pos_s,self.DAQ_BUFFER_SIZE)
                chunk=self.reject_artifacts(chunk)
                print chunk.encode('hex')

                ### check chunk is valid
                length=len(chunk)

                print length
                # print chunk.encode('hex')
                if length != self.DAQ_BUFFER_SIZE:
                    self.bad_recs = self.bad_recs+1

                    self.seek_until(fh,file_size,pos_s)
                else:

                    if recordType == self.TAILSYMBC:

                        rec=struct.unpack(self.daq_fmt,chunk)
                        bytea=chunk
                        # print struct.unpack('<L',bytea[0:4])
                        # for rec in self.DAQ_FORMAT_LIST:
                        #     print rec

                    rec=self.convert_resolution(rec)

                    irec=itertools.chain(rec)

                    ### transform data ###
                    # crec=convert(rec)

                    # enc=rec[85]
                    # print h
                    # h=unpackex(enc,H32)
                    # print h
                    # crec[85]=enc

                    # c1_s2=rec[21]
                    # c3_s2=rec[25]
                    # c4_s2=rec[27]
                    # print 'sense'
                    # print c1_s2,c3_s2,c4_s2
                    # print hex(c1_s2),hex(c3_s2),hex(c4_s2)
                    # h1=unpackex(c1_s2,H24)
                    # h3=unpackex(c3_s2,H24)
                    # h4=unpackex(c4_s2,H24)
                    # print h1,h3,h4

                    # h=unpackex(enc,H32)

                    # counter=rec[88]

                    # crec[88]=unpackex(counter,H32)



                    ### add in processor info ###
                    timestamp=''

                    ### 0 ###

                    irec=self.insert_14(irec)

                    ### 140 ###

                    irec=self.insert_10(irec)

                    ### 240 ###

                    irec=self.insert_10(irec)

                    ### 340 ###

                    irec=self.insert_10(irec)

                    ### 440 ###

                    irec=self.insert_10(irec)

                    ### 540 ###

                    rechash={}
                    rechash.update({'file_index':file_index, 'packet_len':length,'file_pos':self.file_pos})
                    self.db.insert_dict("enc",rechash)

                    self.num_recs += 1

                    if self.num_recs % self.DB_COMMIT_INTERVAL == 0 and self.num_recs > 0:
                        print "commit %s" % self.num_recs
                        self.db.commit()
                        self.currBytess=self.currBytes+length


            # except Exception,e:
            #   print "read error: "+ str(e)


if __name__ == '__main__':
    fp='c:/datasets/1427929783/data/20000101_000222.enc'
    basename=os.path.splitext(os.path.basename(fp))[0]
    recname='%s.recE' % basename
    # recp='%s/%s' % (fdrp,recname)
    shutil.copy('../../common/daq.db',recname)

    task=DecodeEncTask(recname)
    print task.DAQ_BUFFER_SIZE
    task.parse_enc(fp,0)