# -*- coding: utf-8 -*-

import win32api
import win32con

def get_dispsize():
    dispx = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
    dispy = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
    return dispx, dispy
