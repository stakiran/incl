# -*- coding: utf-8 -*-

import win32api

class KEYCODE:
    ALT = 18
    F4 = 115

class Operator:
    def __init__(self):
        pass

    def press(self, keycode):
        self.keydown(keycode)
        self.keyup(keycode)

    def keydown(self, keycode):
        win32api.keybd_event(keycode, 0, 0)

    def keyup(self, keycode):
        win32api.keybd_event(keycode, 0, 2)
