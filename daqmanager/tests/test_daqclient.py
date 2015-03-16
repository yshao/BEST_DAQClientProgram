from common.netutils import *
from best.daqmanager.gui import *

### test daq command ###
config=Config("../config.xml")


host_url=config.get("IP_RADIOMETER_22-30")
username=config.get("REMOTE_USER")
password=config.get("REMOTE_PASSWORD")

dir=config.get("REMOTE_APP_DIR")
print host_url
print dir
tel=TelnetClient(host_url,23)

try:
    tel=TelnetClient(host_url,username,password)
except Exception,e:
    print e

print tel.send("dir")