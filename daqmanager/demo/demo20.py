from common.env import Env
from daqmanager.decoder.dataset import Dataset


###
cfg=Env().getConfig()
local=cfg['local_dir']

fdr='%s/%s' % (local,'1428000000')
dset=Dataset(fdr)
dset.scan_files()
# print dset.inuGroup
# print dset.encGroup
dset.decode_folder()
dset.scan_buffers()

# print dset.encRecGroup
# print dset.inuRecGroup


# dset.interp_time()
dset.create_dataset()

