from common.sqliteutils import *
from common.mathutils import *
from common.configutils import *
from common.fileutils import *
from parse_enc5 import *


def plot(dr):
    ""


print "daq starting"

config=Config("config.xml")

print config.get("IP_ARCHIVAL")
print config.get("IP_ENCODER")

text="DATA"
dir=config.get("LOCAL_DATA_DIR")
folder=dir+timestamp+text


# daqclient(config)

# print daqclient.telnet.sendwait("status")

# daqclient.send_startdaq()

# print daqclient.ftp.status()

# daqclient.ftp.collect_data()


db=DaqDB("daq.db")

timestamp=get_timestamp()
# text=inName.getText()

for fname in list_files(folder):
    file=os.path.join(folder,fname)

    # file="data/092014"

    print "file found - %s" % file

# parse_enc(file,db)

    print "file parsed - %s" % file


    print "load data - %s"

    dr=db.select_data("select * from enc")

    print "convert data - %s"

    convert_data(dr)

    print "update plot"

    plot(dr)

