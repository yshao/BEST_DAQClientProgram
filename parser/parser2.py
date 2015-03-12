import struct
import binascii
import getopt
import sys
import ctypes


import struct
from collections import namedtuple
# data = "1"*24
# fmt = "20si"
# Rec = namedtuple('Rec', 'text index')
# r = Rec._make(struct.unpack_from(fmt, data))
# r


# INU structure
# c_double = DWORD
#
# original ctypes structure definition
# _fields_ = [ ('seq_num', ctypes.c_short),
#              ('enc_counter_hi', ctypes.c_int32),
#              ('enc_counter_lo', ctypes.c_int32),
#              ('enc_counter_lo', ctypes.c_int32),
#              ('wIdx', ctypes.c_int32),
#              ('rIdx', ctypes.c_int32),
#              ('motor_out', ctypes.c_int32),
#              ('ch1_addr1sense', ctypes.c_int32),
#              ('ch1_addr3sense', ctypes.c_int32),
#              ('ch1_addr4sense', ctypes.c_int32),
#              ('ch2_addr1sense', ctypes.c_int32),
#              ('ch2_addr3sense', ctypes.c_int32),
#              ('ch2_addr4sense', ctypes.c_int32),
#              ('ch2_addr5sense', ctypes.c_int32),
#              ('ch3_addr1sense', ctypes.c_int32),
#              ('ch3_addr3sense', ctypes.c_int32),
#              ('ch3_addr4sense', ctypes.c_int32),
#              ('ch4_addr4sense', ctypes.c_int32),
#              ('ch5_addr5sense', ctypes.c_int32),
#              ('ch6_addr4sense', ctypes.c_int32),
#              ('ch6_addr5sense', ctypes.c_int32),
#              ('ch7_addr4sense', ctypes.c_int32),
#              ('ch7_addr5sense', ctypes.c_int32),
#              ('counter_lo', ctypes.c_int32),
#              ('counter_hi', ctypes.c_int32),


# Radiometer structure
# c_double = DWORD
#
# original ctypes structure definition
# _fields_ = [ ('seq_num', ctypes.c_short),
#              ('temp_data', ctypes.c_int32),
#              ('wIdx', ctypes.c_int32),
#              ('rIdx', ctypes.c_int32),
#              ('hKey', ctypes.c_int32),
#              ('ch0', ctypes.c_int32),
#              ('ch1', ctypes.c_int32),
#              ('ch2', ctypes.c_int32),
#              ('ch3', ctypes.c_int32),
#              ('ch4', ctypes.c_int32),
#              ('ch5', ctypes.c_int32),
#              ('ch6', ctypes.c_int32),
#              ('ch7', ctypes.c_int32),
#              ('ch8', ctypes.c_int32),
#              ('ch9', ctypes.c_int32),
#              ('ch10', ctypes.c_int32),
#              ('ch11', ctypes.c_int32),
#              ('ch12', ctypes.c_int32),
#              ('ch13', ctypes.c_int32),
#              ('counter_lo', ctypes.c_int32),
#              ('counter_hi', ctypes.c_int32),
#               TAILSYMB = 3A3A or 3B3B


# Encoder structure
# c_double = DWORD
#
# original ctypes structure definition
# _fields_ = [ ('seq_num', ctypes.c_short),
#              ('enc_counter_hi', ctypes.c_int32),
#              ('enc_counter_lo', ctypes.c_int32),
#              ('enc_counter_lo', ctypes.c_int32),
#              ('wIdx', ctypes.c_int32),
#              ('rIdx', ctypes.c_int32),
#              ('motor_out', ctypes.c_int32),
#              ('ch1_addr1sense', ctypes.c_int32),
#              ('ch1_addr3sense', ctypes.c_int32),
#              ('ch1_addr4sense', ctypes.c_int32),
#              ('ch2_addr1sense', ctypes.c_int32),
#              ('ch2_addr3sense', ctypes.c_int32),
#              ('ch2_addr4sense', ctypes.c_int32),
#              ('ch2_addr5sense', ctypes.c_int32),
#              ('ch3_addr1sense', ctypes.c_int32),
#              ('ch3_addr3sense', ctypes.c_int32),
#              ('ch3_addr4sense', ctypes.c_int32),
#              ('ch4_addr4sense', ctypes.c_int32),
#              ('ch5_addr5sense', ctypes.c_int32),
#              ('ch6_addr4sense', ctypes.c_int32),
#              ('ch6_addr5sense', ctypes.c_int32),
#              ('ch7_addr4sense', ctypes.c_int32),
#              ('ch7_addr5sense', ctypes.c_int32),
#              ('counter_lo', ctypes.c_int32),
#              ('counter_hi', ctypes.c_int32),

