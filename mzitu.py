import sys
import re
import requests
from bs4 import BeautifulSoup
from PyQt5.QtWidgets import QApplication, QCheckBox, QPushButton, QHeaderView
from PyQt5.QtGui import QPixmap
import PyQt5.uic
from PyQt5 import QtWidgets


uic_file = 'Demo5.ui'
(class_ui, class_basic_class) = PyQt5.uic.loadUiType(uic_file)


class Mzitu():
  def __init__(self, url):
    self.url = url
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36', 'Host': 'www.mzitu.com'}
    response = requests.get(self.url, headers = headers)
    content = BeautifulSoup(response.text, 'lxml')
    linkblock = content.find('div', class_='postlist')
    self.linklist = linkblock.find_all('li')
  
  def printli(self):
    linklist = self.linklist
    linksum = list()

    for link in linklist:
      url = link.a.get('href')
      picurl = link.img.get('data-original')
      linkid = re.search(r'(\d+)', url).group()
      firstspan = link.span
      titleword = firstspan.get_text()
      secondspan = firstspan.find_next_sibling('span')
      uploadtime = secondspan.get_text()
      thirdspan = secondspan.find_next_sibling('span')
      viewcount = thirdspan.get_text()
      linksum.append((linkid, titleword, uploadtime, viewcount, picurl))
    return linksum


class Window(class_basic_class, class_ui):
  def __init__(self):
    super(Window, self).__init__()
    self.url = 'http://www.mzitu.com/'
    self.setupUi(self)
    totlist = Mzitu(self.url).printli()
    self.tableWidget.setRowCount(len(totlist))
    self.tableWidget.setColumnCount(2)
    self.tableWidget.setColumnWidth(0, 435)
    verticalHeader = self.tableWidget.verticalHeader()
    verticalHeader.setSectionResizeMode(QHeaderView.Fixed)
    verticalHeader.setDefaultSectionSize(30)
    self.textBrowser.setOpenExternalLinks(True)
    self.page = 1
    self.label_pagenum.setNum(self.page)
    self.checkBoxs = [self._addCheckbox(index, item[0], item[1]) for index, item in enumerate(totlist)]
    self.pushButtons = [self._addpushButtonpic(index, item[0], item[4]) for index, item in enumerate(totlist)]
    self.pushButton.clicked.connect(self.getSelList)
    self.pushButton_nextpage.clicked.connect(lambda: self._nextPage(1))
    self.pushButton_uppage.clicked.connect(lambda: self._nextPage(-1))

  def _addCheckbox(self, index, idd, boxtitle):
    checkBox = QCheckBox()
    checkBox.setObjectName(idd)
    checkBox.setText(boxtitle)
    self.tableWidget.setCellWidget(index, 0, checkBox)
    return checkBox

  def getSelList(self):
    selList = [(item.objectName(), item.text()) for item in self.checkBoxs if item.isChecked()]
    for item in selList:
      url = 'http://www.mzitu.com/'+item[0]
      self.textBrowser.append(item[1])
      self.textBrowser.append('<a href=%s>%s</a>' % (url, url))
    return selList
  
  def _addpushButtonpic(self, index, idd, href):
    pushButton = QPushButton()
    pushButton.setObjectName(idd)
    pushButton.setText(idd)
    self.tableWidget.setCellWidget(index, 1, pushButton)
    pushButton.clicked.connect(lambda: self._showpic(idd, href))
    return pushButton

  def _showpic(self, idd, href):
    pic = requests.get(href, headers={'Referer': href}).content
    pixmap = QPixmap()
    pixmap.loadFromData(pic)
    self.label.setPixmap(pixmap)

  def _nextPage(self, page):
    self.page += page
    self.label_pagenum.setNum(self.page)
    url = self.url + '/page/' + str(self.page)
    totlist = Mzitu(url).printli()
    newcheckBoxs = []
    newpushButtons = []
    for index, item in enumerate(totlist):
      newcheckbox = self._addCheckbox(index, item[0], item[1])
      newpushbutton = self._addpushButtonpic(index, item[0], item[4])
      newcheckBoxs.append(newcheckbox)
      newpushButtons.append(newpushbutton)
    self.checkBoxs = newcheckBoxs
    self.pushButtons = newpushButtons


if __name__ == '__main__':
  app = QtWidgets.QApplication(sys.argv)
  ui = Window()
  ui.show()
  app.exec_()
