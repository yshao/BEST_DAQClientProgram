from common.env import Env
from daqmanager.decoder.dataset import Dataset


### specify dataset ###
DATASET='1427917590'

cfg=Env().getConfig()
local=cfg['local_dir']

fdr='%s/%s' % (local,DATASET)
dset=Dataset(fdr)
print "Raw Datasets"
dset.scan_files()
dset.decode_folder()

print "Decoded buffers"
dset.scan_buffers()

print dset.encRecGroup
print dset.inuRecGroup
print dset.rad22RecGroup
# print dset rad22RecGroup


dset.interp_dataset()
dset.create_dataset()
# dset.sync()
