__company__ = 'Boulder Environmental Sciences and Technology'
__project__ = ''
__author__ = 'Y. Shao'
__created__ = '3/16/2015' '6:37 PM'

### make folder with epochtime ###
# archive to folder
# move to
def archive_folder(tm):
    nowtime.tm()
    make_tar(tm,filep)

    remote=Remote('dataserver')
    remote.upload([filep])
    remote.run()