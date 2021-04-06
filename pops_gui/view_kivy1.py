#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  5 09:58:54 2021

@author: hagen

Notes:
    potentially usefull links:
        https://stackoverflow.com/questions/22831879/how-to-create-real-time-graph-in-kivy
        https://stackoverflow.com/questions/44905416/how-to-get-started-use-matplotlib-in-kivy
        https://stackoverflow.com/questions/53630158/add-points-to-the-existing-matplotlib-scatter-plot
        

"""

from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
import matplotlib.pyplot as plt
from kivy.clock import Clock
import numpy as np

# plt.plot([1, 23, 2, 4])
# plt.ylabel('some numbers')

# f,a = plt.subplots()

class MyApp(App):
    def build(self):
        box = BoxLayout()
        self.f,self.a = plt.subplots()
        
        y = np.random.random(10)
        self.a.plot(y)
        
        Clock.schedule_interval(self.update_clock, 1)
        box.add_widget(FigureCanvasKivyAgg(self.f))
        return box
    
    def update_clock(self, *args):
        # Called once a second using the kivy.clock module
        # Add one second to the current time and display it on the label
        # self.now = self.now + timedelta(seconds = 1)
        # self.my_label.text = self.now.strftime('%H:%M:%S')
        y = np.random.random(10)
        self.a.plot(y)
        print('blab')
    

MyApp().run()


