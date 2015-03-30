from common.env import Env
from common.sqliteutils import DaqDB

class DataBuffer:
    def __init__(self):
        ""
        cfg=Env().getConfig()
        local=cfg['local_dir']
        self.local=local
        self.data=DaqDB('%s/data.db' % local)

    def bulk_insert(self):
        import sqlite3
        timedbp='time.db'
        datadbp=self.data

        connection = sqlite3.connect(timedbp)
        cursor=connection.cursor()
        cursor.execute('ATTACH %s AS master' % datadbp)

        inuRec=''
        encRec=''
        inu='%s/%s' % (self.local,inuFile)
        enc='%s/%s' % (self.local,encFile)

        cursor.execute('attach database %s as db1' % inu)
        cursor.execute('attach database %s as db2' % enc)
        cursor.execute('INSERT OR REPLACE INTO master.data SELECT * FROM db1.inu order by counter')

###
if __name__ == '__main__':
    dbuff=DataBuffer()
    dbuff.bulk_insert()