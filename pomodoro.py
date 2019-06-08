#coding: utf-8

import sys
import logging
from time import strftime
from datetime import timedelta
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QPlainTextEdit
from PyQt5.QtWidgets import QLCDNumber
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5 import QtCore
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import QTimer

from PyQt5.QtCore import Qt

from PyQt5.QtWebKitWidgets import QWebView

from PyQt5.QtWidgets import  QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtCore import QEvent





class PauseableTimer(QTimer):
  COUNT = 0 
  DUR = 2400
  def __init__(self, target,task):
    QTimer.__init__(self,target)    
    self.timeout.connect(self.onTimeout)
    self.target = target
    self.task = task
    self.onBreak = False
    self.counter = PauseableTimer.DUR

  def cur(self):
    td = timedelta(seconds=self.counter)
    td_str = str(td)[2:]
    return td_str

  def setCount(self, cnt):    
    PauseableTimer.DUR = cnt*60
    self.counter = PauseableTimer.DUR
    self.target.display(self.cur())

  #start or restart timer
  def start_(self):
    if not self.isActive():
      if self.counter == self.DUR and not self.onBreak:
        logging.critical("Good, task"+ self.task.text()+" duratioe begin")
      self.start(1000)

  def pause(self):
    if self.isActive():
      self.stop()

  def stop_(self):
    self.counter = PauseableTimer.DUR
    self.stop()
    self.target.display("00:00")

  def onTimeout(self):
    self.target.display(self.cur())
    self.counter -= 1
    if self.counter < 0:
      if self.onBreak:
        self.onBreakDue()        
      else:
        self.onTaskDue()
        
    

  def onTaskDue(self):
    logging.critical("Good, task"+ self.task.text()+" duratioe due")
    self.stop_()
    self.onBreak=True
    self.counter=5
    self.start_()
    
  
  def onBreakDue(self):  
    logging.info("Okay, it is time to work!")
    self.onBreak=False
    self.stop_()




class Pomodoro(QMainWindow):
  def __init__(self):
    QMainWindow.__init__(self)
    self.initUI()
  
  def initUI(self):
    self.content = QWidget(self)
    self.control = QGridLayout(self)    

    self.taskDur = QLineEdit(self)
    self.taskDur.setText("40")

    self.task = QLineEdit(self)

    self.lcd = QLCDNumber(self)
    self.lcd.display("00:00")    
    self.lcd.setMinimumSize(400,400)

    self.pat = PauseableTimer(self.lcd,self.task)
  
    self.start = QPushButton(self)
    self.start.setText("start")
    self.start.released.connect(self.pat.start_)

    self.stop = QPushButton(self)
    self.stop.setText("stop")
    self.stop.released.connect(self.pat.stop_)
  
    self.setTL=QPushButton(self)  
    self.setTL.setText("set dur,minutes")
    self.setTL.released.connect(lambda: self.pat.setCount(int(self.taskDur.text())))
    
  
    self.pause = QPushButton(self)
    self.pause.setText("pause")
    self.pause.released.connect(self.pat.pause)

    
    self.control.addWidget(self.taskDur,0,0,Qt.AlignLeft)
  
    self.control.addWidget(self.task,0,1,1,3)

    self.control.addWidget(self.lcd,1,0,1,4)

    self.control.addWidget(self.start,2,0)
    self.control.addWidget(self.pause,2,1)
    self.control.addWidget(self.stop,2,2)
    self.control.addWidget(self.setTL,2,3)

    self.content.setLayout(self.control)

    self.content.resize(400,600)
    self.setCentralWidget(self.content)
    self.show()


if __name__ == "__main__":
  logging.basicConfig(filename='/var/log/pomodoro.log', level=logging.INFO,
                    format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M')
  
  app = QApplication(sys.argv)
  tomato = Pomodoro()
  sys.exit(app.exec_())