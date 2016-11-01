#coding: utf-8
#created at 16-10-25 17:38
import os
import re
import time
import threading
from Xlib.display import Display
from Xlib import X
from Xlib.ext import record
from Xlib.protocol import rq
from DCtrlSignal import DoubleCtrlSignal







class Detect_Double_Ctrl(object):
    def handler(self, reply):

        """ This function is called when a xlib event is fired """
        data = reply.data
        while len(data):
            event, data = rq.EventField(None).parse_binary_value(data, self.disp.display, None, None)
            if event.detail == 1 and event.type == 5:
                delta = 2
                if self.first_click == 0.0:
                    self.first_click = time.time()
                    print 'a', delta
                else:
                    self.second_click = time.time()
                    delta = self.second_click - self.first_click
                    self.first_click, self.second_click = 0.0, 0.0
                    print delta
                if delta < 1:
                    with os.popen('xsel') as xsel:
                        word = xsel.read()
                        emit = True if re.search(r'[a-zA-z]', word) else False
                        if emit:#double click emit signal only when there exists words selected
                            x = event._data['root_x']
                            y = event._data['root_y']
                            DoubleCtrlSignal.instance().doublle_ctrl_signal.emit(word, x, y)

            if event.detail == 66:
                if event.type == X.KeyPress:
                    self.flag +=1
                elif event.type == X.KeyRelease:
                    pass
                if event.type == X.KeyPress and self.flag % 2 == 0:
                    temp = os.popen('xsel')
                    word = temp.read()
                    temp.close()
                    # double capslock emit signal even though there no words selected to show the window
                    x = event._data['root_x']
                    y = event._data['root_y']
                    DoubleCtrlSignal.instance().doublle_ctrl_signal.emit(word, x, y)

            if event.detail == 9:
                DoubleCtrlSignal.instance().esc_signal.emit()



    def detect_double_ctrl(self):

        root = self.disp.screen().root

        # Monitor keypress and button press
        self.ctx = self.disp.record_create_context(
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
        self.disp.record_enable_context(self.ctx, self.handler)

        self.disp.record_free_context(self.ctx)


    def __init__(self):
        self.disp = Display()
        self.loc_disp = Display()
        self.ctx = None
        self.flag = 0
        self.first_click = 0.0
        self.second_click = 0.0
        self.mythread = threading.Thread(target=self.detect_double_ctrl)
        self.mythread.daemon = True
        self.mythread.start()

    def terminate(self):
        self.loc_disp.record_disable_context(self.ctx)
        self.loc_disp.flush()
        self.mythread.join()
