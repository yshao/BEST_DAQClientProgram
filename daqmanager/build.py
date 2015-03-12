import subprocess
from best.common.sysutils import *

run_command('pyuic4 -x motorwidget.ui -o ui_motorwidget.py')
run_command('pyuic4 -x controlwidget.ui -o ui_controlwidget.py')
run_command('pyuic4 -x plotterwidget.ui -o ui_plotterwidget.py')
run_command('pyuic4 -x daqwidget.ui -o ui_daqwidget.py')
run_command('pyuic4 -x statuswidget.ui -o ui_statuswidget.py')
run_command('pyuic4 -x sensorwidget.ui -o ui_sensorwidget.py')
run_command('pyuic4 -x imuwidget.ui -o ui_imuwidget.py')
run_command('pyuic4 -x servicewidget.ui -o ui_servicewidget.py')
run_command('pyuic4 -x plotterwidget.ui -o ui_plotterwidget.py')

run_command('pyuic4 -x plotterdialog.ui -o ui_plotterdialog.py')

run_command('pyuic4 -x daqwindow.ui -o ui_daqwindow.py')

### test ###
run_command('pyuic4 -x testdatawidget.ui -o ui_testdatawidget.py')