from ftplib import FTP
import sys
import os

class FtpClient(object):
    newline = "\n"
    def __init__(self,host_url,username,password):
        ""
        self.ftp=FTP(host_url,username,password)
        username = username + self.newline
        password = username + self.newline

        self.ftp.chdir("C:\\FlashDisk\\Data")

    def upload(self, file):
        ext = os.path.splitext(file)[1]
        if ext in (".txt", ".htm", ".html"):
            self.ftp.storlines("STOR " + file, open(file))
        else:
            self.ftp.storbinary("STOR " + file, open(file, "rb"), 1024)

    def gettext(self, filename, outfile=None):
        # fetch a text file
        if outfile is None:
            outfile = sys.stdout
        # use a lambda to add newlines to the lines read from the server
        self.ftp.retrlines("RETR " + filename, lambda s, w=outfile.write: w(s+"\n"))

    def getbinary(self, filename, outfile=None):
        # fetch a binary file
        if outfile is None:
            outfile = sys.stdout
        self.ftp.retrbinary("RETR " + filename, outfile.write)