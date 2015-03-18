def bin_to_int(data,num_bit=0,num_pads=0):
    bstr=''
    for d in data:
        bstr = bstr+ bin(d)[2:]

    if num_bit==0: num_bit=len(bstr)

    bstr=bstr[0:num_bit]

    if num_pads != 0:
        bstr=bstr+'0'*num_pads


    num=int(bstr,2)
    return num

if __name__ == '__main__':
    assert bin_to_int([4,4],4) == 9