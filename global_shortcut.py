#coding: utf-8
#created at 16-10-25 17:38
import os
import threading
from Xlib.display import Display
from Xlib import X
from Xlib.ext import record
from Xlib.protocol import rq
from dictcn import query_dict
from use_gtk import create_window
from PyQt5.QtCore import pyqtSignal, QObject
from DCtrlSignal import DoubleCtrlSignal



disp = None
flag = 0




def handler(reply):
    global flag
    """ This function is called when a xlib event is fired """
    data = reply.data
    while len(data):
        event, data = rq.EventField(None).parse_binary_value(data, disp.display, None, None)

        if event.detail ==  66:
            if event.type == X.KeyPress:
                flag +=1
            elif event.type == X.KeyRelease:
                pass
            if event.type == X.KeyPress and flag % 2 == 0:

                word = os.popen('xsel').read()
                x = event._data['root_x']
                y = event._data['root_y']
                DoubleCtrlSignal.instance().doublle_ctrl_signal.emit(word, x, y)
        if event.detail == 9:
            DoubleCtrlSignal.instance().esc_signal.emit()



def detect_double_ctrl():
    # get current display
    global disp
    disp = Display()
    root = disp.screen().root

    # Monitor keypress and button press
    ctx = disp.record_create_context(
        0,
        [record.AllClients],
        [{
            'core_requests': (0, 0),
            'core_replies': (0, 0),
            'ext_requests': (0, 0, 0, 0),
            'ext_replies': (0, 0, 0, 0),
            'delivered_events': (0, 0),
            'device_events': (X.KeyReleaseMask, X.ButtonReleaseMask),
            'errors': (0, 0),
            'client_started': False,
            'client_died': False,
        }])
    disp.record_enable_context(ctx, handler)
    disp.record_free_context(ctx)

    while 1:
        # Infinite wait, doesn't do anything as no events are grabbed
        event = root.display.next_event()