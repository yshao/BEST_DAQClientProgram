import os
import shutil
from common.env import Env
from daqmanager.decoder.DecodeEncTask3 import DecodeEncTask
from daqmanager.decoder.DecodeInuTask import DecodeInuTask
from daqmanager.decoder.dataset import Dataset

if __name__ == '__main__':
    cfg=Env().getConfig()
    local=cfg['local_dir']

    fdr='%s/%s' % (local,'1010')
    d=Dataset(fdr)
    inuGroup=d.fileGroup['inu']
    encGroup=d.fileGroup['enc']

    bufferp='%s/%s' % (fdr,'records')

    try:
        os.mkdir(bufferp)
    except:
        pass



    for i,f in enumerate(encGroup):
        recname='%senc.db' % f
        shutil.copy('daq.db',recname)
        efile='%s/%s' & (local,f)
        etask=DecodeEncTask()
        etask.parse_enc(efile,i)



    for i,f in enumerate(inuGroup):
        recname='%sinu.db' % f
        shutil.copy('daq.db',recname)
        ifile='%s/%s' & (local,f)
        itask=DecodeInuTask()
        itask.parse_inu(ifile,i)
        # itask.par

