import sys
import struct
import re
from test.common.sqliteutils import *

TIMESTAMP_HEAD='A7AF'
TIMESTAMP_TAIL='A7BF'

TAILSYMBC="3C3C"
DB_COMMIT_INTERVAL=5

def reject_artifacts(dr):
    ""
    dr=dr.encode("hex")
    dr=dr.replace("e7e7","")
    dr=dr.decode("hex")

    return dr

def get_next_record(fh,file_size,start,estimate,margin=6):
    pos_s=start
    dr=fh.read(estimate - margin)

    while(pos_s+estimate < file_size):
        dr1=fh.read(2)
        hexsymb=dr1.encode("hex").upper()
        # print hexsymb

        dr=dr+dr1
        if hexsymb == TAILSYMBC:
            #TODO: modify encoder firmware to be the same as rad
            # dr=dr+fh.read(4)
            break

        # print dr.encode("hex")

    return dr

# find the end of first header
def seek_until(fh,file_size):
  pre=0
  while (pre < file_size):
    bytes=fh.read(2).encode("hex").upper()
    # print bytes
    if bytes == TAILSYMBC:
      break
    else:
      pre+=2

  return fh.tell()

def extract_timestamp(dr):
    ""
    hex_dr=dr.encode("hex").upper()
    m= re.search(re.escape(TIMESTAMP_HEAD)+r'.*?'+re.escape(TIMESTAMP_TAIL),hex_dr)
    if m.group(0) is None:
        return ''
    else:
        print m.group(0)
        return m.group(0)

    # dr=dr.decode("hex")




def main():
  file_index=-1
  i=-1
  for file in np.sort(glob.glob(os.path.join("data", '*.time'))):
    file_index += 1

    file_size=os.stat(file).st_size
    print "Opening file %s size %s" % (file, file_size)

    with open(file,'rb') as fh:
      pos_s=seek_until(fh,file_size)

      i=0
      while(1):
        i += 1
        try:
            pos_s=fh.tell()
            # print pos_s

            if pos_s+55 > file_size:
                break

            chunk=get_next_record(fh,file_size,pos_s,55)
            chunk=reject_artifacts(chunk)
            timestamp=extract_timestamp(chunk)
            print timestamp


        except Exception,e:
          print "read error: "+ str(e)


main()
