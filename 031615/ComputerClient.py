


class ComputerClient(object):
    def __init__(self,ip,local_dir,user,password):
        self.ip=ip
        self.local_dir=local_dir
        self.user=user
        self.password=password

        self.telnet=TelnetClient(ip,user,password)
        self.ftp=FtpClient(ip,user,password)

    def send(self,command):
        self.telnet.send(command)


    def sync(self):
        self.daqclient=TelnetClient(self.ip,self.user,self.password)
        self.ftp.sync_download()