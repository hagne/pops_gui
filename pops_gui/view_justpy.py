# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import justpy as jp
import asyncio
import numpy as np
# import pops_gui.com as pops_com
# import pops_gui.controller as controller

class JustPy(object):
    def __init__(self, controller = None):
        self.controller = controller
        self.wp = jp.WebPage(delete_flag=False)
        self.initiate_plots()
        # jp.justpy(self.initiate_plots, startup = self.task_init)
        
        jp.justpy(self.dummy, startup = self.task_init)
        # self.run()
        
    async def dummy(self):
        return self.wp
    
    async def run(self):
        while True:
            self.active_data = self.controller.communication.get_next_data()
            self.collector_pc = self.collector_pc.append(self.active_data.particle_concentration)
            # print('got data')
            self.update_plots()
            jp.run_task(self.wp.update())
            await asyncio.sleep(0.5)
            
    async def task_init(self):
        jp.run_task(self.run())        
        # print('initiated task')
            
    def update_plots(self):
        self.active_data.plot_siz_distribution(ax = self.a_sd)
        
        cols = ['red', 'black', ] + [str(i) for i in np.linspace(0.2, 0.9, 8)]
        for e,g in enumerate(self.a_sd.get_lines()[::-1]):
            if e > 9:
                g.remove()
            else:
                g.set_color(cols[e])
                g.set_zorder(100-e)
                if e == 0:
                    g.set_linewidth(2)
        
        self.a_sd.set_xlim(-1,15)
        
        self.chart_sd.set_figure(self.f_sd)
        
        # particle concentrations
        self.a_pc.clear()
        self.a_pc.plot(self.collector_pc)
        self.a_pc.set_xlim(self.collector_pc.index.min(), self.collector_pc.index.max())
        self.chart_pc.set_figure(self.f_pc)
        

    
    def initiate_plots(self):
        # get current data
        self.active_data = self.controller.communication.get_next_data()
        
        # size distribution
        self.a_sd = self.active_data.plot_siz_distribution()#ax = self.a_sd)
        self.f_sd = self.a_sd.get_figure()
        self.chart_sd = jp.Matplotlib(figure = self.f_sd, a=self.wp)
        
        # particle concentration
        self.a_pc = self.active_data.plot_particle_concentration()
        # self.a_pc = self.active_data.particle_concentration.plot()
        self.collector_pc = self.active_data.particle_concentration
        self.f_pc = self.a_pc.get_figure()
        self.chart_pc = jp.Matplotlib(figure = self.f_pc, a=self.wp)
        return self.wp
        
        
    
    
    # jp.justpy(plot_test)
    
    
    # jp.justpy(plot_test)#, startup=clock_init)
    
if __name__ == "__main__":
    view = JustPy()