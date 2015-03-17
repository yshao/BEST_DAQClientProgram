import subprocess

def run_command(cmd):
    cmd = cmd.split(" ")
    if cmd[0] == "pyuic4":
        cmd[0] = "C:\\Python27\\Lib\\site-packages\\PyQt4\\pyuic4.bat"

    try:
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE,
                              stdin=subprocess.PIPE)

        out, err = p.communicate()
        print err
        print out



    except:
        print err

    return out,err

import subprocess, threading

class Command(object):
    def __init__(self, cmd,parser=None):
        self.cmd = cmd
        self.process = None
        self.out=""
        self.err=""
        self.parser=parser

    def run(self, timeout=10):
        def target(self):
            cmda = self.cmd.split(" ")
            if cmda[0] == "pyuic4":
                cmda[0] = "C:\\Python27\\Lib\\site-packages\\PyQt4\\pyuic4.bat"


            self.cmd=" ".join(cmda)
            print 'Thread started: '+self.cmd
            self.process = subprocess.Popen(cmda, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE,
                              stdin=subprocess.PIPE)
            self.out, self.err=self.process.communicate()
            print 'Thread finished: '+self.cmd

        thread = threading.Thread(target=target,args=(self,))
        thread.start()

        thread.join(timeout)
        if thread.is_alive():
            print 'Terminating process: '+self.cmd
            self.process.terminate()
            # print "H"
            thread.join()
        # print self.process.returncode

        if self.process.returncode <= 0 and self.parser != None:
            self.result=self.parser(self.out)
        else:
            self.result=False

        return self.result,self.out,self.err


### test setup
def parser2(out):
    result = {}
    for row in out.split('\n'):
        ### regexp parsering
        if row.startswith("Reply from"):
            result=True

    return result

# ### test command not work
#
# command = Command("ping -n 1 192.168.38.1",parser2)
# code,out,err =  command.run(timeout=3)
#
# assert code == False
#
# ### test command work with parser
# command = Command("ping -n 1 google.com",parser2)
# code,out,err =  command.run(timeout=3)
#
# assert code == True
#
# ### sample
# output = subprocess.check_output("ipconfig /displaydns", shell=True)
# result = {}
# # print output
# for row in output.split('\n'):
#     if ': ' in row:
#         key, value = row.split(': ')
#         result[key.strip(' .')] = value.strip()
#
# # print(result)
# # print(result['A (Host) Record'])
#
#
# ### test command parser
# def parser1(out):
#     ""
#     # print out
#
#     result = {}
#     for row in out.split('\n'):
#         if ': ' in row:
#             key, value = row.split(': ')
#             result[key.strip(' .')] = value.strip()
#
#     # print(result)
#     # print(result['A (Host) Record'])
#     return result
#
# command = Command("ipconfig /displaydns",parser=parser1)
# code,out,err = command.run(timeout=10)
# # print out


