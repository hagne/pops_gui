#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  2 15:22:07 2021

@author: hagen
"""

import pops_gui.data
# import pops_gui.view_justpy
import pops_gui.view_kivy
import pops_gui.com

class Controller(object):
    def __init__(self, test = False):
        # self.communication = pops_gui.com.Listen2UDP(controller = self, test = test)
        self.communication = pops_gui.com.Listen2Serial(controller = self, test = test)
        self.view = pops_gui.view_kivy.View_Kivy(controller = self, test = test)
        self.view.run()
        # self.view = pops_gui.view_justpy.JustPy(controller = self)
        
        
        
        
if __name__ == "__main__":
    view = Controller(test = False)