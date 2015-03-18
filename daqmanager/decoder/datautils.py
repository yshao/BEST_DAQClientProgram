from daqmanager.client.utils import epoch_to_tm


def bin_to_int(data,num_bit=0,num_pads=0):
    "non standard number of bits conversion"
    bstr=''
    for d in data:
        bstr = bstr+ bin(d)[2:]

    if num_bit==0: num_bit=len(bstr)

    bstr=bstr[0:num_bit]

    if num_pads != 0:
        bstr=bstr+'0'*num_pads


    num=int(bstr,2)
    return num

class DataUtils():
    def __init__(self,fdr):
        self.folderp=fdr
        self.base_time=0

    def counter_to_tm(self,counter):
        epoch=self.base_time+counter
        epoch_to_tm(epoch)

if __name__ == '__main__':
    assert bin_to_int([4,4],4) == 9


