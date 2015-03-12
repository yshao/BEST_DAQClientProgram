from best.common.consts import *



class PlotDataTask(QThread):
    def __init__(self):
        ""

    def check_update(self):
        ""

    def refresh(self):
        ""


config=



list=[config.get('IP_STATIONARY_SWITCH'),config.get('IP_SCANNING_SWITCH_1'),config.get('IP_SCANNING_SWITCH_2')]
scan_network(list)

comp_list=[config.get('IP_ARCHIVAL'),config.get('IP_ENCODER'),config.get('IP_RADIOMETER_22-30'),
           config.get('IP_RADIOMETER_60-90'),config.get('IP_RADIOMETER_122-130')]
scan_network(comp_list)