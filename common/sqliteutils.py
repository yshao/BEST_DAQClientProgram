#from astropy.io import fits
import sqlite3
import os
import glob
import numpy as np
from astropy import log

# from dr2 import constants

DB_DIR="../daqmanager"
DB_NAME="daq.db"

import shutil as sl
import pandas as pd

def convert_timestamp(systemtime):
    new_time = list (systemtime)
    return new_time


class DaqDB(object):

    def __del__(self):
        self.connection.cursor()

    def __init__(self, filename):
        # sqlite doesn't know how to handle certain numpy types unless told
        sqlite3.register_adapter(np.int8, bool)
        sqlite3.register_adapter(np.int16, int)
        sqlite3.register_adapter(np.int32, int)
        sqlite3.register_adapter(np.float32, float)
        sqlite3.register_adapter(bool, int)
        #sqlite3.register_converter("BOOLEAN", lambda v: bool(int(v)))
        
        self.filename = filename
        self.connection = sqlite3.connect(self.filename,
                                          isolation_level='EXCLUSIVE')

        self.connection.text_factory = str
        self.cursor = self.connection.cursor()
        self.optimise_inserts()
        # self.insert_init()


    # def __del__(self):
    #     self.connection.close()

    def get_connection(self):
        return self.connection

    def commit(self):
        self.connection.commit()

    def optimise_inserts(self):
        """Optimise the cursor for bulk inserts
        Inspired by http://blog.quibb.org/2010/08/fast-bulk-inserts-into-sqlite/
        """
        self.cursor.execute('PRAGMA synchronous=OFF')
        self.cursor.execute('PRAGMA count_changes=OFF')
        self.cursor.execute('PRAGMA journal_mode=MEMORY')
        self.cursor.execute('PRAGMA temp_store=MEMORY')
        self.cursor.execute('PRAGMA locking_mode=EXCLUSIVE')
        # self.cursor.execute('PRAGMA journal_mode=WAL')

    def create_table(self, name, columns):
        coldef = "('"+"', '".join(columns)+"')"
        self.cursor.execute("CREATE TABLE IF NOT EXISTS {0} {1}".format(name, coldef))

    # def create_indexes(self):
    #     self.cursor.execute("PRAGMA temp_store=FILE")
    #     # self.cursor.execute("PRAGMA temp_store_directory='{0}'".format(constants.TMPDIR))
    #     self.cursor.execute("PRAGMA cache_size = '2000000'")
    #     log.info('Now indexing (ra, dec)')
    #     self.cursor.execute('CREATE INDEX iphas_ra_dec_idx ON iphas(ra, dec)')
    #     log.info('Now indexing (l, b)')
    #     self.cursor.execute('CREATE INDEX iphas_l_b_idx ON iphas(l, b)')

    def insert_ndarray(self, table,data, columns):
        log.info('Ingesting data')
        self.cursor.executemany('INSERT INTO '+table+' VALUES ('
                                + ','.join(['?']*len(columns)) + ')',
                                data)        



    # def insert_fits(self, filename, columns):
    #     log.info('Ingesting {0}'.format(filename))
    #     # Using .__array__() is important for speed
    #     data = fits.getdata(filename, 1).__array__()
    #     # Correct boolean columns for the silly way in which FITS stores bools
    #     for field in ['brightNeighb', 'deblend', 'saturated', 'reliable']:
    #         data[field][data[field] == ord('T')] = 1
    #         data[field][data[field] == ord('F')] = 0
    #     # Insert
    #     self.cursor.executemany('INSERT INTO iphas VALUES ('
    #                             + ','.join(['?']*len(columns)) + ')',
    #                             data)

    def insert_raws(self, table, columns, data):
        # log.info('Ingesting {0}'.format(filename))
        # Using .__array__() is important for speed
        # data = fits.getdata(filename, 1).__array__()


        # Correct boolean columns for the silly way in which FITS stores bools
        # for field in ['brightNeighb', 'deblend', 'saturated', 'reliable']:
        #     data[field][data[field] == ord('T')] = 1
        #     data[field][data[field] == ord('F')] = 0
        # Insert
        # cursor.executemany('''insert into data values (?, ?, ?, ?)''', map(tuple, data.tolist()))
        # print ('INSERT INTO '+table+' VALUES (' + ','.join(['?']*len(columns)) + ')' ) % data
        self.cursor.executemany('INSERT INTO '+table+' VALUES ('
                                + ','.join(['?']*len(columns)) + ')',
                                data)

    def insert_dict(self, table, my_dict):
            "Create a insert statememnt"
            columns = ', '.join(my_dict.keys())
            placeholders = ':'+', :'.join(my_dict.keys())
            query = 'INSERT INTO '+table+' (%s) VALUES (%s)' % (columns, placeholders)
            self.cursor.execute(query, my_dict)

    # def check_avail(self):
    #     return True


    # def update_joins(self):
    #     ""
    #     stmt='INSERT * SELECT * FROM inu SELECT * FROM enc SELECT * FROM rad' \
    #          '  INTO data'
    #     print stmt

    # def view_streams_window(self,start_time,end_time):
    #     ""
    #     stmt='SELECT * FROM data WHERE timestamp > %s AND timestamp < %s' % start_time,end_time
    #     print stmt
    #     self.cursor.execute('')

    def select_data(self,stmt):
        rs=self.cursor.execute(stmt)
        dr=rs.fetchall()
        return dr

    def load_pd_data(self,stmt):
        return pd.read_sql(stmt,self.connection)

    def close(self):
        self.connection.close

    def dump_tables(self):
        self.cursor.execute('select name from sqlite_master where type = "table"')
        print(self.cursor.fetchall())


