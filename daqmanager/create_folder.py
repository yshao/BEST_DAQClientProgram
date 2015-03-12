import unittest

import os
import shutil
from best.common.datautils import *
from best.common.sysutils import *

shutil.move()


### full exception handled command ###
text="testFolder"
folder=get_timestamp()+"_"+text

try:
    cmd=Command("mkdir %s" % folder)
    if cmd.run(timeout=3) != True:
        throws e

except Exception, e:

    print "Dir exists!"


### test command ###

class TestCreateFolder(unittest.TestCase):
    ""
    def setUp(self):
        ""
        text="testFolder"
        cmd=command("text")

    def test_folderNameGenerationIsCorrect(self):
        ""
        assert cmd.run == "[0-9]*"+"_"+text

    def test_commandsSet(self):


### test comman phrase from expect ###



