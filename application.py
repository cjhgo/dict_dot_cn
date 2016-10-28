#coding: utf-8
#created at 16-10-25 18:03
import sys
from PyQt5 import QtCore
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import QTimer
from PyQt5.QtWebKitWidgets import QWebView
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QPlainTextEdit, QLineEdit
from PyQt5.QtWidgets import  QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtCore import QEvent
from DCtrlSignal import DoubleCtrlSignal
from get_rendered_html import MyWebPage


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.dict_widget = DictDotCn(self)
        self.setWindowTitle('Dict.cn')
        self.setCentralWidget(self.dict_widget)
        self.show()




class DictDotCn(QWidget):
    def __init__(self, parent=None):
        super(DictDotCn, self).__init__(parent)
        DoubleCtrlSignal.instance().doublle_ctrl_signal[str, int, int].connect(self.double_ctrl_event)
        DoubleCtrlSignal.instance().esc_signal.connect(self.hide)
        self.fadeflag = True
        self.word = ''
        self.resize(400, 450)

        self.layout =  QVBoxLayout(self)

        self.webview = QWebView()
        self.layout.addWidget(self.webview)

        # self.text = QLineEdit()# QPlainTextEdit()
        # self.text.resize(400, 4)
        # self.text.returnPressed.connect(self.queryword)
        # self.layout.addWidget(self.text)




        self.layout2 = QHBoxLayout()

        self.layout.addWidget(self.webview)
        self.layout.addLayout(self.layout2)

        self.text =QLineEdit()# QPlainTextEdit()
        self.text.resize(400, 4)
        self.text.returnPressed.connect(self.queryword)
        self.layout2.addWidget(self.text)

        self.button = QPushButton('+')
        self.layout2.addWidget(self.button)


        # self.setGeometry(0, 0, 400, 500)



    def queryword(self):
        word = self.text.text()
        # x = self.geometry().x()
        # y = self.geometry().y()
        # self.double_ctrl_event(word, x + 100, y + 100)
        self.double_ctrl_event(word, 0, 0)


    def fadeout(self, opacity):
        if self.fadeflag:
            opacity -= 0.1
            if opacity > 0.2 :
                self.setWindowOpacity(opacity)
                QTimer.singleShot(80, lambda: self.fadeout(opacity))
            else:
                self.hide()
    def double_ctrl_event(self, message, x, y):
        """

        :param message: word to query
        :param x,y: position that selectecd a word
        :return:
        """
        if self.isHidden() or self.word!= message:
            print 'get to here', x, y, message
            self.word = message

            if x > 0 and y > 0:#come from xsel
                self.setGeometry(x+30, y+25, 400, 500)
                self.text.setText(self.word)
            else:#come from text
                pass


            # MyWebPage.instance(self.webview).set_content("http://dict.cn/" + self.word)
            self.webpage = MyWebPage("http://dict.cn/" + self.word, self.webview)
            self.setWindowOpacity(1)
            self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
            self.show()
            QTimer.singleShot(3000, lambda :self.fadeout(1))

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            self.hide()
            self.fadeflag = True

    def enterEvent(self, e):
        """
        when cursor enter window, stop the fadeout effect
        :param e:
        :return:
        """
        self.fadeflag = False

    def leaveEvent(self, e):
        """
        leave from left,
        leave from top,below,right do nothing/not hide so to drag the window
        :param e:
        :return:
        """
        cursor = QCursor()
        x1 = cursor.pos().x()
        y1 = cursor.pos().y()

        x2 = self.geometry().x()
        y2 = self.geometry().y()

        if x1 < x2 and y1 > y2:
            self.hide()
            self.fadeflag = True


    # def mouseMoveEvent(self, e):
    #     print 'get you youyouy'
    #     self.fadeflag = False

    # def eventFilter(self, object, event):
    #     if event.type() == QEvent.MouseMove:
    #         self.fadeflag = False
    #         return False
    #     if event.type() == QEvent.HoverLeave:
    #         print 'fuckfuck'
    #         return False
    #     return False
app = QApplication(sys.argv)


