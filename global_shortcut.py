#coding: utf-8
#created at 16-10-25 17:38
import os
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



    # def __init__(self, *args, **kwargs):
    #     super(QObject, self).__init__(*args, **kwargs)
    #     self.


def handler(reply):
    global flag
    """ This function is called when a xlib event is fired """
    data = reply.data
    while len(data):
        event, data = rq.EventField(None).parse_binary_value(data, disp.display, None, None)

        # KEYCODE IS FOUND USERING event.detail
        # print event.detail
        if event.detail ==  37:
            # print event.detail

            # print 'ctrl'
            if event.type == X.KeyPress:
                # BUTTON PRESSED
                flag +=1
                # print flag
                # print "pressed"
            elif event.type == X.KeyRelease:
                # BUTTON RELEASED
                # print "released"
                pass
            if event.type == X.KeyPress and flag % 2 == 0:
                # print flag%2
                word = os.popen('xsel').read()
                # create_window.main()
                print word
                # print query_dict(words=word)#.encode('utf-8')
                DoubleCtrlSignal.instance().doublle_ctrl_signal.emit()
            # else:
            #     create_window.main_quit()



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
