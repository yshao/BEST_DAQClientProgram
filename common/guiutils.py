import logging

grad2rad = 3.141592/180.0

APP_NAME="DAQ Manager"

class LoggerPanel(object):
    def __init__(self,browser):
        self._logger_disp=browser
        self._logger=self.create_logger(APP_NAME,"New App Logger")

    def create_logger(script_name,start_message):
        logger = logging.getLogger(script_name)
        hdlr = logging.FileHandler(script_name+".log")
        logger.debug("Creating Logger for "+script_name)
        logger.addHandler(hdlr)
        logger.setLevel(logging.DEBUG)
        # create console handler with a higher log level
        ch = logging.StreamHandler()

        logger.info("")
        logger.info("****************************************************************************")
        logger.info(start_message)
        logger.info("****************************************************************************")

        # create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        hdlr.setFormatter(formatter)
        ch.setFormatter(formatter)
        # add the handlers to the logger
        logger.addHandler(ch)

        return logger

import matplotlib.pyplot as plt
from sqliteutils import *

class Plotter(object):
    def __init__(self):
        ""
        # self.data=data
        # if source == ".db":
            # self.datasource=DaqDB(source)

            # self.data=self.datasource.load_data()

    def plot_data(self,data):
        ""



    # def show(self):
    #     ""
    #     plt.plot(self.data, label='22 GHz Branch 1')
    #     plt.plot(self.data, label='29 GHz Branch 1')
    #     plt.plot(self.data, label='29 GHz Branch 2')
    #     plt.plot(self.data, label='22 GHz Branch 2')
    #     plt.title('Radiometer Output')
    #     plt.ylabel('Voltage (mV)')
    #     plt.xlabel('Counts')
    #     plt.legend(loc=7)
    #     plt.show()

    def refersh(self):
        ""

import threading
import time

from PyQt4.QtCore import QObject, SIGNAL

class asyncUiControl(threading.Thread, QObject):

    mTaskList = []
    mResultList = []
    mResultFetched = True

    def __init__(self):
        QObject.__init__(self)
        threading.Thread.__init__(self)

    def run(self):
        while not len(self.mTaskList) == 0:
            while not self.mResultFetched:
                time.sleep(0.1)
            if not len(self.mTaskList) == 0:
                self.__performTask(self.mTaskList.pop())
        threading.Thread.__init__(self)

    def __performTask(self, pTask):
        self.mResultFetched = False
        pTask.perform()
        self.mResultList.append(pTask)
        self.emit(SIGNAL(pTask.ID))

    def addTask(self, pLabelControlTask):
        self.mTaskList.insert(0, pLabelControlTask)

    def grabLatestResult(self):
        vResult = self.mResultList.pop()
        self.mResultFetched = True
        return vResult



import twitter

class downloadTimeLineTask():
    ID = "task_downloadTimeLine()"
    mUserName = ""
    mTimeLine = []

    def __init__(self, pUserName, pApi):
        self.mUserName = pUserName
        self._twitterApi = pApi

    def perform(self):
        self._twitterApi.SetCacheTimeout(1)
        self.mTimeLine = self._twitterApi.GetFriendsTimeline(None, 100)