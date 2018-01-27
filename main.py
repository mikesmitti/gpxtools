#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 29.05.2017

@author: MikeSmitti

# 6. Nachkommastelle entspricht Dezimeter
# 5. Nachkommastelle entspricht Meter

'''

import tkinter
from class_gpx_tools_gui import cgui as gui
#import os


if __name__ == '__main__':
    root = tkinter.Tk()
    root.wm_title("GPX-Tools by Mike")
    app = gui(root)
    app.mainloop()
