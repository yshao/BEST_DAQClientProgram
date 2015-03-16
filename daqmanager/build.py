### build all ui
import os
from common.sysutils import run_command

import glob
# glob.glob('*.gif')

folder="gui/ui"
for f in glob.glob('%s/*.ui' %folder):
    target=os.path.join(folder,"ui_"+os.path.basename(f)[:-3]+".py")

    if run_command('pyuic4 -x %s -o %s' %(f,target)) == ('',''):
        print "built ui for "+f
    else:
        print "error: "+f