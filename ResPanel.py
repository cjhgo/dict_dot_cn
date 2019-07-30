#coding: utf-8

import os
import sys
import logging
from time import strftime
from datetime import timedelta
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QPlainTextEdit,QTextEdit
from PyQt5.QtWidgets import QLCDNumber
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5 import QtCore
from PyQt5.QtGui import QCursor,QDesktopServices
from PyQt5.QtCore import QTimer

from PyQt5.QtCore import Qt,QUrl

from PyQt5.QtWebKitWidgets import QWebView

from PyQt5.QtWidgets import  QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtCore import QEvent


class Panel(QWidget):
  def __init__(self,data=None):
    self.data = data
    QWidget.__init__(self)
    self.initUI()
  
  
  def initUI(self):
    self.content = QWidget(self)
    self.control = QGridLayout(self)    

    self.word = QPushButton(self)

    self.word.released.connect(lambda: 
                                QDesktopServices.openUrl(
                                    QUrl("http://dict.cn/"+self.word.text())
                                  )
                                )
  
    self.phonetic = QPushButton(self)
    
    self.definition = QTextEdit(self)
    
    self.translation = QTextEdit(self,)
    
    self.tag = QLineEdit(self)
    

    self.control.addWidget(self.word, 1,0)
    self.control.addWidget(self.phonetic, 1,1)
    self.control.addWidget(self.definition, 2,0,2,2)
    self.control.addWidget(self.translation, 3,0,3,2)
    self.control.addWidget(self.tag, 4,0,4,2)
    
    self.content.setLayout(self.control)
    self.content.resize(380,430)
    # self.setCentralWidget(self.content)

  def setcontent(self,data):
    self.data = data
    self.word.setText(self.data["word"])
    self.phonetic.setText(self.data["phonetic"])
    self.definition.setText(self.data["definition"])
    self.translation.setText(self.data["translation"])
    self.tag.setText("{} # {} # {}".format(self.data["tag"], self.data["frq"], self.data["bnc"]))    

if __name__ == "__main__":
  logging.basicConfig(filename='/var/log/pomodoro.log', level=logging.INFO,
                    format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M')
  app = QApplication(sys.argv)
  data={'definition': u'n. an isolated fact that is considered separately from the whole\nn. a small part that can be considered separately from the whole\nn. extended treatment of particulars\nn. a crew of workers selected for a particular task', 'word': 'detail', 'bnc': 566, 'exchange': u's:details/i:detailing/d:detailed/p:detailed/3:details', 'sw': u'detail', 'pos': u'v:9/n:91', 'detail': None, 'oxford': 1, 'frq': 997, 'tag': u'cet4 cet6 ky ielts', 'phonetic': u"'di:teil", 'collins': 4, 'translation': u'n. \u7ec6\u8282, \u8be6\u60c5\nvt. \u8be6\u8ff0, \u9009\u6d3e\nvi. \u753b\u8be6\u56fe\n[\u8ba1] \u8be6\u7ec6\u6570\u636e', 'audio': u'', 'id': 805261}
  panel = Panel()
  panel.setcontent(data)
  panel.show()
  QDesktopServices.openUrl(QUrl("http://www.google.com"))
  sys.exit(app.exec_())