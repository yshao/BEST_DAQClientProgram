import sys
import struct
from test.common.sqliteutils import *

# RAD structure


def usage():
    print "Usage: daq_parse [options] file_directory"
    print "       Options:"
    print "         -v  Logger output on/off"
    print "         -d  File directory to read raw files"
    print "         -f  Individual file to parse"
    sys.exit(1)

TAILSYMB1=0x3A3A
TAILSYMB2=0x3B3B

def get_next_record(fh,start,symb,estimate,margin=6):
    fh.seek(start)
    dr=fh.read(estimate - margin)

    while(fh.start < file.size):
        dr1=fh.read(2)
        if dr1 == symb:
            break
        else:
            dr1=fh.read(2)
            ### filter E7E7
            if dr1 == 0xE7E7:
                "buffer empty"

            else:
                dr=dr+dr1

    return dr


def main():
  db=DaqDB("daq.db")
  BUFFER_SIZE=64

  fmt_list=['!HHHHHHHHHHHHH',
            'HHHHHHHHHHHHH',
            'LHHH2s']
  cols = ['ch1_1','ch2_1','ch3_1','ch4_1','ch5_1','ch6_1','ch7_1','ch8_1','ch9_1','ch10_1','ch11_1','ch12_1','hKey_1',
            'ch1_2','ch2_2','ch3_2','ch4_2','ch5_2','ch6_2','ch7_2','ch8_2','ch9_2','ch10_2','ch11_2','ch12_2','hKey_2',
            'counter','temp','wIdx','rIdx','tailsymb',
            'file_index','timestamp']
  fmt="".join(fmt_list)

  file_index=-1
  i=-1
  for file in np.sort(glob.glob(os.path.join("data", '*.rad'))):
    file_index += 1

    print "Opening file %s" % file
    with open(file,'rb') as fh:
      # get to header
      # pos=seek_until(fh,[0x3A,0x3A],145)
      # if pos == 145:
      #     pos = seek_until(fh,[0x3B,0x3B],145)
      #
      # fh.seek(pos)

      eob=False
      while(1):
        i += 1
        try:
            pos_s=fh.tell()
            pos_e= (i+1)*BUFFER_SIZE
            # print pos_e
            if pos_e > os.stat(file).st_size:
                num_bytes= os.stat(file).st_size - pos_s
                eob=True

                chunk=fh.read(num_bytes)
            else:
                chunk=fh.read(BUFFER_SIZE)

            length=len(chunk)
            if length == BUFFER_SIZE:
                rec=struct.unpack(fmt,chunk)
                reclen=len(rec)
                if reclen == 31:


                    rec = rec + (file_index,)
                    rec = rec + ("_",)

                    ### apply scaling ###
                    rec1=rec

                    db.insert_raws("rad",cols,[rec1])
                    if i % 50 == 0:
                        db.commit()

            if eob:
                break

        except Exception,e:
          print "read error: "+ str(e)



main()

#convert raw counts into proper numerical
def apply_scaling(dr):
    dr[0] = dr[0] * 5000. / 2^31
    dr[1] = dr[1] * 5000. / 2^31
    dr[2] = dr[2] * 5000. / 2^31
    dr[3] = dr[3] * 5000. / 2^31
    dr[4] = dr[4] * 5000. / 2^31
    dr[5] = dr[5] * 5000. / 2^31
    dr[6] = dr[6] * 5000. / 2^31
    dr[7] = dr[7] * 5000. / 2^31
    dr[8] = dr[8] * 5000. / 2^31
    dr[9] = dr[9] * 5000. / 2^31
    dr[10] = dr[10] * 5000. / 2^31
    dr[11] = dr[11] * 5000. / 2^31
    dr[12] = map( lambda x: {0x1234 : 1, 0x4444 : 2}.get(x), dr[12])

    dr[13] = dr[13] * 5000. / 2^31
    dr[14] = dr[14] * 5000. / 2^31
    dr[15] = dr[15] * 5000. / 2^31
    dr[16] = dr[16] * 5000. / 2^31
    dr[17] = dr[17] * 5000. / 2^31
    dr[18] = dr[18] * 5000. / 2^31
    dr[19] = dr[19] * 5000. / 2^31
    dr[20] = dr[20] * 5000. / 2^31
    dr[21] = dr[21] * 5000. / 2^31
    dr[22] = dr[22] * 5000. / 2^31
    dr[23] = dr[23] * 5000. / 2^31
    dr[24] = dr[24] * 5000. / 2^31
    dr[25] = map( lambda x: {0x1234 : 1, 0x4444 : 2}.get(x), dr[25])

    dr[26] = dr[1] * 5000. / 2^31
    dr[27] = dr[2] * 5000. / 2^15
    dr[28] = dr[3] * 5000. / 2^15
    dr[29] = dr[4] * 5000. / 2^15
    #dr[30] = TAILBYM

    #dr[31] = file_index
    dr[32] = convert_timestamp(dr[32])

    return dr


def seek_until(fh,hex_pattern,bytes_limit):
    i=0
    while(1):
        fh.seek(i)
        byte=fh.read(1)
        if byte == hex_pattern[0]:
            byte=fh.read(1)
            if byte == hex_pattern[1]:
                break

        if i > bytes_limit:
            break
        i +=1

    return i
