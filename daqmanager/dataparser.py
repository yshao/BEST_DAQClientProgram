from best.daqmanager.tasks.helpers.parse_enc import *
from best.daqmanager.tasks.helpers.parse_inu import *
from best.daqmanager.tasks.helpers.parse_rad import *

### definition for
def parse_enc():
    ""

def parse_rad():
    ""

def parse_inu():
    ""

class DataParser(object):
    def __init__(self,type,sink):
        ""
        self.db=sink



        if type == "rad":
            self.parser=parse_rad

        if type == "enc":
            self.parser=parse_enc

        if type == "inu":
            self.parser=parse_inu

    def parse(self,file):
        self.parser(file)



