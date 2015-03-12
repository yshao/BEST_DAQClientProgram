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
        # self.optimise_inserts()

    def __del__(self):
        self.connection.close()

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

    def check_avail(self):
        return True


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


    def load_data(self,table):
        ""
        stmt="SELECT * from %s" % table
        print stmt
        rs=self.cursor.execute(stmt)
        dr=rs.fetchall()

        # rs = curs.execute(sql) #Send SQL-syntax to cursor
        # recs = rs.fetchall()  # All data are stored in recs
        # late fix for xy-plots
        format_rad = [('ch1_1', float), ('ch2_1', float),('ch3_1', float), ('ch4_1', float),
                  ('ch5_1', float), ('ch6_1', float),('ch7_1', float), ('ch8_1', float),
                  ('ch9_1', float), ('ch10_1', float),('ch11_1', float), ('ch12_1', float),
                  ('hKey_1', str),
                  ('ch1_2', float), ('ch2_2', float),('ch3_2', float), ('ch4_2', float),
                  ('ch5_2', float), ('ch6_2', float),('ch7_2', float), ('ch8_2', float),
                  ('ch9_2', float), ('ch10_2', float),('ch11_2', float), ('ch12_2', float),
                  ('hKey_2', str),
                  ('counter', long), ('temp', float),('wIdx', long), ('rIdx', long),
                  ('tailsymb', str), ('file_index', int),('timestamp', str), ('packet_len', int),
                  ]#define a format for xy-plot (to use if not datetime on x-axis)

        format_rad = (float,float,float,float,float,float,float,float,float,float,float,float,str,
                      float,float,float,float,float,float,float,float,float,float,float,float,str,
                      long,float,long,long,str,int,str,int)

        format_enc = [('c1_a1', float), ('c1_a3', float),('c1_a4', float), ('c1_a5', float),
                  ('c1_a6', float), ('c1_a7', float),('c1_a8', float), ('c1_a9', float),
                  ('c1_aA', float), ('c1_aD', float),('c1_aE', float), ('c1_aF', float),

                  ('c2_a1', float), ('c2_a3', float),('c2_a4', float), ('c2_a5', float),
                  ('c2_a6', float), ('c2_a7', float),('c2_a8', float), ('c2_a9', float),
                  ('c2_aA', float), ('c2_aD', float),('c2_aE', float), ('c2_aF', float),

                  ('c3_a1', float), ('c3_a3', float),('c3_a4', float), ('c3_a5', float),
                  ('c3_a6', float), ('c3_a7', float),('c3_a8', float), ('c3_a9', float),
                  ('c3_aA', float),

                  ('c4_a4', float), ('c4_a3', float),('c4_aE', float), ('c4_a5', float),
                  ('c4_a8', float), ('c2_a9', float),('c2_aF', float),

                  ('c5_a4', float), ('c5_a5', float), ('c5_aD', float), ('c5_aE'),

                  ('c6_a5', float), ('c6_a4', float), ('c5_aE', float), ('c5_aD'),

                  ('c7_a4', float), ('c7_a5', float),('c7_aE', float), ('c7_aD', float),

                  ('encoder_counter', long), ('mo1', int),('mo2', int),

                  ('counter', long), ('wIdx', long), ('rIdx', long), ('tailsymb', str),

                  ('file_index', int), ('timestamp', str), ('packet_len', int)

                  ]#define a format for xy-plot (to use if not datetime on x-axis)

        #Transform data to a numpy.recarray
        # dtable=
        # dtable=np.array()

        # for row in dr:
        #     print row

        a=[(192,192,2.5),(200,200,1.5),(200,200,1.5)]
        a1= [list(elem) for elem in a]
        af=[('a',int),('b',int),('c',float)]
        bf=[(int,int,float)]

        b=[list(i1) for i1 in a1]

        # na=np.array(b,dtype=af)
        # na=np.array(b)
        # print na.shape

        a1= [list(elem) for elem in dr]
        na=np.array(a1)
        print na.shape


        # try:
        #     if table == 'rad':
        #         # dtable = np.asarray(dr, dtype=format_rad)  #NDARRAY
        #         # for row in len(dr):
        #             # dtable.append(row)
        #     elif table == 'enc':
        #         # dtable = np.array(dr, dtype=format_enc)  #NDARRAY
        #
        #
        #     # dtable.reshape(2,2,4)
        #
        # except Exception,e:
        #   print "error: "+ str(e)


        return na


