#coding: utf-8
#created at 16-10-25 17:39


import sys
from global_shortcut import Detect_Double_Ctrl #detect_double_ctrl
from application import app, DictDotCn, MainWindow

if __name__ == '__main__':
    key_event_loop = Detect_Double_Ctrl()
    ex = DictDotCn(key_listen_loop=key_event_loop)
    # ex = MainWindow()
    # app.installEventFilter(ex)
    sys.exit(app.exec_())
