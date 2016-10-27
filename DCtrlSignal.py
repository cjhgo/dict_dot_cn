#coding: utf-8
#created at 16-10-25 17:55
from PyQt5.QtCore import pyqtSignal, QObject


class DoubleCtrlSignal(QObject):
    doublle_ctrl_signal = pyqtSignal(str)

    @staticmethod
    def instance():
        if not hasattr(DoubleCtrlSignal, "_instance"):
            DoubleCtrlSignal._instance = DoubleCtrlSignal()
        return DoubleCtrlSignal._instance
