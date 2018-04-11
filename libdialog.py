# -*- coding: utf-8 -*-

import ctypes
import win32con

def message_box(message, title, mbtype):
    return ctypes.windll.user32.MessageBoxW(
        0,
        str(message),
        str(title),
        mbtype
    )

def ok(message, title):
    message_box(message, title, win32con.MB_OK)