#              ('id1', ctypes.c_char * 3) ]
#
# Equivalent struct format string:
# 'hhhd3s'
#'counter', ctypes.c_int32 = l

from collections import namedtuple


def usage():
    print "Usage: daq_parse [options] file_directory"
    print "       Options:"
    print "         -v  Logger output on/off"
    print "         -d  File directory to read raw files"
    print "         -f  Individual file to parse"
    sys.exit(1)


from sqlalchemy.engine import *
from sqlalchemy import schema, types

#metadata = schema.MetaData()


# PAGE_TABLE = schema.Table(
#     schema.Column('id', types.Integer, primary_key=True),
#     schema.Column('name', types.Unicode(255), default=u''),
#     schema.Column('title', types.Unicode(255), default=u'Untitled Page'),
#     schema.Column('content', types.Text(), default=u''),
# )

from sqlalchemy import *
from sqlalchemy.orm import *
from collections import namedtuple

def sql_insert_record(dr):
    Point=namedtuple('Point',['x','y'],verbose=True)
    p=Point(3,4)

    db=create_engine('sqlite:///daq.db')
    metadata=MetaData()
    if dr == "RadRecord":
        pointxy=Table('pointxy',metadata,
              Column('no',Integer,primary_key=True),
              Column('x',Integer),
              Column('y',Integer),
              sqlite_autoincrement=True)
        metadata.create_all(db)
        m=mapper(Point, pointxy)

    elif dr == "EncRecord":
        ""

    elif dr == "InuRecord":
        ""

    Session=sessionmaker(bind=db)
    session=Session()

    # f=Point(3,4)
    newrow=mapper(dr) #http://stackoverflow.com/questions/7634177/is-it-possible-to-use-a-namedtuple-with-sqlalchemy
    session.add(newrow)

import struct

from collections import namedtuple

def main():
  # get command line arguments
  # if len(sys.argv) > 1:
  #     try:
  #         clopts, clargs = getopt.getopt(sys.argv[1:], ':v:d:f:')
  #     except getopt.GetoptError, err:
  #         print str(err)
  #         sys.exit(2)
  #     #endtry
  #
  #     for opt, arg in clopts:
  #         if opt == "-v":
  #             loggerOn = True
  #         elif opt == "-d":
  #             repo = arg
  #         elif opt == "-f":
  #             file = arg
  #         else:
  #             print "Unrecognized option"
  #             usage()
  #     if len(clargs) > 0:
  #         fname = clargs[0]
  # else:
  #     usage()
  #     sys.exit(2) # oops - forget to put this into the code in the book


  print "Processing starts here"
  file="receiver20-30_20000101_000353.rad"
  print "Opening %s\n" % file

  i=0
  rc=[]

  # find first header
  BUFFER_SIZE=80

  with open(file,'rb') as fh:
   # get_header
   i += 1
   try:
    print i
    # byte= binascii.hexlify(fh.read(4))
    chunk=fh.read(BUFFER_SIZE)
    if len(chunk) < BUFFER_SIZE:
        ""
    else:
    # error in unpack struct then discard
    #   rec=struct.unpack('LLLLLLLLLLLLLLLLLLLcc',chunk)
      rec=struct.unpack('HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH2s',chunk)
      # Rec = namedtuple('RadRecord','1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 TAILSYMB')
      # newrec=Rec._make(struct.unpack_from('HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH2s',chunk))
      # newrec=DataRecord(rec)

    newrec=1
    # insert_record(newrec)



   except:
       print "read error"


main()