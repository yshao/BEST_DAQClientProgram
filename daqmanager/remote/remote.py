import os
import re
from fabric.context_managers import cd, settings
from fabric.operations import put, get, run, sudo
from common.env import Env

__company__ = 'Boulder Environmental Sciences and Technology'
__project__ = ''
__author__ = 'Y. Shao'
__created__ = '3/9/2015' '2:10 PM'

class Remote(object):
    @staticmethod
    def gen_login(target):
        d=Env().getConfig()

        nd={}
        if target == 'dataserver':
            host='%s@%s' % (d['data_server_username'],d['data_server_host'])
            pwd=d['data_server_password']
            # base_dir=d
            nd=dict(host_string=host,password=pwd,base_dir='')

        return nd

    def __init__(self,d):
        ""
        self.d=d
        # print d
        # self.init()

    def status(self):
        d=self.d
        # print d
        with settings(host_string=d['host_string'],password=d['password']):
            res=run('date')
            # print res

        return res

    def init(self):
        d=self.d
        # print d
        homep=Env().param['HOME']
        remote_api_path=homep+'/common/remote/remote_api.py'

        # print d
        with settings(host_string=d['host_string'],password=d['password']):
            # with cd(d['base_dir']):
                print d['base_dir']
                put(remote_api_path,d['base_dir'])
                run('ls')

    def pexec(self,cmd,*args):
        ""
        d=self.d

        with settings(host_string=d['host_string'],password=d['password']):
            with cd(d['base_dir']):
                if args != ():
                    res=run('python remote_api.py %s %s' % (cmd," ".join(args)))
                else:
                    res=run('python remote_api.py %s' % (cmd))

        return res

    def upload(self,lFiles,dir=None):
        ""
        d=self.d
        l=[]

        with settings(host_string=d['host_string'],password=d['password']):
            if dir != None:
                with cd(dir):
                    for f in lFiles:
                        res=put(f)
                        if res.succeeded:
                            l.append(res)

            else:
                    for f in lFiles:
                        res=put(f)
                        if res.succeeded:
                            l.append(res)
        return l

    def download(self,lFiles,local):
        d=self.d
        l=[]
        with settings(host_string=['host_string'],password=d['password']):
            with cd(dir):
                for f in lFiles:
                    res=get(f)
                    if res.succeeded:
                        l.append()
        return l

    def execute(self,cmd,dir=None):
        d=self.d
        # if dir == None:
        #     dir=d['base_dir']
        # print d
        res=[]
        with settings(host_string=d['host_string'],password=d['password']):
            if dir != None:
                with cd(dir):
                    res=sudo(cmd)
            else:
                # print cmd
                res=sudo(cmd)

        return res

    def daemon(self,cmd,dir=None):
        d=self.d

        with settings(host_string=d['host_string'],password=d['password']):
            # run('ls')
            if dir != None:
                with cd(dir):
                    res=sudo(cmd,pty=False)
            else:
                # print cmd
                res=sudo(cmd,pty=False)

        return res
    # def pexec(self,cmd):
    #     remote_exec()

    # def ls(self):
    #     self.pexec("""
    #     import fileutils
    #
    #     """
    #     )

    def ls(self):
        ""
        return ['111.jpg','222.jpg','333.png','12444.png','12443.png']

    def listfilter(self,l,regex):
        ""
        # l=self.ls()
        lFiles = [f for f in l if re.match(regex, f)]
        return lFiles

    def listByExt(self,l,ext):
        lFiles = [f for f in l if re.match(r'[0-9]+.*\.%s' % ext, f)]
        return lFiles

    def list_folders(self,path):
        ""
        dirs = [x[0] for x in os.walk(path)]
        dirs.pop(0)
        return dirs

    def filterByList(self,l1,l2):
        from fnmatch import fnmatch
        # l1 = ['test1', 'test2', 'test3', 'test4', 'test5']
        l2 = set(['*%s*'%e for e in l2])
        # l2 = set(['*t1*', '*t4*'])
        res=[x for x in l1 if any(fnmatch(x, p) for p in l2)]
        return res

    def mv(self,lFiles,dir):
        ""

    def rm(self,lFiles):
        ""

    def mkdir(self,dir):
        ""

    def cd(self,dir):
        ""
        cd(dir)
        run('pwd')

    # def pexec(self):
    #     ""
    def cmd(self):
        ""

    def glob_files(self):
        ""