def create_db_light(table,cols):
    ""
    print "creating table %s" % table
    print "creating columns %s" % cols

    db = DaqDB('daq.db')
    db.optimise_inserts()
    db.create_table(table, cols)
    db.commit()


# Press         - U2
# press stat    - U1
# ITOW          - U4
# LAT           - I4
# LON           - I4
# ALT           - I4
# VEL_N         - I4
# VEL_E         - I4
# VEL_D         - I4
# Hacc          - U4
# Vacc          - U4
# Sacc          - U4
# bGPS          - GPS
# TS            - U2

# Status    byte
#   CS      byte

INU_COL = ['pre','bid','mid','len',
        'accx', 'accy', 'accz', 'magx', 'magy', 'magz', 'gyrx', 'gyry', 'gyrz', 'temp',
        'Press','bPrs','ITOW','LAT','LON','ALT','VEL_N','VEL_E','VEL_D',
        'Hacc','Vacc','Sacc','bGPS','TS','Status','CS',
        'counter','wIdx','rIdx','tailsymb',
        'file_index','timestamp','packet_len'
       ]


RAD_COL = ['ch1','ch2','ch3','ch4','ch5','ch6','ch7','ch8','ch9','ch10','ch11','ch12','hKey',
        'ch13','ch14','ch15','ch16','ch17','ch18','ch19','ch20','ch21','ch22','ch23','ch24',
        'counter','temp','wIdx','rIdx','tailsymb',
        'file_index','timestamp','packet_len'
       ]

GPS_COL = ['pps','counter']




ENC_COL = ['c1_s1','c1_s2','c1_s3','c1_s4','c1_s5','c1_s6',
        'c2_s1','c2_s2','c2_s3','c2_s4','c2_s5','c2_s6',
        'c3_s1','c3_s2','c3_s3','c3_s4','c3_s5','c3_s6',
        'c4_s1','c4_s2','c4_s3','c4_s4','c4_s5','c4_s6',
        'c5_s1','c5_s2','c5_s3','c5_s4','c5_s5','c5_s6',
        'c6_s1','c6_s2','c6_s3','c6_s4','c6_s5','c6_s6',
                                'c8_s4','c8_s5',
        'mo1','mo2','encoder_counter',
        'counter','temp','wIdx','rIdx','tailsymb',
        'file_index','timestamp','packet_len'
        ]
### Session Table ###
SESSION_COL = [
    'sessionIdx',
    'startingTime',
    'endTime',
    'fileIndex',
    'fileName',
    'fileSize',
    'folderName',
    'recordsUploaded','recordsRejected',
]

