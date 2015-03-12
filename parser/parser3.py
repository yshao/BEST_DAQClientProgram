import struct
from parseutils import *


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

  basedir="C:/Users/Ping/Workspace/DAQ/test/parser/data"
  for file in list_files_with(basedir,"*.enc"):
      full_pname=basedir+"/"+file
      print "Opening %s\n" % full_pname

      i=0
      rc=[]

      # find first header
      BUFFER_SIZE=80

      with open(full_pname,'rb') as fh:
       # get_header
       i += 1
       try:
        print i
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
        sql_insert_record(newrec)



       except:
           print "read error"


main()