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

# plt.plot([1, 23, 2, 4])
# plt.ylabel('some numbers')

f,a = plt.subplots()

class MyApp(App):

    def build(self):
        box = BoxLayout()
        box.add_widget(FigureCanvasKivyAgg(plt.gcf()))
        return box

MyApp().run()


