#!/usr/bin/python
#coding: utf-8
#created at 16-10-25 17:39

import sys
import argparse
import logging
from global_shortcut import Detect_Double_Ctrl #detect_double_ctrl
from application import app, DictDotCn, MainWindow

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='dict.cn client.')
    parser.add_argument('--env')
    args = parser.parse_args()
    env = args.env or 'develop'
    if env == 'develop':
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(levelname)s %(message)s', datefmt='%Y-%m-%d %H:%M')
    elif env == 'production':
        logging.basicConfig(filename='/var/log/dict.cn.log', level=logging.INFO,
                            format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M')
    key_event_loop = Detect_Double_Ctrl()
    ex = DictDotCn(key_listen_loop=key_event_loop)
    # ex = MainWindow()
    # app.installEventFilter(ex)
    sys.exit(app.exec_())
