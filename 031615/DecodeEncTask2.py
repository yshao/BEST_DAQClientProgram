import struct
import os
from PyQt4.QtCore import pyqtSignal, SIGNAL, QThread
from best.common.sqliteutils import DaqDB
import itertools
from datautils import *


class DecodeEncTask(QThread):
    # QThread.__init__(self)
    signalNumOfRecords=pyqtSignal(int)
    signalCommit=pyqtSignal()

    TAILSYMBC="3C3C"
    # HEADER_STAT_DUMP_INIT="A7E8"
    # HEADER_STAT_DUMP_DATA="A7E1"
    HEADER_STAT="A8A7"
    HEADER_ENC="FCA7"


    DB_COMMIT_INTERVAL=5
  # previous state machine
  # symb enc mo 14 11 24 21 34 31 45 55 65 75
  # symb enc mo 13 23 33
  # symb enc mo 11 21 31
  # symb enc mo 15 13 25 23 35 33 44 54 64 74
  # symb enc mo 11 21 31
  # symb enc mo 13 23 33
  # symb rIdx wIdx counter tailsymb

    # DAQ_FORMAT_LIST=["<2sHHLsBHsBHsBHsBHsBHsBHsBHsBHsBHsBH",
    #                    "2sHHLsBHsBHsBH",
    #                    "2sHHLsBHsBHsBH",
    #                    "2sHHLsBHsBHsBHsBHsBHsBHsBHsBHsBHsBH",
    #                    "2sHHLsBHsBHsBH",
    #                    "2sHHLsBHsBHsBH",
    #                    "2sHHL2s"
    #             ]


  # current state machine
  #   FCA7 mo1 mo2 enc 15 25 35 45 55 65 75
  #   FCA7 mo1 mo2 enc 22 32 42 52 62
  #   FCA7 mo1 mo2 enc 16 26 36 46 56 66
  #   FCA7 mo1 mo2 enc 14 24 34 44 54 64 74
  #   FCA7 mo1 mo2 enc 12 22 32 42 52 62
  #   FCA7 mo1 mo2 enc 16 26 36 46 56 66
  #   A8A7 rIdx wIdx counter 3C3C

    DAQ_FORMAT_LIST=[ "<2sHHL","sHBsHBsHBsHBsHBsHBsHB",
                       "2sHHL","sHBsHBsHBsHBsHBsHB",
                       "2sHHL","sHBsHBsHBsHBsHBsHB",
                       "2sHHL","sHBsHBsHBsHBsHBsHBsHB",
                       "2sHHL","sHBsHBsHBsHBsHBsHB",
                       "2sHHL","sHBsHBsHBsHBsHBsHB",

                       "2sHHL2s",
                ]

    DAQ_FORMAT_LIST=["<HHL"



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
    def __del__(self):
        ""
        # self.db.close(self)

    def __init__(self):
        ""
        QThread.__init__(self)
        self.numRecords=0
        self.currBytes=0
        self.totalBytes=0
        self.currFile=""
        self.db=DaqDB("../enc.db")
        self.pdb=DaqDB("../daq.db")
        
        # self.connect(self,SIGNAL("task_decode()"),self.parse_enc,file)

    def commit(self):
        ""
        self.db.commit()
                        # self.numRecords=num_recs
                        # self.currBytess=
        # self.emit(SIGNAL("decoded_sets()"))
        self.signalCommit.emit()
        self.signalNumOfRecords.emit(self.numRecords)


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

        while(pos_s+estimate < file_size):
            dr1=fh.read(2)
            hexsymb=dr1.encode("hex").upper()

            dr=dr+dr1
            if hexsymb == self.TAILSYMBC:
                break

        return hexsymb,dr

    # clean off artifiacts
    def reject_artifacts(self,dr):
        ""
        ndr=dr.encode("hex")
        ndr=ndr.replace("e7e7","")
        print ndr
        print len(ndr)

        a=ndr[0:424]
        b=ndr[896:920]
        disgard=ndr[424:1246]

        c= a+b
        print c
        ndr=c.decode("hex")


        return ndr

    def remove_tuple(self,original_tuple, element_to_remove):
        new_tuple = []
        for s in list(original_tuple):
            if not s == element_to_remove:
                new_tuple.append(s)
        return tuple(new_tuple)



    def convert_resolution(self,dr):
        ""
        # ndr  = [i for i in range(self.DAQ_BUFFER_SIZE)]
        # cdr=cycle(dr)
        ndr=list()


        cdr = itertools.chain(dr)

  # current state machine
  #   FCA7 mo1 mo2 enc 15 25 35 45 55 65 85
  #   FCA7 mo1 mo2 enc 12 22 32 42 52 62
  #   FCA7 mo1 mo2 enc 16 26 36 46 56 66
  #   FCA7 mo1 mo2 enc 14 24 34 44 54 64 84
  #   FCA7 mo1 mo2 enc 12 22 32 42 52 62
  #   FCA7 mo1 mo2 enc 16 26 36 46 56 66
  #   A8A7 rIdx wIdx counter 3C3C


  #   hum values are 11bit
  #   pres values are 24bit

  #   val = 66

        ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next())
        ndr.append(cdr.next());ndr.append(bin_to_int([cdr.next(),cdr.next()],11,5))
        ndr.append(cdr.next());ndr.append(bin_to_int([cdr.next(),cdr.next()],11,5))
        ndr.append(cdr.next());ndr.append(bin_to_int([cdr.next(),cdr.next()],11,5))
        ndr.append(cdr.next());ndr.append(bin_to_int([cdr.next(),cdr.next()],11,5))
        ndr.append(cdr.next());ndr.append(bin_to_int([cdr.next(),cdr.next()],11,5))
        ndr.append(cdr.next());ndr.append(bin_to_int([cdr.next(),cdr.next()],11,5))
        ndr.append(cdr.next());ndr.append(bin_to_int([cdr.next(),cdr.next()],11,5))

        ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next())
        ndr.append(cdr.next());ndr.append(bin_to_int([cdr.next(),cdr.next()],24))
        ndr.append(cdr.next());ndr.append(bin_to_int([cdr.next(),cdr.next()],24))
        ndr.append(cdr.next());ndr.append(bin_to_int([cdr.next(),cdr.next()],24))
        ndr.append(cdr.next());ndr.append(bin_to_int([cdr.next(),cdr.next()],24))
        ndr.append(cdr.next());ndr.append(bin_to_int([cdr.next(),cdr.next()],24))
        ndr.append(cdr.next());ndr.append(bin_to_int([cdr.next(),cdr.next()],24))

        ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next())
        ndr.append(cdr.next());ndr.append(bin_to_int([cdr.next(),cdr.next()],24))
        ndr.append(cdr.next());ndr.append(bin_to_int([cdr.next(),cdr.next()],24))
        ndr.append(cdr.next());ndr.append(bin_to_int([cdr.next(),cdr.next()],24))
        ndr.append(cdr.next());ndr.append(bin_to_int([cdr.next(),cdr.next()],24))
        ndr.append(cdr.next());ndr.append(bin_to_int([cdr.next(),cdr.next()],24))
        ndr.append(cdr.next());ndr.append(bin_to_int([cdr.next(),cdr.next()],24))


        ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next())
        ndr.append(cdr.next());ndr.append(bin_to_int([cdr.next(),cdr.next()],11,5))
        ndr.append(cdr.next());ndr.append(bin_to_int([cdr.next(),cdr.next()],11,5))
        ndr.append(cdr.next());ndr.append(bin_to_int([cdr.next(),cdr.next()],11,5))
        ndr.append(cdr.next());ndr.append(bin_to_int([cdr.next(),cdr.next()],11,5))
        ndr.append(cdr.next());ndr.append(bin_to_int([cdr.next(),cdr.next()],11,5))
        ndr.append(cdr.next());ndr.append(bin_to_int([cdr.next(),cdr.next()],11,5))
        ndr.append(cdr.next());ndr.append(bin_to_int([cdr.next(),cdr.next()],11,5))

        ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next())
        ndr.append(cdr.next());ndr.append(bin_to_int([cdr.next(),cdr.next()],24))
        ndr.append(cdr.next());ndr.append(bin_to_int([cdr.next(),cdr.next()],24))
        ndr.append(cdr.next());ndr.append(bin_to_int([cdr.next(),cdr.next()],24))
        ndr.append(cdr.next());ndr.append(bin_to_int([cdr.next(),cdr.next()],24))
        ndr.append(cdr.next());ndr.append(bin_to_int([cdr.next(),cdr.next()],24))
        ndr.append(cdr.next());ndr.append(bin_to_int([cdr.next(),cdr.next()],24))

        ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next())
        ndr.append(cdr.next());ndr.append(bin_to_int([cdr.next(),cdr.next()],24))
        ndr.append(cdr.next());ndr.append(bin_to_int([cdr.next(),cdr.next()],24))
        ndr.append(cdr.next());ndr.append(bin_to_int([cdr.next(),cdr.next()],24))
        ndr.append(cdr.next());ndr.append(bin_to_int([cdr.next(),cdr.next()],24))
        ndr.append(cdr.next());ndr.append(bin_to_int([cdr.next(),cdr.next()],24))
        ndr.append(cdr.next());ndr.append(bin_to_int([cdr.next(),cdr.next()],24))

        ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next())

        return ndr



    def parse_enc(self,file,file_index):
        ""
        file_size=os.stat(file).st_size
        print "Opening file %s size %s" % (file, file_size)
        
        with open(file,'rb') as fh:
          pos_s=self.seek_until(fh,file_size,0)

          self.num_recs=0
          self.bad_recs=0
          self.currBytes=0
          while(True):
            try:
                pos_s=fh.tell()

                if pos_s+self.DAQ_BUFFER_SIZE > file_size:
                    break

                recordType,chunk=self.get_next_record(fh,file_size,pos_s,self.DAQ_BUFFER_SIZE)
                chunk=self.reject_artifacts(chunk)

                ### check chunk is valid
                length=len(chunk)

                # print chunk.encode('hex')
                if length != self.DAQ_BUFFER_SIZE:
                    self.bad_recs = self.bad_recs+1

                    self.seek_until(fh,file_size,pos_s)
                else:

                    if recordType == self.TAILSYMBC:
                        rec=struct.unpack(self.daq_fmt,chunk)

                    rec=self.convert_resolution(rec)

                    ### add in processor info ###
                    timestamp=''
                    rechash={}

                    rechash.update({"mo1":rec[1], "mo2":rec[2], "encoder_counter":rec[3],
                                    'c1_s5':rec[5], 'c2_s5':rec[7], 'c3_s5':rec[9], 'c4_s5':rec[11],
                                   'c5_s5':rec[13], 'c6_s5':rec[15], 'c8_s5':rec[17]})
                    # rechash.update({'file_index':file_index,  'packet_len':length})
                    self.db.insert_dict("enc",rechash)
                    # db.commit()

                    ###
                    rechash={}
                    rechash.update({"mo1":rec[19], "mo2":rec[20], 'encoder_counter':rec[21],
                                    'c1_s2':rec[23], 'c2_s2':rec[25], 'c3_s2':rec[77],'c4_s2':rec[29],
                                    'c5_s2':rec[31], 'c6_s2':rec[33]})
                    # rechash.update({'file_index':file_index, 'packet_len':length})
                    self.db.insert_dict("enc",rechash)
                    # db.commit()

                    ###
                    # print rec[32]
                    rechash={}
                    rechash.update({"mo1":rec[35], "mo2":rec[36], 'encoder_counter':rec[37],
                                    'c1_s6':rec[39], 'c2_s6':rec[41], 'c3_s6':rec[43],'c4_s6':rec[45],
                                    'c5_s6':rec[47], 'c6_s6':rec[49]})
                    # rechash.update({'file_index':file_index,  'packet_len':length})
                    self.db.insert_dict("enc",rechash)
                    # db.commit()

                    rechash={}

                    rechash.update({"mo1":rec[51], "mo2":rec[52], "encoder_counter":rec[53],
                                    'c1_s4':rec[55], 'c2_s4':rec[57], 'c3_s4':rec[59], 'c4_s4':rec[61],
                                   'c5_s4':rec[63], 'c6_s4':rec[65], 'c8_s4':rec[67]})
                    # rechash.update({'file_index':file_index,  'packet_len':length})
                    self.db.insert_dict("enc",rechash)

                    rechash={}
                    rechash.update({"mo1":rec[69], "mo2":rec[70], 'encoder_counter':rec[71],
                                    'c1_s2':rec[73], 'c2_s2':rec[75], 'c3_s2':rec[77],'c4_s2':rec[79],
                                    'c5_s2':rec[81], 'c6_s2':rec[83]})
                    # rechash.update({'file_index':file_index, 'packet_len':length})
                    self.db.insert_dict("enc",rechash)
                    # db.commit()

                    rechash={}
                    rechash.update({"mo1":rec[85], "mo2":rec[86], 'encoder_counter':rec[87],
                                    'c1_s6':rec[89], 'c2_s6':rec[91], 'c3_s6':rec[93],'c4_s6':rec[95],
                                    'c5_s6':rec[97], 'c6_s6':rec[99]})
                    # rechash.update({'file_index':file_index,  'packet_len':length})
                    self.db.insert_dict("enc",rechash)
                    # db.commit()

                    rechash={}
                    rechash.update({'wIdx':rec[101], 'rIdx':rec[102], 'counter':rec[103], 'tailsymb':rec[104],
                                    'timestamp':timestamp})
                    rechash.update({'file_index':file_index, 'packet_len':length})
                    self.db.insert_dict("enc",rechash)
                    # db.commit()
                    self.num_recs += 1

                    if self.num_recs % self.DB_COMMIT_INTERVAL == 0 and self.num_recs > 0 :
                        print "commit %s" % self.num_recs
                        self.db.commit()
                        # self.numRecords=num_recs
                        self.currBytess=self.currBytes+length
                        # self.emit(SIGNAL("decoded_sets()"))
                

            except Exception,e:
              print "read error: "+ str(e)


if __name__ == '__main__':
    task=DecodeEncTask()
    task.parse_enc("data/20000101_000141.enc",0)



