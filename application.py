#coding: utf-8
#created at 16-10-25 18:03
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton
from DCtrlSignal import DoubleCtrlSignal


class DictDotCn(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()

        self.initUI()


    def initUI(self):
        DoubleCtrlSignal.instance().doublle_ctrl_signal.connect(self.double_ctrl_event)
        qbtn = QPushButton('Quit', self)
        qbtn.clicked.connect(self.double_ctrl_event)
        self.setGeometry(300, 300, 290, 150)
        self.setWindowTitle('Emit signal')
        self.show()

    def double_ctrl_event(self):
        print 'ahhhhh'
        if self.isHidden():
            self.show()
        else:
            self.hide()

    def mousePressEvent(self, event):
        self.c.doublle_ctrl_signal.emit()


# if __name__ == '__main__':

app = QApplication(sys.argv)

# print 5
# app.exec_()
    # sys.exit(app.exec_())
