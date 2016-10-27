#coding: utf-8
#created at 16-10-25 18:03
import sys
from time import  sleep
from PyQt5.QtCore import QUrl
from PyQt5.QtCore import QTimer
from PyQt5.QtWebKitWidgets import QWebView
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget
from DCtrlSignal import DoubleCtrlSignal
from get_rendered_html import MyWebPage
from dictcn import get_html_by_word



class DictDotCn(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()
        DoubleCtrlSignal.instance().doublle_ctrl_signal[str].connect(self.double_ctrl_event)
        self.word = ''
        self.webview = None
        self.initUI()

    def initUI(self):

        w = QWidget(self)

        w.resize(1000, 800)
        w.move(0, 0)
        w.setWindowTitle('Dict.cn')

        self.webview = QWebView(w)

        # view.setUrl(QUrl("http://dict.cn/preliminary"))
        self.webview.load(QUrl("http://dict.cn/" + self.word))
        print '______', self.word, '________'


        # qbtn = QPushButton('Quit', self)
        # qbtn.clicked.connect(self.double_ctrl_event)
        self.setGeometry(0, 0, 1000, 800)
        # self.setWindowTitle('Emit signal')

        # self.word = ''
        # w = QWidget(self)
        #
        # w.resize(500, 500)
        # w.move(300, 300)
        # w.setWindowTitle('Dict.cn')
        #
        # view = QWebView(w)
        #
        # # view.setUrl(QUrl("http://dict.cn/preliminary"))
        # view.load(QUrl("http://dict.cn/" + self.word))
        # view.show()
        # w.show()
        self.show()



    def double_ctrl_event(self, message):
        print message
        self.word = message
        # if self.isHidden():
            # self.show()
            # self.webview.load(QUrl("http://dict.cn/" + self.word))
            # content = get_html_by_word(self.word)
            # self.webview.setHtml(content)
        self.webpage = MyWebPage("http://dict.cn/" + self.word, self.webview)
        self.show()
        QTimer.singleShot(3000, self.hide)
        # else:
        #     self.hide()

    # def show(self):
    #     self.initUI()
    #     super(QMainWindow, self).show()

    def mousePressEvent(self, event):
        self.c.doublle_ctrl_signal.emit()


# if __name__ == '__main__':

app = QApplication(sys.argv)

# print 5
# app.exec_()
    # sys.exit(app.exec_())
