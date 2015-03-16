import multiprocessing


def check_network():
    lComputers=[]
    l=lComputers + cfg['switch1'] + cfg['switch2']
    for link in l:
        if run_command():

class DownloadPool():
    def __init__(self,lIps):
        ""
        self.cfg=Env().getConfig()
        self.local=cfg['local_dir']+'/'+lIps

    def fetch(self,ip):
        ###find files###
        for f in lFiles:
            get(f,self.locatl)

        lFiles=ftputil.get_files()

    def run(self):
        ""

        # To wait for the thread to finish, use Thread.join():
        pool=multiprocessing.Pool(processes=len(lIps)) #use 5 processes to download the data
        output=pool.map(fetch,lIps)


