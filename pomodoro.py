#coding: utf-8

import os
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


BASE=60


class PauseableTimer(QTimer):
  COUNT = 0 
  DUR = 2400
  def __init__(self, target,task,indicator):
    QTimer.__init__(self,target)    
    self.timeout.connect(self.onTimeout)
    self.target = target
    self.task = task
    self.indicator=indicator
    self.onBreak = False
    self.counter = PauseableTimer.DUR

  def cur(self):
    td = timedelta(seconds=self.counter)
    td_str = str(td)[2:]
    return td_str

  def setCount(self, cnt):    
    PauseableTimer.DUR = cnt*BASE
    self.counter = PauseableTimer.DUR
    self.target.display(self.cur())
    self.indicator.display(self.cur())

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
    self.indicator.display("00:00")

  def onTimeout(self):
    self.target.display(self.cur())
    self.indicator.display(self.cur())
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
    self.counter=5*60
    self.start_()
    os.system("notify-send  task-done  -i /usr/lib/firefox/browser/icons/mozicon128.png -u critical")    
  
  def onBreakDue(self):  
    logging.info("Okay, it is time to work!")
    os.system("notify-send  -t 0 go-to-work -u critical")    
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
    self.task.setText("task")

    self.lcd = QLCDNumber(self)
    self.lcd.display("00:00")    
    self.lcd.setMinimumSize(400,400)

    self.indicator = QLCDNumber()
    self.indicator.display("00:00")        
    self.indicator.setMinimumSize(75,55)
    self.pat = PauseableTimer(self.lcd,self.task,self.indicator)
  
    self.start = QPushButton(self)
    self.start.setText("start")
    self.start.released.connect(self.pat.start_)

    self.pause = QPushButton(self)
    self.pause.setText("pause")
    self.pause.released.connect(self.pat.pause)

    self.stop = QPushButton(self)
    self.stop.setText("stop")
    self.stop.released.connect(self.pat.stop_)
  
    self.setTL=QPushButton(self)  
    self.setTL.setText("set dur,minutes")
    self.setTL.released.connect(lambda: self.pat.setCount(int(self.taskDur.text())))
    
  
    self.log = QLineEdit(self)
    self.append = QPushButton(self)
    self.append.setText("append")
    self.append.released.connect(lambda: logging.critical("------"+self.log.text()))
    
    self.control.addWidget(self.taskDur,0,0,Qt.AlignLeft)
  
    self.control.addWidget(self.task,0,1,1,3)#从0,1位置开始,跨1行,跨3列

    self.control.addWidget(self.lcd,1,0,1,4)

    self.control.addWidget(self.start,2,0)
    self.control.addWidget(self.pause,2,1)
    self.control.addWidget(self.stop,2,2)
    self.control.addWidget(self.setTL,2,3)
    self.control.addWidget(self.log, 3,0,1,3)
    self.control.addWidget(self.append,3,3)

    self.content.setLayout(self.control)

    self.content.resize(400,600)
    self.setCentralWidget(self.content)    
    self.show()
    frameGm = self.indicator.frameGeometry()
    screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
    bottomRight = QApplication.desktop().screenGeometry(screen).bottomRight()
    frameGm.moveCenter(bottomRight)
    self.indicator.move(frameGm.bottomRight())
    self.indicator.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
    self.indicator.show()


if __name__ == "__main__":
  logging.basicConfig(filename='/var/log/pomodoro.log', level=logging.INFO,
                    format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M')
  app = QApplication(sys.argv)
  tomato = Pomodoro()
  sys.exit(app.exec_())