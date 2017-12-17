import sys, requests
from PyQt5 import QtGui, uic, QtWidgets


(form_class, qtbase_class) = uic.loadUiType('Demo3.ui')


class MainWindow(qtbase_class, form_class):
  def __init__(self):
    super(MainWindow, self).__init__()
    self.setupUi(self)
    self.pushButton.clicked.connect(self._showpic)

  def _showpic(self):
    url = 'http://i1.ce.cn/ce/culture/tk/gdn/201308/14/W020130814387271679357.jpg'
    pic = requests.get(url).content
    pixmap = QtGui.QPixmap()
    pixmap.loadFromData(pic)
    self.label.setPixmap(pixmap)

if __name__ == "__main__":
  app = QtWidgets.QApplication(sys.argv)
  ui = MainWindow()
  ui.show()
  sys.exit(app.exec_())

