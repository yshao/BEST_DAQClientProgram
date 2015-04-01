import glob
import os
import shutil
import time
import sqlite3
from common.env import Env
# from common.utils import get_timestamp
# from daqmanager.client.ftpfunc import ftp_list, ftp_download, ftp_delete, touch, ftp_upload
from daqmanager.client.utils import tm_to_epoch
from daqmanager.decoder.DecodeEncTask3 import DecodeEncTask
from daqmanager.decoder.DecodeInuTask import DecodeInuTask
from daqmanager.decoder.DecodeRadTask import DecodeRadTask

import pandas.io.sql as psql
import numpy as np


class Dataset():
    def __init__(self,fp):
        self.path=fp
        self.basetm=os.path.basename(fp)
        cfg=Env().getConfig()
        self.local=cfg['local_dir']

        ### builds dataset attributes ###
        print 'folder %s' % self.path
        datap='%s/%s' % (self.path,'data')
        for d in glob.glob('%s/**' % datap):
            if os.stat(d).st_size < 16:
                os.remove(d)

        self.scan_files()
        self.scan_buffers()

        local=self.path
        datap='%s/%s' % (local,'dataset.db')
        self.datap=datap

        self.inuGroup=[]
        self.encGroup=[]
        self.radGroup=[]

    def make_stats(self):
        ""

        ### file tm ###
        self.basetm=os.path.splitext(os.path.basename())[0]

        d={}
        self.filestats=d
        ### decode ###

        ### time sync ###

    def log(fliep,a):
      with open(fliep) as fh:
        for l in a:
          fh.write(l)

    def read_stats(self,lFiles):
        ""
        l=[]
        for f in lFiles:
            st=os.stat(f)
            # st.st_ctime
            # st.st_mtime
            d={}
            d[f]={}
            d[f]['ctime']=st.st_ctime
            d[f]['mtime']=st.st_mtime

            ### time from filename ###
            EPOCH2000 = tm_to_epoch('20000101_000000','%Y%m%d_%H%M%S')
            name=os.path.splitext(os.path.basename(f))[0]
            tm=tm_to_epoch(name,'%Y%m%d_%H%M%S')
            tmFile=(tm - EPOCH2000) * 1000
            d[f]['tm']=tmFile
            print d
            l.append(d)

        # print
        return l

    def scan_files(self):
        ""
        base=self.path
        scannedFiles=glob.glob('%s/data/**' %base)

        # print np.sort([f for f in scannedFiles if f.endswith('imu')])
        # print np.sort([f for f in scannedFiles if f.endswith('enc')])

        self.inuGroup=self.read_stats(np.sort([f for f in scannedFiles if f.endswith('imu')]))
        self.encGroup=self.read_stats(np.sort([f for f in scannedFiles if f.endswith('enc')]))
        self.radGroup=self.read_stats(np.sort([f for f in scannedFiles if f.endswith('rad')]))

    def scan_buffers(self):
        ""
        base=self.path
        scannedFiles=glob.glob('%s/buffers/**' %base)
        self.inuRecGroup=self.read_stats(np.sort([f for f in scannedFiles if f.endswith('recI')]))
        self.encRecGroup=self.read_stats(np.sort([f for f in scannedFiles if f.endswith('recE')]))
        self.rad22RecGroup=self.read_stats(np.sort([f for f in scannedFiles if f.endswith('recR22')]))

    # def make_fullfile(self):
    #   # tm=self.tm
    #   fullfilep=self.basetm
    #
    #   lStats=[]
    #   lFiles=self.scan_files()
    #
    #   ### inu group ###
    #   lFiles=self.inuGroup
    #   for f in lFiles:
    #     lStats.append(f)
    #     file(fullfilep+'.inu','wb').write(file(f,'rb').read())
    #   ### enc group ###
    #   lFiles=self.encGroup
    #   for f in lFiles:
    #     lStats.append(f)
    #     file(fullfilep+'.enc','wb').write(file(f,'rb').read())
    #
    #   self.filetm=lStats
      # self.log(lStats)

    def write_log(self):
        ""
        logname=self.basetm+'.log'
        with open(logname,'wb') as fh:
            fh.write(self.files)
            fh.write(self.filem)
            fh.write(self.bufferp)
            fh.write(self.res)


    def interp_time(self,bufferp,tmFile):
        ### interpolate Enc###
        if bufferp.endswith('recE'):
            # bufferp=rec.keys()[0]
            # print bufferp
            con = sqlite3.connect(bufferp)
            con.execute('update enc set counter=? where rowId=1',(tmFile,))
            con.commit()
            with con:
                dr = psql.frame_query("SELECT counter from enc", con)

            dr.fillna(np.nan)

            aTime=np.array(dr.interpolate())
            mlist=[(val[0],i+1) for i,val in enumerate(aTime)]
            con.executemany('UPDATE enc SET counter=? WHERE rowId=?', mlist)
            con.commit()

        ### interpolate Inu###
        if bufferp.endswith('recI'):
            # print bufferp
            ### create secondary buffer ###
            con = sqlite3.connect(bufferp)
            buffer2p=bufferp+'1'
            try:
                os.remove(buffer2p)
            except:
                pass
            shutil.copy('../../common/daq.db',buffer2p)

            con.execute("attach database '%s' as recI1" % buffer2p)
            con.execute("attach database '%s' as db1" % bufferp)

            sql_con="""select * from(select * from db1.inu where counter < (select counter from db1.inu where rowid =
(select max(rowid) from db1.inu where counter is not null)) or counter is null) where CS != 0 order by file_pos
            """
            con.execute("insert into recI1.inu %s" % sql_con).fetchall()
            con.commit()

            ### interpolate ###
            con = sqlite3.connect(buffer2p)
            con.execute('update inu set counter=? where rowId=1',(tmFile,))
            con.commit()
            with con:
                dr = psql.frame_query("SELECT counter  from inu", con)

            # s=pd.Series(dr)
            dr.fillna(np.nan)
            aTime=np.array(dr.interpolate())
            mlist=[(val[0],i+1) for i,val in enumerate(aTime)]

            con.executemany('UPDATE inu SET counter=? WHERE rowId=?', mlist)
            con.commit()

        ### interpolate Rad###
        # ext=os.path.splitext(os.path.basename(bufferp))[1]
        if bufferp.endswith('recR22'):
            con = sqlite3.connect(bufferp)
            con.execute('update rad set counter=? where rowId=1',(tmFile,))
            con.commit()

            with con:
                dr = psql.frame_query("SELECT counter  from rad", con)

            # s=pd.Series(dr)
            dr.fillna(np.nan)
            aTime=np.array(dr.interpolate())
            mlist=[(val[0],i+1) for i,val in enumerate(aTime)]

            con.executemany('UPDATE rad SET counter=? WHERE rowId=?', mlist)
            con.commit()


    def merge_buffer(self,bufferp):
        datap=self.datap
        con = sqlite3.connect(datap)
        recp=bufferp
        # print recp
        if recp.endswith('recE'):
            con.execute("attach database '%s' as db1" % recp)

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

            con.execute("insert into data(%s) select %s from db1.enc" % (sql,sql))

        if recp.endswith('recI'):
            con.execute("attach database '%s1' as db2" % recp)
            sql= """pre,bid,mid,len,
                    accx, accy, accz, magx, magy, magz, gyrx,gyry,gyrz,temp,
                    Press,bPrs,ITOW,LAT,LON,ALT,VEL_N,VEL_E,VEL_D,
                    Hacc,Vacc,Sacc,bGPS,TS,Status,CS,
                    counter,wIdx,rIdx,tailsymb,
                    file_index,timestamp,packet_len,file_pos"""

            con.execute("insert into data (%s) select %s from db2.inu" % (sql,sql))

        if recp.endswith('recR22'):
            con.execute("attach database '%s' as db3" % recp)
            sql= """ch1,ch2,ch3,ch4,ch5,ch6,ch7,ch8,ch9,ch10,ch11,ch12,hKey,
        ch13,ch14,ch15,ch16,ch17,ch18,ch19,ch20,ch21,ch22,ch23,ch24,
        counter,temp,wIdx,rIdx,tailsymb,
        file_index,timestamp,packet_len,file_pos"""

            con.execute("insert into data (%s) select %s from db3.rad" % (sql,sql))

        con.commit()

    def sync(self):
        datap=self.datap

        print datap
        old=datap+'unsort'
        print old
        try:
            os.rename(datap,old)
            os.remove(datap)
        except:
            pass

        shutil.copy('../../common/daq.db',datap)
        con = sqlite3.connect(datap)


        # recp=bufferp
        con.execute("attach database '%s' as dbmain" % old)
        con.execute("insert into data select * from dbmain.data where counter is not null order by counter")
        con.commit()

        try:
            os.remove(old)
        except:
            pass



    def decode_folder(self):
        encGroup=self.encGroup
        inuGroup=self.inuGroup
        radGroup=self.radGroup
        local=self.local

        # self.lo

        fdrp=self.path
        print 'decoding %s' % fdrp
        fdrp=fdrp+'/buffers'
        try:
            os.mkdir(fdrp)
        except:
            pass

        ### decode all enc ###
        # for i,f in enumerate(encGroup):
        #     fp=f.keys()[0]
        #     basename=os.path.splitext(os.path.basename(fp))[0]
        #     recname='%s.recE' % basename
        #     recp='%s/%s' % (fdrp,recname)
        #     shutil.copy('../../common/daq.db',recp)
        #     # shutil.copy('../../common/daq.db',recp)
        #
        #     task=DecodeEncTask(recp)
        #     task.parse_enc(fp,i)

        ### decode all inu ###
        for i,f in enumerate(inuGroup):
            fp=f.keys()[0]
            basename=os.path.splitext(os.path.basename(fp))[0]
            recname='%s.recI' % basename
            recp='%s/%s' % (fdrp,recname)
            shutil.copy('../../common/daq.db',recp)

            task=DecodeInuTask(recp)
            task.parse_inu(fp,i)

        ### decode all rad ###
        for i,f in enumerate(radGroup):
            fp=f.keys()[0]
            basename=os.path.splitext(os.path.basename(fp))[0]
            recname='%s.recR22' % basename
            recp='%s/%s' % (fdrp,recname)
            shutil.copy('../../common/daq.db',recp)

            task=DecodeRadTask(recp)
            task.parse_rad(fp,i)

        self.scan_buffers()

    def create_dataset(self):
        local=self.path
        datap='%s/%s' % (local,'dataset.db')
        self.datap=datap
        # print 'DATASET',self.datap
        shutil.copy('../../common/daq.db',datap)

        for b in self.encRecGroup:
            file=b.keys()[0]
            # fileb=b[0]
            # self.interp_time(file,b[file]['tm'])
            self.merge_buffer(file)

        for b in self.inuRecGroup:
            file=b.keys()[0]
            # self.interp_time(file,b[file]['tm'])
            # print b
            self.merge_buffer(file)

        for b in self.rad22RecGroup:
            file=b.keys()[0]
            # self.interp_time(file,b[file]['tm'])
            # print b
            self.merge_buffer(file)

        self.sync()

    def interp_dataset(self):

        local=self.path
        datap='%s/%s' % (local,'dataset.db')
        self.datap=datap
        # print 'DATASET',self.datap
        shutil.copy('../../common/daq.db',datap)

        for b in self.encRecGroup:
            file=b.keys()[0]
            # fileb=b[0]
            self.interp_time(file,b[file]['tm'])
            # self.merge_buffer(file)

        for b in self.inuRecGroup:
            file=b.keys()[0]
            self.interp_time(file,b[file]['tm'])
            # print b
            # self.merge_buffer(file)

        for b in self.rad22RecGroup:
            file=b.keys()[0]
            self.interp_time(file,b[file]['tm'])
            # print b
            # self.merge_buffer(file)

