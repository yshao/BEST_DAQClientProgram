import os
from keepass import kpdb
from keepass.kpdb import Database
from common.iniconfig import IniParser
# from common.jsonconfig import JsonConfig


class Env():
    param={'HOME':'c:/Users/Ping/Code/best/daqclient1'}

    def __init__(self):
        ""
        #TODO: installer then test this
        # self.init_from_os()

        config=self.param['HOME']+'/common/config.ini'
        # print config
        kdb=self.param['HOME']+'/common/resources/daq.kdb'
        parser = IniParser()
        parser.read(config)
        # pd={}
        pd=parser.as_dict()
        # print pd
        d={}
        d=pd['base']
        d['radiometer']=pd['radiometer']

        d2=self._get_passwords(kdb)

        d.update(d2)
        self.k=d

    def init_from_os(self):
        ""
        homep=os.getenv('WEATHER_HOME', 'c:/Weather')
        self.param['HOME']=homep


    def getpath(self,param):
        return self.param


    def getConfig(self):
        return self.k



    def _get_passwords(self,filep):
        db=Database(filep,'best')
        d={}

        try:
            for ent in db.entries:
                title=ent.title
                username=ent.username
                password=ent.password
                if title != 'Meta-Info':
                    # d[title]={}
                    d['%s_username'%title]=username
                    d['%s_password' %title]=password
        except:
            print "End of DB"

        return d

if __name__ == '__main__':
    e=Env()
    print e.getConfig()