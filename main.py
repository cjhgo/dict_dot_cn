#coding: utf-8
#created at 16-10-25 17:39


import threading
from global_shortcut import detect_double_ctrl
from application import app, DictDotCn

if __name__ == '__main__':
    global_shortcut_detect_loop = threading.Thread(target= detect_double_ctrl)
    global_shortcut_detect_loop.start()
    ex = DictDotCn()
    # ex = MainWindow()
    # app.installEventFilter(ex)
    app.exec_()
    global_shortcut_detect_loop.join()
