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
import pandas as pd

class FigDic(dict):
    def __init__(self,fig = None, ax = None, lines = [], cursor = None):
        super().__init__(fig = fig, ax = ax, lines = lines, cursor = cursor)
    
    @property
    def fa(self):
        if isinstance(self['fig'], type(None)):
            self['fig'] = self['ax'].get_figure()
        return self['fig'], self['ax']

class View_Kivy(App):
    def __init__(self, controller = None, test = False):
        super().__init__()
        self.test = test
        self.controller = controller
        self.plots = {}
        
        
    def build(self):
        Clock.schedule_interval(self.update_clock, 1)
        
        self.active_data = self.controller.communication.get_next_data()
        box = BoxLayout()
        box.orientation = 'vertical'

        self.initiate_plots_sizedistribution(box)
        self.initiate_plots_numberconcentration(box)        
        
        return box
    
    def update_clock(self, *args):
        # return
        self.active_data = self.controller.communication.get_next_data()
        self.update_sizedistribution()
        self.update_particle_numbers()
    

        
    def update_particle_numbers(self):
        if 1:
            self.collector_pc = self.collector_pc.append(self.active_data.particle_concentration)
        # else:
        #     self.collector_pc = self.collector_pc.append(pd.DataFrame([np.random.random()]))
        # print(self.collector_pc)
        f,a = self.plots['numberconcentration'].fa 
        g = a.get_lines()[-1]
        # print(len(a.get_lines()))
        g.remove()
        a.plot(self.collector_pc, color = 'red')
        f.canvas.draw()


    def initiate_plots_sizedistribution(self, container):
        f,a = plt.subplots()
        
        a.set_title('particle size distribution')
        a.set_ylabel('Particle numbers')
  
        g, = a.plot(self.active_data.size_distribution.values[0])
        
        self.plots['sizedistribution'] = FigDic(fig = f, ax = a, lines = [g,])
        # self.chart_sd = jp.Matplotlib(figure = self.f_sd, a=self.wp)
        container.add_widget(FigureCanvasKivyAgg(f))
        f.canvas.mpl_connect('button_press_event', self.onclick_sd)
        # f.canvas.draw()

    def onclick_sd(self, event):
        # print(event.x)
        # print(event.xdata)
        # print(event.inaxes)
        
        bla = self.plots['sizedistribution']['cursor']
        if not isinstance(bla, type(None)):
            cursor, text = bla
            cursor.remove()
            text.remove()
        
        a = event.inaxes
        cursor = a.axvline(event.xdata)
        text = a.text(event.xdata, event.ydata, f'{event.xdata:0.3f}')
        self.plots['sizedistribution']['cursor'] = (cursor, text)
        
        event.canvas.draw()
        
    def update_sizedistribution(self):
        
        f,a = self.plots['sizedistribution'].fa
        self.active_data.plot_siz_distribution(ax = a)
        g = a.get_lines()[-1]
        
        lines = self.plots['sizedistribution']['lines']
        lines.append(g)
        
        cols = ['red', 'black', ] + [str(i) for i in np.linspace(0.2, 0.9, 8)]
        # for e,g in enumerate(a.get_lines()[::-1]):
        for e,g in enumerate(lines[::-1]):
            if e > 9:
                g.remove()
                lines.pop(lines.index(g))
            else:
                g.set_color(cols[e])
                g.set_zorder(100-e)
                if e == 0:
                    g.set_linewidth(2)
        
        f.canvas.draw()
        
    def initiate_plots_numberconcentration(self, container):
        # if 0:
        #     a = self.active_data.plot_particle_concentration()
        #     self.collector_pc = self.active_data.particle_concentration
        # else:
        #     a = plt.subplot()
        #     self.collector_pc = pd.DataFrame([np.random.random()])
        #     a.plot(self.collector_pc)
            
        # # self.a_pc = self.active_data.particle_concentration.plot()
        # f = a.get_figure()     
        
        f,a = plt.subplots()
        
        a.set_ylabel('particle number concentration (#/cm^-3)')
        a.set_title('particle number concentration')

        self.collector_pc = self.active_data.particle_concentration
        a.plot(self.collector_pc)

        self.plots['numberconcentration'] = FigDic(fig = f, ax = a)

        # self.chart_pc = jp.Matplotlib(figure = self.f_pc, a=self.wp)
        container.add_widget(FigureCanvasKivyAgg(f))
        # f.canvas.draw()

        return 





# MyApp().run()