def create_db_light(table,cols):
    """Running cost: 91m22.244s (6 Nov 2013)"""
    print "creating table %s" % table
    print "creating columns %s" % cols

    db = DaqDB('daq.db')
    db.optimise_inserts()
    db.create_table(table, cols)
    # for filename in np.sort(glob.glob(os.path.join(constants.DESTINATION, '*.enc'))):
    #     db.insert_raw(filename, cols)
    # db.create_indexes()
    db.commit()

def create_db_full():
    """Creates iphas-dr2-full.db

    Running cost: about 10 hours?
    """
    cols = ['name', 'ra', 'dec',
            'sourceID', 'posErr', 'l', 'b',
            'mergedClass', 'mergedClassStat', 
            'pStar', 'pGalaxy', 'pNoise',
            'pSaturated', 'rmi', 'rmha',
            'r', 'rErr', 'rPeakMag', 'rPeakMagErr',
            'rAperMag1', 'rAperMag1Err', 'rAperMag3', 'rAperMag3Err',
            'rGauSig', 'rEll', 'rPA', 'rClass', 'rClassStat',
            'rErrBits', 'rMJD', 'rSeeing', 'rDetectionID',
            'rX', 'rY',
            'i', 'iErr', 'iPeakMag', 'iPeakMagErr',
            'iAperMag1', 'iAperMag1Err', 'iAperMag3', 'iAperMag3Err',
            'iGauSig', 'iEll', 'iPA', 'iClass', 'iClassStat',
            'iErrBits', 'iMJD', 'iSeeing', 'iDetectionID',
            'iX', 'iY', 'iXi', 'iEta',
            'ha', 'haErr', 'haPeakMag', 'haPeakMagErr',
            'haAperMag1', 'haAperMag1Err', 'haAperMag3', 'haAperMag3Err',
            'haGauSig', 'haEll', 'haPA', 'haClass', 'haClassStat',
            'haErrBits', 'haMJD', 'haSeeing', 'haDetectionID',
            'haX', 'haY', 'haXi', 'haEta',
            'brightNeighb', 'deblend', 'saturated', 'errBits',
            'nBands', 'reliable', 'fieldID', 'fieldGrade',
            'night', 'seeing', 'ccd', 'nObs', 'sourceID2',
            'fieldID2', 'r2', 'rErr2', 'i2', 'iErr2', 'ha2', 'haErr2',
            'errBits2']
    #db = SurveyDB('/home/gb/tmp/test.db')
    # db = DaqDB(os.path.join(constants.DESTINATION, 'iphas-dr2-full.db'))
    db = DaqDB(os.path.join('daq-full.db'))
    db.optimise_inserts()
    db.create_table('iphas', cols)
    # files_to_insert = glob.glob(os.path.join(constants.PATH_CONCATENATED, 'full', '*.fits'))
    files_to_insert = glob.glob(os.path.join('full', '*.fits'))
    #files_to_insert = glob.glob(os.path.join(constants.PATH_CONCATENATED, 'full', '*215b.fits'))
    for filename in np.sort(files_to_insert):
        db.insert_fits(filename, cols)
    db.commit()
    db.create_indexes()
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
        'Press','bPrs','LAT','LON','ALT','VEL_N','VEL_E','VEL_D',
        'Hacc','Vacc','Sacc','bGPS','TS','Status','CS',
        'counter','wIdx','rIdx','tailsymb',
        'file_index','timestamp','packet_len'
       ]


RAD_COL = ['ch1','ch2','ch3','ch4','ch5','ch6','ch7','ch8','ch9','ch10','ch11','ch12','hKey',
        'ch13','ch14','ch15','ch16','ch17','ch18','ch19','ch20','ch21','ch22','ch23','ch24',
        'counter','temp','wIdx','rIdx','tailsymb',
        'file_index','timestamp','packet_len'
       ]

ENC_COL = ['c1_s1','c1_s2','c1_s3','c1_s4','c1_s5','c1_s6',
        'c2_s1','c2_s2','c2_s3','c2_s4','c2_s5','c2_s6',
        'c3_s1','c3_s2','c3_s3','c3_s4','c3_s5','c3_s6',
        'c4_s1','c4_s2','c4_s3','c4_s4','c4_s5','c4_s6',
        'c5_s1','c5_s2','c5_s3','c5_s4','c5_s5','c5_s6',
        'c6_s1','c6_s2','c6_s3','c6_s4','c6_s5','c6_s6',
                                        'c7_s5','c7_s6',
        ]
