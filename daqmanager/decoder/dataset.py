import glob
import os
import shutil
import time
import sqlite3
import pandas
import numpy as np
from common.env import Env
from common.utils import get_timestamp
from daqmanager.client.ftpfunc import ftp_list, ftp_download, ftp_delete, touch, ftp_upload
from daqmanager.decoder.DecodeEncTask3 import DecodeEncTask
from daqmanager.decoder.DecodeInuTask import DecodeInuTask


class Dataset():
    def __init__(self,fp):
        self.path=fp
        self.basetm=os.path.basename(fp)
        cfg=Env().getConfig()
        self.local=cfg['local_dir']

        ### builds dataset attributes ###
        self.scan_files()

        # self.decode_folder()

        self.scan_buffers()

        self.create_dataset()

        # self.write_log()
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
            l.append(d)

        return l

    def scan_files(self):
        ""
        base=self.path
        scannedFiles=glob.glob('%s/data/**' %base)

        # print np.sort([f for f in scannedFiles if f.endswith('imu')])
        # print np.sort([f for f in scannedFiles if f.endswith('enc')])

        self.inuGroup=self.read_stats(np.sort([f for f in scannedFiles if f.endswith('imu')]))
        self.encGroup=self.read_stats(np.sort([f for f in scannedFiles if f.endswith('enc')]))

    def scan_buffers(self):
        ""
        base=self.path
        scannedFiles=glob.glob('%s/buffers/**' %base)
        self.inuRecGroup=self.read_stats(np.sort([f for f in scannedFiles if f.endswith('recI')]))
        self.encRecGroup=self.read_stats(np.sort([f for f in scannedFiles if f.endswith('recE')]))

    def merge_all_datasets(self):
        ""


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


    def interp_time(self,bp):
        import pandas.io.sql as psql

        # local='c:/datasets/buffer'
        # bufferp='%s/%s' % (local,'20000101_000204.recE')
        # db=DaqDB(bufferp)
        ### interpolate ###
        bufferp=bp

        if bufferp.endswith('recE'):
            con = sqlite3.connect(bufferp)
            # print bufferp
            with con:
                dr = psql.frame_query("SELECT counter from enc", con)
            s=pandas.Series(dr)
            dr.fillna(np.nan)

            aTime=np.array(dr.interpolate())
            mlist=[(val[0],i+1) for i,val in enumerate(aTime)]
            con.executemany('UPDATE enc SET counter=? WHERE rowId=?', mlist)

            con.commit()

        elif bufferp.endswith('recI'):
            ### create secondary buffer ###
            con = sqlite3.connect(bufferp)
            buffer2p=bufferp+'1'
            try:
                os.remove(buffer2p)
            except:
                pass

            shutil.copy('daq.db',buffer2p)


            con.execute("attach database '%s' as recI1" % buffer2p)
            con.execute("attach database '%s' as db1" % bufferp)
            res=con.execute('select * from recI1.calib').fetchall()
            # res=con.fetchall()
            # for s in res:
            #     print s

            sql_con="select * from db1.inu where counter < (select counter from inu where rowid =(select max(rowid) from inu)) order by file_pos"

            res=con.execute("insert into recI1.inu %s" % sql_con).fetchall()
            # res=con.fetchall()
            # print len(res)
            # for s in res:
            #     print s


            # res=con.execute("select * from recI1.calib").fetchall()
            con = sqlite3.connect(buffer2p)

            ### interpolate ###
            import numpy as np
            import pandas as pd

            with con:
                dr = psql.frame_query("SELECT counter  from inu", con)

            # local='c:/datasets/buffer'
            # buffer2p='%s/%s' % (local,'20000101_000203.recI')
            # db=DaqDB(bufferp)

            #
            s=pd.Series(dr)
            dr.fillna(np.nan)
            aTime=np.array(dr.interpolate())
            mlist=[(val[0],i+1) for i,val in enumerate(aTime)]
            #
            # print mlist[0:100]
            con.executemany('UPDATE inu SET counter=? WHERE rowId=?', mlist)
            con.commit()



    def merge_buffer(self,recp):
        cfg=Env().getConfig()
        local='c:/datasets/buffer'
        datap='%s/%s' % (local,'dataset.db')

        shutil.copy('daq.db',datap)

        con = sqlite3.connect(datap)

        if recp['ext'] == 'recE':
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



        if recp['ext'] == 'recI':
            con.execute("attach database '%s' as db2" % recp)
            sql= """pre,bid,mid,len,
                    accx, accy, accz, magx, magy, magz, gyrx,gyry,gyrz,temp,
                    Press,bPrs,ITOW,LAT,LON,ALT,VEL_N,VEL_E,VEL_D,
                    Hacc,Vacc,Sacc,bGPS,TS,Status,CS,
                    counter,wIdx,rIdx,tailsymb,
                    file_index,timestamp,packet_len,file_pos"""

            con.execute("insert into data (%s) select %s from db2.inu" % (sql,sql))


        con.commit()

    def decode_folder(self):
        encGroup=self.encGroup
        inuGroup=self.inuGroup
        local=self.local

        # self.lo

        fdrp=self.path
        print 'decoding %s' % fdrp
        fdrp=fdrp+'/buffers'
        try:
            os.mkdir(fdrp)
        except:
            pass

        for i,f in enumerate(encGroup):
            fp=f.keys()[0]
            basename=os.path.splitext(os.path.basename(fp))[0]
            recname='%s.recE' % basename
            recp='%s/%s' % (fdrp,recname)
            shutil.copy('../../common/daq.db',recp)
            # shutil.copy('../../common/daq.db',recp)

            task=DecodeEncTask(recp)
            task.parse_enc(fp,i)
        #
        for i,f in enumerate(inuGroup):
            fp=f.keys()[0]
            basename=os.path.splitext(os.path.basename(fp))[0]
            recname='%s.recI' % basename
            recp='%s/%s' % (fdrp,recname)
            shutil.copy('../../common/daq.db',recp)

            task=DecodeInuTask(recp)
            task.parse_inu(fp,i)

        self.scan_buffers()

    def create_dataset(self):

        # lBuffers=self.scan_buffers()
        # print lBuffers
        for b in self.encRecGroup:
            file=b.keys()[0]
            self.interp_time(b)
            self.merge_buffer(b)

        for b in self.inuRecGroup:
            self.interp_time(b)
            self.merge_buffer(b)
