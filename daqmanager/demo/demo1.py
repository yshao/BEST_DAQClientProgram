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