### Session Table ###
SESSION_COL = [
    'session_index',
    'starting time',
    'end time',
    'file index',
    'file name',
    'filesize',
    'folder name',
    'records_uploaded','records_rejected',
]

ENC_INIT_COL = ['c1_c1','c1_c2','c1_c3','c1_c4','c1_c5','c1_c6',
        'c2_c1','c2_c2','c2_c3','c2_c4','c2_c5','c2_c6',
        'c3_c1','c3_c2','c3_c3','c3_c4','c3_c5','c3_c6',
        'c4_c1','c4_c2','c4_c3','c4_c4','c4_c5','c4_c6',
        'c5_c1','c5_c2','c5_c3','c5_c4','c5_c5','c5_c6',
        'c6_c1','c6_c2','c6_c3','c6_c4','c6_c5','c6_c6'
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

if __name__ == '__main__':
    # generate tables
# def create_db():
    # sl.rename(os.path.join(DB_DIR,DB_NAME),os.path.join(DB_DIR,DB_NAME+".bk"))

    create_db_light("inu",INU_COL)

    # cols = ['ch1_1','ch2_1','ch3_1','ch4_1','ch5_1','ch6_1','ch7_1','ch8_1','ch9_1','ch10_1','ch11_1','ch12_1','hKey_1',
    #         'ch1_2','ch2_2','ch3_2','ch4_2','ch5_2','ch6_2','ch7_2','ch8_2','ch9_2','ch10_2','ch11_2','ch12_2','hKey_2',
    #         'counter','temp','wIdx','rIdx','tailsymb',
    #         'file_index','timestamp','packet_len'
    #        ]
    # create_db_light("rad",cols)


    create_db_light("rad",RAD_COL)

    # cols = ['c1_a1','c1_a3','c1_a4','c1_a5','c1_a6','c1_a7','c1_a8','c1_a9','c1_aA','c1_aD','c1_aE','c1_aF',
    #       'c2_a1','c2_a3','c2_a4','c2_a5','c2_a6','c2_a7','c2_a8','c2_a9','c2_aA','c2_aD','c2_aE','c2_aF',
    #       'c3_a1','c3_a3','c3_a4','c3_a5','c3_a6','c3_a7','c3_a8','c3_a9','c3_aA',
    #       'c4_a4','c4_a3','c4_aE','c4_a5',                'c4_a8','c4_a9',                        'c4_aF',
    #                       'c5_a4','c5_a5',                                        'c5_aD','c5_aE',
    #       'c6_a5','c6_a4','c6_aE',                                                'c6_aD',
    #       'c7_a4','c7_a5','c7_aE',                                                'c7_aD',
    #       'encoder_counter','mo1','mo2','counter','wIdx','rIdx','tailsymb',
    #       'file_index','timestamp','packet_len'
    #         ]
    # create_db_light("enc",cols)

    # cols = ['c1_a1','c1_a3','c1_a4','c1_a5','c1_a6','c1_a7','c1_a8','c1_a9','c1_aA','c1_aD','c1_aE','c1_aF',
    #       'c2_a1','c2_a3','c2_a4','c2_a5','c2_a6','c2_a7','c2_a8','c2_a9','c2_aA','c2_aD','c2_aE','c2_aF',
    #       'c3_a1','c3_a3','c3_a4','c3_a5','c3_a6','c3_a7','c3_a8','c3_a9','c3_aA',
    #       'c4_a1','c4_a3','c4_aE','c4_a5','c4_a6','c4_a7','c4_a8','c4_a9',
    #       'c5_a1','c5_a3','c5_a4','c5_a5','c5_a6','c5_a7','c5_a8','c5_a9',        'c5_aD','c5_aE',
    #       'c6_a1','c6_a3','c6_a4','c6_a5','c6_a6','c6_a7','c6_a8','c6_a9',                                                'c6_aD',
    #       'encoder_counter','mo1','mo2','counter','wIdx','rIdx','tailsymb',
    #       'file_index','timestamp','packet_len'
    #         ]
    # create_db_light("enc",cols)

    create_db_light("enc",ENC_COL)

    create_db_light("calib",ENC_INIT_COL)


    create_db_light("session",SESSION_COL)

    create_db_light("converted",DATA_COL)




    sl.move(DB_NAME,os.path.join(DB_DIR,DB_NAME))
    print os.path.join(DB_DIR,DB_NAME)