ENC_INIT_COL = ['c1_c1','c1_c2','c1_c3','c1_c4','c1_c5','c1_c6',
        'c2_c1','c2_c2','c2_c3','c2_c4','c2_c5','c2_c6',
        'c3_c1','c3_c2','c3_c3','c3_c4','c3_c5','c3_c6',
        'c4_c1','c4_c2','c4_c3','c4_c4','c4_c5','c4_c6',
        'c5_c1','c5_c2','c5_c3','c5_c4','c5_c5','c5_c6',
        'c6_c1','c6_c2','c6_c3','c6_c4','c6_c5','c6_c6'
        ]


### Parser Diagnostics Table ###
DECODER_COL = ['file_name','file_index','bIdx','packet_len'



]


### Converted Level 1 Table ###
DATA_COL = [
    'raw_data_index',
    'calib_index',

    'p1', 'h1', 'pt1', 'ht1',
    'p2', 'h2', 'pt2', 'ht2',
    'p3', 'h3', 'pt3', 'ht3',
    'p4', 'h4', 'pt4', 'ht4',
    'p5', 'h5', 'pt5', 'ht5',
    'p6', 'h6', 'pt6', 'ht6',
          'h7',        'ht7',

    'ch1','ch2','ch3','ch4','ch5','ch6','ch7','ch8','ch9','ch10','ch11','ch12',
    'ch13','ch14','ch15','ch16','ch17','ch18','ch19','ch20','ch21','ch22','ch23','ch24',

    'r1ctrl1','r2ctrl2',
    'r1temp',

    'enc_degree',
    'quadrant',

    'posX','poxY','posZ',
    'vel'
    'lat','long','elevation',


    'cunter','time',
    ]


    ### init
def insert_init():
    db=DaqDB("daq.db")

    init = {
    'c1_c1':40695,'c1_c2':35411,'c1_c3':23713,'c1_c4':21714,'c1_c5':32532,'c1_c6':28824,

    'c2_c1':40200,'c2_c2':37500,    'c2_c3':23808,'c2_c4':23527,'c2_c5':31353,'c2_c6':28666,

    'c3_c1':40709,'c3_c2':36913,'c3_c3':23830,'c3_c4':23599,'c3_c5':30841,'c3_c6':28764,
    'c4_c1':40439,'c4_c2':36650,'c4_c3':23486,'c4_c4':22888,'c4_c5':31176,'c4_c6':28619,
    'c5_c1':40771,'c5_c2':38839,'c5_c3':23726,'c5_c4':24670,'c5_c5':30772 ,'c5_c6':28618,
    'c6_c1':41095,'c6_c2':36757,'c6_c3':23869,'c6_c4':22635,'c6_c5':32139,'c6_c6':28734
    }

    for key in init:
            print key
            init[key] = str(init[key])

    db.insert_dict('calib',init)
    db.commit()


def create_full():
    create_db_light("inu",INU_COL)
    create_db_light("gps",GPS_COL)
    create_db_light("rad",RAD_COL)
    create_db_light("enc",ENC_COL)
    create_db_light("calib",ENC_INIT_COL)
    create_db_light("session",SESSION_COL)
    create_db_light("decoder",DECODER_COL)
    insert_init()


    sl.move(DB_NAME,os.path.join(DB_DIR,DB_NAME))
    src=os.path.join(DB_DIR,DB_NAME)
    sl.copy(src,os.path.join(DB_DIR,"enc.db"))
    sl.copy(src,os.path.join(DB_DIR,"rad.db"))
    sl.copy(src,os.path.join(DB_DIR,"inu.db"))
    print os.path.join(DB_DIR,DB_NAME)

if __name__ == '__main__':
    # generate tables
# def create_db():
    # sl.rename(os.path.join(DB_DIR,DB_NAME),os.path.join(DB_DIR,DB_NAME+".bk"))

    create_full()




    # sl.move(DB_NAME,os.path.join(DB_DIR,DB_NAME))
    # src=os.path.join(DB_DIR,DB_NAME)
    # sl.copy(src,os.path.join(DB_DIR,"enc.db"))
    # sl.copy(src,os.path.join(DB_DIR,"rad.db"))
    # sl.copy(src,os.path.join(DB_DIR,"inu.db"))
    # print os.path.join(DB_DIR,DB_NAME)


