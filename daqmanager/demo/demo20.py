from common.env import Env
from daqmanager.decoder.dataset import Dataset


###
DATASET=''

cfg=Env().getConfig()
local=cfg['local_dir']

fdr='%s/%s' % (local,DATASET)
dset=Dataset(fdr)
dset.scan_files()
# print dset.inuGroup
# print dset.encGroup
# dset.decode_folder()
dset.scan_buffers()

# print dset.encRecGroup
# print dset.inuRecGroup
# print dset.rad22RecGroup
# print dset rad22RecGroup


# dset.interp_dataset()
dset.create_dataset()
dset.sync()
