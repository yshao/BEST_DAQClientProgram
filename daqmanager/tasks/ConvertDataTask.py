import pandas as pd

from best.common.guiutils import *
from best.common.sqliteutils import *

class ConvertDataTask(object):
    def __init__(self,db):
        ""

    def perform(self):
        ""




def interpolate_timescale():
    ""
    #TODO: rollover

    #TODO:

def convert_to_fullset(enc,rad,inu):
    db.insert_data(inu)
    db.insert_data(enc)
    db.insert_data(rad)

    db.insert_data({'':})

db=DaqDb()
encDR=db.select_data('select counter,timestamp from enc')
radDR=db.select_data('select counter,timestamp from rad')
inuDR=db.select_data('select counter,timestamp from inu')

inuDR[counter]

inuDR[timestamp] float


dr=interpolate_timescale(dr)

db.update_record(dr,'time')


### plot raw enc ###
refresh(encDR)
update_disp(title,xLabel,yLabel,legend)


### plot raw rad ###
plotter.plot(radDR)

### plot raw inu ###
plotter.plot(inuDR)

### plot raw motor ###
plotter.plot(encDR)

### plot level 1 ###
plotter.plot(converted,disp)