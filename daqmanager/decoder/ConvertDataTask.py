import struct
import os
from PyQt4.QtCore import pyqtSignal, SIGNAL, QThread
from best.common.sqliteutils import DaqDB
import itertools
from datautils import *
import pandas.io.sql as sql
from best.common.sqliteutils import *
from best.daqmanager.tasks.helpers.convert_data import *

class ConvertDataTask(QThread):
    encdb="../enc.db"
    raddb="../rad.db"
    inudb="../inu.db"

    def __del__(self):
        ""
        # self.db.close()

    def __init__(self):
        ""
        QThread.__init__(self)
        self.db=DaqDB("../daq.db")

    # def load_data(self,query):
    #     conn = pyodbc.connect('DRIVER={SQL Server};SERVER=MyServer;Trusted_Connection=yes;')
    #     cur = conn.cursor()
    #     cur.execute('select object_id from sys.objects')
    #     results = cur.fetchall()
    #     results_as_list = [i[0] for i in results]
    #     array = numpy.fromiter(results_as_list, dtype=numpy.int32)
    #
    #     #data = numpy.array(curs.fetchall(),dtype=float)
    #     return array

    def convert(self,type):
        ""
        if type == "rad":
            self.rad_conv()
        elif type == "enc":
            self.enc_conv()
            # self.hum_conv()

        elif type == "inu":
            self.inu_conv()




    def get_enc_init(self,ch):
        ""
        # db.close

        daq=sqlite3.connect("../daq.db")

        chq='c%s_c1, c%s_c2, c%s_c3, c%s_c4, c%s_c5, c%s_c6' % (ch,ch,ch,ch,ch,ch)
        q="select %s from calib" % chq
        print q
        cursor = daq.cursor().execute(q)
        cdata=cursor.fetchall()[0]
        # columns = [column[0] for column in cursor.description]

        # results = []
        # for row in cursor.fetchall():
        #     results.append(dict(zip(columns, row)))

        # print results

        daq.close()

        return cdata


    def hum_conv(self):
        ""
        db=sqlite3.connect("../daq.db")
        encdb=sqlite3.connect("../enc.db")

        ### P1 ###
        H1=sql.read_sql("select c1_s4 from enc where c1_s4 != \"\"",encdb)
        H1=H1.astype(int)
        H1=H1.interpolate()

        T1=sql.read_sql("select c1_s5 from enc where c1_s5 != \"\"",encdb)
        T1=T1.astype(int)
        T1=T1.interpolate()

        res=convert_SHT_data(H1,T1)
        res=res.ix[:,("RHi","T")]
        res.rename(columns={'$RHi': 'H1', '$T': 'T1'}, inplace=True)

        sql.to_sql(res,'converted1h',db,flavor='sqlite')

        ### P2 ###
        H2=sql.read_sql("select c2_s4 from enc where c2_s4 != \"\"",encdb)
        H2=H2.astype(int)
        H2=H2.interpolate()

        T2=sql.read_sql("select c2_s5 from enc where c2_s5 != \"\"",encdb)
        T2=T2.astype(int)
        T2=T2.interpolate()

        res=convert_SHT_data(H2,T2)
        res=res.ix[:,("RHi","T")]
        res.rename(columns={'$RHi': 'H2', '$T': 'T2'}, inplace=True)

        sql.to_sql(res,'converted2h',db,flavor='sqlite')

        ### P3 ###
        H3=sql.read_sql("select c3_s4 from enc where c3_s4 != \"\"",encdb)
        H3=H3.astype(int)
        H3=H3.interpolate()

        T3=sql.read_sql("select c3_s5 from enc where c3_s5 != \"\"",encdb)
        T3=T3.astype(int)
        T3=T3.interpolate()

        res=convert_SHT_data(H3,T3)
        res=res.ix[:,("RHi","T")]
        res.rename(columns={'$RHi': 'H3', '$T': 'T3'}, inplace=True)

        sql.to_sql(res,'converted3h',db,flavor='sqlite')

        ### P4 ###
        H4=sql.read_sql("select c4_s4 from enc where c4_s4 != \"\"",encdb)
        H4=H4.astype(int)
        H4=H4.interpolate()

        T4=sql.read_sql("select c4_s5 from enc where c4_s5 != \"\"",encdb)
        T4=T4.astype(int)
        T4=T4.interpolate()

        res=convert_SHT_data(H4,T4)
        res=res.ix[:,("RHi","T")]
        res.rename(columns={'$RHi': 'H4', '$T': 'T4'}, inplace=True)

        sql.to_sql(res,'converted4h',db,flavor='sqlite')

        ### P5 ###
        H5=sql.read_sql("select c5_s4 from enc where c5_s4 != \"\"",encdb)
        H5=H5.astype(int)
        H5=H5.interpolate()

        T5=sql.read_sql("select c5_s5 from enc where c5_s5 != \"\"",encdb)
        T5=T5.astype(int)
        T5=T5.interpolate()

        res=convert_SHT_data(H5,T5)
        res=res.ix[:,("RHi","T")]
        res.rename(columns={'$RHi': 'H5', '$T': 'T5'}, inplace=True)

        sql.to_sql(res,'converted5h',db,flavor='sqlite')

        ### P6 ###
        H6=sql.read_sql("select c6_s4 from enc where c6_s4 != \"\"",encdb)
        H6=H6.astype(int)
        H6=H6.interpolate()

        T6=sql.read_sql("select c6_s5 from enc where c6_s5 != \"\"",encdb)
        T6=T6.astype(int)
        T6=T6.interpolate()

        res=convert_SHT_data(H6,T6)
        res=res.ix[:,("RHi","T")]
        res.rename(columns={'$RHi': 'H6', '$T': 'T6'}, inplace=True)

        sql.to_sql(res,'converted6h',db,flavor='sqlite')


    def enc_conv(self):
        ""
        db=sqlite3.connect("../daq.db")

        encdb=sqlite3.connect("../enc.db")
        # C=self.get_enc_init()

        CVAL1=self.get_enc_init('1')
        CVAL1=map(int,CVAL1)

        CVAL2=self.get_enc_init('2')
        CVAL2=map(int,CVAL2)

        CVAL3=self.get_enc_init('3')
        CVAL3=map(int,CVAL3)

        CVAL4=self.get_enc_init('4')
        CVAL4=map(int,CVAL4)

        CVAL5=self.get_enc_init('5')
        CVAL5=map(int,CVAL5)

        CVAL6=self.get_enc_init('6')
        CVAL6=map(int,CVAL6)



        ### P1 ###
        P1=sql.read_sql("select c1_s6 from enc where c1_s6 != \"\"",encdb)
        P1=P1.astype(int)
        P1=P1.interpolate()

        T1=sql.read_sql("select c1_s2 from enc where c1_s2 != \"\"",encdb)
        T1=T1.astype(int)
        T1=T1.interpolate()

        res=convert_MS_data(P1,T1,CVAL1)
        res=res.ix[:,("TEMP","P")]
        res.rename(columns={'$TEMP': 'T1', '$P': 'P1'}, inplace=True)

        sql.to_sql(res,'converted1',db,flavor='sqlite')

        ### P2 ###
        P2=sql.read_sql("select c2_s6 from enc where c2_s6 != \"\"",encdb)
        P2=P2.astype(int)
        P2=P2.interpolate()

        T2=sql.read_sql("select c2_s2 from enc where c2_s2 != \"\"",encdb)
        T2=T2.astype(int)
        T2=T2.interpolate()

        res=convert_MS_data(P2,T2,CVAL2)
        res=res.ix[:,("TEMP","P")]
        res.rename(columns={'$TEMP': 'T2', '$P': 'P2'}, inplace=True)

        sql.to_sql(res,'converted2',db,flavor='sqlite')

        ### P3 ###
        P3=sql.read_sql("select c3_s6 from enc where c3_s6 != \"\"",encdb)
        P3=P3.astype(int)
        P3=P3.interpolate()

        T3=sql.read_sql("select c3_s2 from enc where c3_s2 != \"\"",encdb)
        T3=T3.astype(int)
        T3=T3.interpolate()

        res=convert_MS_data(P3,T3,CVAL3)
        res=res.ix[:,("TEMP","P")]
        res.rename(columns={'$TEMP': 'T3', '$P': 'P3'}, inplace=True)

        sql.to_sql(res,'converted3',db,flavor='sqlite')


        ### P4 ###
        P4=sql.read_sql("select c4_s6 from enc where c4_s6 != \"\"",encdb)
        P4=P4.astype(int)
        P4=P4.interpolate()

        T4=sql.read_sql("select c4_s2 from enc where c4_s2 != \"\"",encdb)
        T4=T4.astype(int)
        T4=T4.interpolate()

        res=convert_MS_data(P4,T4,CVAL4)
        res=res.ix[:,("TEMP","P")]
        # print res.columns=['T5','P5']
        res.rename(columns={'$TEMP': 'T4', '$P': 'P4'}, inplace=True)
        # print res

        sql.to_sql(res,'converted4',db,flavor='sqlite')


        ### P5 ###
        P5=sql.read_sql("select c5_s6 from enc where c5_s6 != \"\"",encdb)
        P5=P5.astype(int)
        P5=P5.interpolate()

        T5=sql.read_sql("select c5_s2 from enc where c5_s2 != \"\"",encdb)
        T5=T5.astype(int)
        T5=T5.interpolate()

        res=convert_MS_data(P5,T5,CVAL5)
        res=res.ix[:,("TEMP","P")]
        # print res.columns=['T5','P5']
        res.rename(columns={'$TEMP': 'T5', '$P': 'P5'}, inplace=True)

        sql.to_sql(res,'converted5',db,flavor='sqlite')

        print res

        ### P6 ###
        P6=sql.read_sql("select c5_s6 from enc where c5_s6 != \"\"",encdb)
        P6=P5.astype(int)
        P6=P5.interpolate()

        T6=sql.read_sql("select c5_s2 from enc where c5_s2 != \"\"",encdb)
        T6=T5.astype(int)
        T6=T5.interpolate()

        res=convert_MS_data(P6,T6,CVAL6)
        res=res.ix[:,("TEMP","P")]
        res.rename(columns={'$TEMP': 'T6', '$P': 'P6'}, inplace=True)

        sql.to_sql(res,'converted6',db,flavor='sqlite')



    def rad_conv(self):
        pd[0:24]=pd[0:24] * 2500/2**12


    def inu_conv(self):
        ""



task=ConvertDataTask()
task.convert("enc")