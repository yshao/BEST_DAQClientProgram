import sqlite3 as lite


attach database database1.db as db1;
attach database database2.db as db2;


### select and order by
con=lite.connect()
con.execute('select * from db1 union select * from db2 order by counter')

### bulk insert ###