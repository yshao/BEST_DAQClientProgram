from PyQt4 import QtCore, QtGui, QtXml
from PyQt4.QtGui import QTreeWidgetItem, QTreeWidget

def fill_item(item, value):
  item.setExpanded(True)
  if type(value) is dict:
    for key, val in sorted(value.iteritems()):
      child = QTreeWidgetItem()
      child.setText(0, unicode(key))
      item.addChild(child)
      fill_item(child, val)
  elif type(value) is list:
    for val in value:
      child = QTreeWidgetItem()
      item.addChild(child)
      if type(val) is dict:      
        child.setText(0, '[dict]')
        fill_item(child, val)
      elif type(val) is list:
        child.setText(0, '[list]')
        fill_item(child, val)
      else:
        child.setText(0, unicode(val))              
      child.setExpanded(True)
  else:
    child = QTreeWidgetItem()
    child.setText(0, unicode(value))
    item.addChild(child)

def fill_widget(widget, value):
  widget.clear()
  fill_item(widget.invisibleRootItem(), value)


from configutils import *

d = { 'archival': 'value1',
  'encoder': 'value2',
  'radio': [1,2,3, { 1: 3, 7 : 9}],
  'radio': {'ip':1,'a':2},
  'motor': object(),
  'data folder': { 'another key1' : 'another value1',
            'another key2' : 'another value2'} }


STATUS_MAP = {
    'archival':{'ip:':'','connected:':'','ftp:':''},
    'encoder':{'ip':'','connected:':'','ftp':''},
    'radiometer':{'ip':'','type':'','connected:':'','ftp:':''},
    'radiometer':{'ip':'','type':'','connected:':'','ftp:':''},

    'motor':{'mode':'','speed':'','profile:':''},
    'data folder':{'root:':'','path':''},
    'data server':{'num_records':''},
}

### test config readback

# if __name__ == '__main__':
#     import sys
#     app = QtGui.QApplication(sys.argv)
#     config = Config("config.xml")
#     configMap= config.get_map()
#
#     widget = QTreeWidget()
#     fill_widget(widget, configMap)
#     widget.show()
#     sys.exit(app.exec_())


### test config readmap with statusMap
if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)

    widget = QTreeWidget()
    fill_widget(widget, STATUS_MAP)
    widget.show()
    sys.exit(app.exec_())