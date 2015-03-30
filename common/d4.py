import shutil
import sqlite3
from common.env import Env

recE='20000101_000204.recE'
recI='20000101_000203.recI'

cfg=Env().getConfig()
local='c:/datasets/buffer'
datap='%s/%s' % (local,'dataset.db')

shutil.copy('daq.db',datap)

con = sqlite3.connect(datap)
recEp='%s/%s' % (local,recE)
recIp='%s/%s' % (local,recI)

print recEp,recIp
con.execute("attach database '%s' as db1" % recEp)
con.execute("attach database '%s' as db2" % recIp)

sql="""c1_s1,c1_s2,c1_s3,c1_s4,c1_s5,c1_s6,
        c2_s1,c2_s2,c2_s3,c2_s4,c2_s5,c2_s6,
        c3_s1,c3_s2,c3_s3,c3_s4,c3_s5,c3_s6,
        c4_s1,c4_s2,c4_s3,c4_s4,c4_s5,c4_s6,
        c5_s1,c5_s2,c5_s3,c5_s4,c5_s5,c5_s6,
        c6_s1,c6_s2,c6_s3,c6_s4,c6_s5,c6_s6,
                                c8_s4,c8_s5,
        mo1,mo2,encoder_counter,
        counter,temp,wIdx,rIdx,tailsymb,
        file_index,timestamp,packet_len,file_pos"""

print "insert into data(%s) select %s from db1.enc" % (sql,sql)

con.execute("insert into data(%s) select %s from db1.enc" % (sql,sql))

sql= """pre,bid,mid,len,
        accx, accy, accz, magx, magy, magz, gyrx,gyry,gyrz,temp,
        Press,bPrs,ITOW,LAT,LON,ALT,VEL_N,VEL_E,VEL_D,
        Hacc,Vacc,Sacc,bGPS,TS,Status,CS,
        counter,wIdx,rIdx,tailsymb,
        file_index,timestamp,packet_len,file_pos"""

con.execute("insert into data (%s) select %s from db2.inu" % (sql,sql))
con.commit()