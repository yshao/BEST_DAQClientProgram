### test parse with polling ###
from best.daqmanager.dataparser import *
from best.common.sqliteutils import *
from best.common.configutils import *

import os


PYTHONPATH="c:/Users/Ping/Workspace"
config=Config(os.path.join(PYTHONPATH,"best/daqmanager/config.xml"))
db=DaqDB(os.path.join(config.get("LOCAL_DB_DIR"),config.get("LOCAL_DB_NAME")))


class DecodeTask(object):
    mState= ""
    mCurrentFile = ""
    mNumFiles = ""

    def __init__(self,folder):
        ""
        self.db=db
        self.radParser=DataParser(type='rad',sink=self.db)
        self.inuParser=DataParser(type='enc',sink=self.db)
        self.encParser=DataParser(type='enc',sink=self.db)

        ### init signals ###

        folder="data/single"
        folder="data/multi"

    def perform(self):
        ""
        for idx,file in enumerate(np.sort(glob.glob(os.path.join(folder, '*.rad')))):
            print "task"
            self.state=""

    def get_state(self):
        return self.state




class DecodeDataFolderTask(object):
    def __init__(self,folder):
        ""

    def perform(self):
        ""

### test decode task thread ###
folder=os.path.join(PYTHONPATH,"best/daqmanager/data/single")

task=DecodeTask(folder)
task.run()

print task.get_state()

### test decode folder iteraotr thread ###

# gui.update(task.get_state())