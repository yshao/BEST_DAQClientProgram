### download ####
import os
from common.datasetman import DatasetMan
from common.env import Env
from daqmanager.client.ftpfunc import ftp_download

cfg=Env().getConfig()

datam=DatasetMan()

datam.clear_buffer()

datam.download(cfg['archival_ip'])
datam.download(cfg['encoder_ip'])
datam.download(cfg['radiometer']['rad22_ip'])


datam.save_buffer()
# try:
#     os.mkdir('./data')
# except:
#     pass
# try:
#     ftp_download(cfg['archival_ip'],cfg['praco_username'],cfg['praco_password'],'./data')
# except:
#     pass
# try:
#     ftp_download(cfg['encoder_ip'],cfg['praco_username'],cfg['praco_password'],'./data')
# except:
#     pass

# datam.archive()