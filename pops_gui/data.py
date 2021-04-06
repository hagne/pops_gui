#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  2 15:18:31 2021

@author: hagen
"""
import matplotlib.pyplot as plt
import numpy as np

class UdpData(object):
    def __init__(self, data, controller = None, test = False):
        self.controller = controller
        self.raw = data
        self.test = test
        
    @property
    def size_distribution(self):
        cols = [b for b in self.raw.columns if 'bin_' in b]
        sd = self.raw.loc[:,[b for b in self.raw.columns if 'bin_' in b]].astype(int)
        if self.test:
            sd = sd + (np.random.random(sd.shape) * 10)
        return sd 
    
    @property
    def particle_concentration(self):
        return self.raw.PartCon.astype(float)
    
    @property
    def laser_temperature(self):
        return self.raw.LDTemp.astype(float)
    
    @property
    def pressure_temperatur_unit(self):
        ptu = self.raw.loc[:,['P', "TofP"]].astype(float)
        ptu.columns = ['Pressure', 'Temperature']
        return ptu
    
    @property
    def baseline(self):
        df = self.raw.loc[:,['BL', 'STD']].astype(float)
        df.columns = ['baseline', 'std']
        return df
    
        
    def plot_siz_distribution(self, ax = None):
        if isinstance(ax, type(None)):
            a = plt.subplot()
            a.set_title('particle size distribution')
            a.set_ylabel('Particle numbers')
        else:
            a = ax
        a.plot(self.size_distribution.values[0])
        return a
    
    def plot_particle_concentration(self, ax = None):
        if isinstance(ax, type(None)):
            a = plt.subplot()
            a.set_title('particle number concentration')
            a.set_ylabel('particle number concentration (#/cm^-3)')
        else:
            a = ax
        a.plot(self.particle_concentration)
        return a
        
    
if __name__ == "__main__":
    data = UdpData(test = True)
    