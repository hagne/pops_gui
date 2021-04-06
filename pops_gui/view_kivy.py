#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  5 09:58:54 2021

@author: hagen

Todo:
    - Apply the initiate_plot function to all the others (excet the sizedistribution)
    - add an intensity plot for the changing sizedistribution
    - add an alltime average for size distribution into the plot
    - allow to change to log scale for all plots
    - limits, clear_button, log-lin toggle

Notes:
    potentially usefull links:
        https://stackoverflow.com/questions/22831879/how-to-create-real-time-graph-in-kivy
        https://stackoverflow.com/questions/44905416/how-to-get-started-use-matplotlib-in-kivy
        https://stackoverflow.com/questions/53630158/add-points-to-the-existing-matplotlib-scatter-plot        

"""

from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.accordion import Accordion, AccordionItem
import matplotlib.pyplot as plt
from kivy.clock import Clock
import numpy as np
import pandas as pd

class FigDic(dict):
    def __init__(self,fig = None, ax = None, at = None, collector = None, column = None, dataset_name = None, lines = [], cursor = None):
        super().__init__(fig = fig, ax = ax, at = at, collector = collector, column = column, dataset_name = dataset_name, lines = lines, cursor = cursor)
    
    @property
    def fa(self):
        if isinstance(self['fig'], type(None)):
            self['fig'] = self['ax'].get_figure()
        return self['fig'], self['ax'], self['at']

class View_Kivy(App):
    def __init__(self, controller = None, test = False):
        super().__init__()
        self.test = test
        self.controller = controller
        self.plots = {}
        
        
    def build(self):
        Clock.schedule_interval(self.update_clock, 1)
        self.active_data = self.controller.communication.get_next_data()
        
####    Tab structure
        tabs = TabbedPanel()
        tabs.do_default_tab = False
        
        tab_measure = TabbedPanelItem()
        tabs.add_widget(tab_measure)
        tabs.default_tab = tab_measure
        tab_measure.text = 'Measure'
        
        tab_analytics = TabbedPanelItem()
        tabs.add_widget(tab_analytics)
        tab_analytics.text = 'Analytics'
        
        tab_auxiliary = TabbedPanelItem()
        tabs.add_widget(tab_auxiliary)
        tab_auxiliary.text = 'Auxiliary'
     
####    Tab measurement
        box = BoxLayout()
        tab_measure.add_widget(box)
        box.orientation = 'vertical'

        self.initiate_plots_sizedistribution(box)
        self.initiate_plots_numberconcentration(box)        

####    Tab analytics
        ta_accordion = Accordion()
        tab_analytics.add_widget(ta_accordion)
        ta_accordion.orientation = 'vertical'
        
        #### Tab analytics BL
        accorditem = AccordionItem()
        ta_accordion.add_widget(accorditem)
        accorditem.title = 'Baseline'
        self.initiate_plot(accorditem, 'baseline', ['baseline', 'std'], ['baseline (digitizer bins)', 'standard diviation'])
        
        #### Tab analytics laser
        ta_accordion_laser = AccordionItem()
        ta_accordion.add_widget(ta_accordion_laser)
        ta_accordion_laser.title = 'Laser'
        self.initiate_plots_laser(ta_accordion_laser)
        
        #### Tab analytics flow
        accorditem = AccordionItem()
        ta_accordion.add_widget(accorditem)
        accorditem.title = 'Flow rate'
        self.initiate_plot(accorditem, 'flow_rate', ['flow_rate',], ['flow rate (cc/s)', ])

####    Tab auxiliary
        
        
        tau_accordion = Accordion()
        tab_auxiliary.add_widget(tau_accordion)
        tau_accordion.orientation = 'vertical'
        
        #### Tab analytics PT
        tau_accordion_ptu = AccordionItem()
        tau_accordion.add_widget(tau_accordion_ptu)
        tau_accordion_ptu.title = 'PTU'
        self.initiate_plots_ptu(tau_accordion_ptu)
        
        return tabs
    
    def update_clock(self, *args):
        # return
        self.active_data = self.controller.communication.get_next_data()
        self.update_sizedistribution()
        self.update_particle_numbers()
        self.update_laser()
        self.update_ptu()
        self.update_plot('baseline')
        self.update_plot('flow_rate')
        
        
    def initiate_plot(self, container, dataset, column, ylabel):       
        """
        universal function to initiate timeseries plots (all but the 
        sizedistribution).
        
        Parameters
        ----------
        container : TYPE
            DESCRIPTION.
        dataset : TYPE
            Name of the attribute of the data instance (active_data).
        column : TYPE
            DESCRIPTION.
        ylabel : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        if isinstance(column, (list)):
            pass
        elif isinstance(column, str):
            column = [column,]
            ylabel = [ylabel,]
        else:
            assert(False), 'not possible'
        
        assert(len(column) <= 2), 'so far only 2 columns plottable'
        
        collector = getattr(self.active_data, dataset)
        f,a = plt.subplots()
        f.autofmt_xdate()
        
        a.plot(collector.loc[:,column[0]])
        a.set_ylabel(ylabel[0], color = 'red')        
        
        if len(column) == 2:
            at = a.twinx()
            at.plot(collector.loc[:,column[1]])
            at.set_ylabel(ylabel[1], color = 'blue')
        
        else:
            at = None
        
        container.add_widget(FigureCanvasKivyAgg(f))
        self.plots[dataset] = FigDic(fig = f, ax = a, at = at, collector = collector, column = column, dataset_name = dataset)
        return 
    
    def update_plot(self, plot_name):
        plotinfo = self.plots[plot_name]
        collector = plotinfo['collector']
        dataset_name = plotinfo['dataset_name']
        column = plotinfo['column']
        f,a,at = plotinfo.fa
        if self.test:
            cpt = collector.iloc[[-1]].copy()
            # print(cpt)
            scale = 0.5 * cpt.iloc[0]
            cpt.iloc[0] += scale * np.random.random(cpt.iloc[0].shape[0]) - (scale/2)
            cpt.index += pd.to_timedelta(1, 'D')
            # collector = 
            # collector.append(cpt, inplace=True)
            # print(cpt.index.values[0])
            collector.loc[cpt.index.values[0]] = cpt.values[0]
            # print(collector)
        else:
            cpt = getattr(self.active_data, dataset_name) #)#self.active_data.pressure_temperatur_unit)
            collector.loc[cpt.index.values[0]] = cpt.values[0]
        # f,a = self.plots['ptu'].fa 
        g = a.get_lines()[-1]
        g.remove()
        a.plot(collector.loc[:,column[0]], color = 'red')
        
        if not isinstance(at, type(None)):
            # at = a.get_shared_x_axes().get_siblings(a)[0]
            g = at.get_lines()[-1]
            g.remove()
            at.plot(collector.loc[:,column[1]], color = 'blue')
        f.canvas.draw()   
        return
  
        
        

    def initiate_plots_ptu(self, container):       
        f,a = plt.subplots()
        self.plots['ptu'] = FigDic(fig = f, ax = a)
        at = a.twinx()
        
        a.set_ylabel('Pressure (mbar)', color = 'red')
        
        self.collector_ptu = self.active_data.pressure_temperatur_unit
        a.plot(self.collector_ptu.loc[:,'Pressure'])

        at.plot(self.collector_ptu.loc[:,'Temperature'])
        container.add_widget(FigureCanvasKivyAgg(f))
        at.set_ylabel('T (°C)', color = 'blue')
        return 
    
    def update_ptu(self):
        if self.test:
            cpt = self.collector_ptu.iloc[[-1]].copy()
            scale = 10
            cpt.iloc[0] += (10 * np.random.random(2)) - (scale/2)
            cpt.index += pd.to_timedelta(1, 'D')
            self.collector_ptu = self.collector_ptu.append(cpt)
        else:
            self.collector_ptu = self.collector_ptu.append(self.active_data.pressure_temperatur_unit)

        f,a, at = self.plots['ptu'].fa 
        g = a.get_lines()[-1]
        g.remove()
        a.plot(self.collector_ptu.loc[:,'Pressure'], color = 'red')
        
        at = a.get_shared_x_axes().get_siblings(a)[0]
        g = at.get_lines()[-1]
        g.remove()
        at.plot(self.collector_ptu.loc[:,'Temperature'], color = 'blue')
        
        f.canvas.draw()   
        return

    def initiate_plots_laser(self, container):       
        f,a = plt.subplots()
        
        a.set_ylabel('T (°C)')
        a.set_title('Laser diode temperature')

        self.collector_laser_t = self.active_data.laser_temperature
        a.plot(self.collector_laser_t)
        
        self.plots['laser_temp'] = FigDic(fig = f, ax = a)

        container.add_widget(FigureCanvasKivyAgg(f))

        return 
    
    def update_laser(self):
        if self.test:
            cpt = self.collector_laser_t.iloc[[-1]].copy()
            # print(type(cpt))
            scale = 10
            cpt.iloc[0] += (10 * np.random.random()) - (scale/2)
            cpt.index += pd.to_timedelta(1, 'D')
            self.collector_laser_t = self.collector_laser_t.append(cpt)
            # print(self.collector_laser_t)
        else:
            self.collector_laser_t = self.collector_laser_t.append(self.active_data.laser_temperature)
        # else:
        #     self.collector_pc = self.collector_pc.append(pd.DataFrame([np.random.random()]))
        # print(self.collector_pc)
        f,a, at = self.plots['laser_temp'].fa 
        g = a.get_lines()[-1]
        # print(len(a.get_lines()))
        g.remove()
        a.plot(self.collector_laser_t, color = 'red')
        # print(self.collector_laser_t)
        f.canvas.draw()
        
    def update_particle_numbers(self):
        if self.test:
            cpt = self.collector_pc.iloc[[-1]].copy()
            # print(type(cpt))
            scale = 10
            cpt.iloc[0] += (10 * np.random.random()) - (scale/2)
            cpt.index += pd.to_timedelta(1, 'D')
            self.collector_pc = self.collector_pc.append(cpt)
        else:
            self.collector_pc = self.collector_pc.append(self.active_data.particle_concentration)
        # else:
        #     self.collector_pc = self.collector_pc.append(pd.DataFrame([np.random.random()]))
        # print(self.collector_pc)
        f,a, at = self.plots['numberconcentration'].fa 
        g = a.get_lines()[-1]
        # print(len(a.get_lines()))
        g.remove()
        a.plot(self.collector_pc, color = 'red')
        f.canvas.draw()


    def initiate_plots_sizedistribution(self, container):
        f,a = plt.subplots()
        
        a.set_title('particle size distribution')
        a.set_ylabel('Particle numbers')
  
        g, = a.plot(self.active_data.size_distribution.columns, self.active_data.size_distribution.values[0])
        
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
        
        f,a,at = self.plots['sizedistribution'].fa
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


