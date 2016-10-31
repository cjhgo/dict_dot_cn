#coding: utf-8
#created at 16-10-25 17:38
import os
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

            if event.detail ==  66:
                if event.type == X.KeyPress:
                    self.flag +=1
                elif event.type == X.KeyRelease:
                    pass
                if event.type == X.KeyPress and self.flag % 2 == 0:

                    word = os.popen('xsel').read()
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
        self.mythread = threading.Thread(target=self.detect_double_ctrl)
        self.mythread.start()

    def terminate(self):
        self.loc_disp.record_disable_context(self.ctx)
        self.loc_disp.flush()
        self.mythread.join()

