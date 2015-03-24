import copy
import glob
import os
from common.env import Env
from common.sqliteutils import DaqDB
from daqmanager.client.utils import tm_to_epoch
import numpy as np
import pandas as pd

__company__ = 'Boulder Environmental Sciences and Technology'
__project__ = ''
__author__ = 'Y. Shao'
__created__ = '3/23/2015' '11:13 AM'

class DatasetDB(DaqDB):
    def __init__(self,filep):
        ""
        # print filep
        super(DatasetDB,self).__init__(filep)
        # print self.connection

class Dataset():
  def __init__(self,fdrp):
    # dataset=
    homepathp=Env().getParam()['HOME']
    cfg=Env().getConfig()
    # print homepathp
    self.fdr='%s/%s' %(cfg['local_dir'],fdrp)
    print self.fdr
    bufferp='%s/%s' % (self.fdr,'dataset.db')
    # print bufferp
    # print 'DBD'
    db=DatasetDB(bufferp)
    print 'A'
    self.db=db



  def make_time_axis(self,f):
    self.timedb=DaqDB('inu.db')
    print 'MAKE'
    # filename=timedb.select('select filename from decoder').fetchall()[0]
    filem=os.path.basename(f).replace('inu.db','')
    base_tm=tm_to_epoch(filem,'%Y%m%d_%H%M%S')
    print 'MAKE'
    aTime=self.calc_offsets()
    aTime = aTime/1000 + base_tm
    print aTime
    self.db.insert_record(aTime)


  def calc_offsets(self):
        ""
        import pandas.io.sql as psql
        print self.timedb.connection
        with self.timedb.connection:
            sql = "SELECT CS,counter from inu where CS != ''"
            df = psql.frame_query(sql, self.timedb.connection)

        p=pd.DataFrame(range(0,256))
        nn=np.zeros([256,1])
        nd=np.array(df['CS'])
        nt=np.array(df['counter'])

        ndiff =np.diff(nd)

        ndd=np.where(ndiff < 0)[0]
        mpad=ndd.shape[0]
        nnm=np.empty([0,1])

        aDiffIdx=np.hstack((np.zeros(1),ndd,np.array(nd.shape[0])))
        for n in range(0,mpad):
            st=aDiffIdx[n];end=aDiffIdx[n+1]

        newA=copy.copy(nn)
        for i in range(int(st),int(end+1)):
            tm=nt[i]
            csIdx=nd[i]
            # print i,csIdx,tm

            newA[csIdx,0]=csIdx
            newA[csIdx,1]=tm

        nnm=np.vstack((nnm,newA))
        return nnm


  def get_decode_buffers(self):
      ""
      self.decodeFile=glob.glob('%s/**/buffer/**'%(self.fdr))
      # print 'abc'.endswith('c')
      print self.decodeFile
      for f in self.decodeFile:
          print f.endswith('imu')
      self.inuFile=[f for f in self.decodeFile if f.endswith('inu.db')]
      print self.inuFile

  def join_datasets(self,f):
      # decodeCfg=open_decode_result()
      buffer=DaqDB(f).connect()
      if f == '.inu':
          q='select * from inu'
          data=buffer.select(q)
      if f == '.enc':
          q='select * from enc'
          data=buffer.select(q)
      if f == 'rad':
          q='select * from rad'
          data=buffer.select(q)

      timedb=self.timedb

      timedb.insert(data)

  def run(self):
    ### read buffers
    self.get_decode_buffers()

    print self.inuFile
    print self.decodeFile


    for inu in self.inuFile:
    ### create offset reference
        print inu
        self.make_time_axis(inu)

    for f in self.decodeFile:
        self.join_datasets(f)

if __name__ == '__main__':
    ### folder name
    ds=Dataset('1426610662')
    ds.run()


