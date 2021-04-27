#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  2 14:26:34 2021

@author: hagen
"""

import pandas as pd
import socket
import pops_gui.data
import serial


class Listen2UDP(object):
    def __init__(self,
                 port = 10080,
                 verbose = False,
                 controller = None,
                 test = False):
        
        self.controller = controller
        self.port = port
        self._verbose = verbose
        self.test = test
        
        self._socket_inbound = None
        self.data = pd.DataFrame()
    
    @property
    def socket_inbound(self):
        if isinstance(self._socket_inbound, type(None)):
            socket_in = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            socket_in.bind(('',self.port))
            self._socket_inbound = socket_in
            if self._verbose:
                print(f'Listening on port {self.port}.')
        return self._socket_inbound
                
      
    def get_next_data(self):
        df = pd.DataFrame()
        # try:
#         for i in range(2):    #print ('Hello')
            # Receive UDP packets
        
        if self.test:
            data = 'POPS,POPS-190,/media/usb0/Data/F20210402/HK_20210402x003.csv,20210402T201453,72893.8042,3,0,553,553,185.83,2315,2335,6.72,7.49,839.88,34.65,141.43,15.14,29.24,2.98,229.45,43.63,610.11,1021.98,22.44,11.26,2.87,1.78,30000,3.0,16,1.75,4.81,0,8,255,512,102,100,87,75,45,65,54,13,8,2,0,1,1,0,0,0\r\n'
        else:
            dataline, address = self.socket_inbound.recvfrom(8192)
            # show POPS name
            data = dataline.decode('utf-8')
        
        data = str(data).split(',')
        data = [d.strip() for d in data]
        #print(datastr)
    #     test = datastr.split(',')
    #     pName = test[1]


        # Echo to stdout
        # print ('Received string: %s' %dataline)
        # print('No Problem')
    #     df = df.append(datastr.split(','))
        ts = data[3]
        ts = pd.to_datetime(ts,#[:8+1+], 
                       format = '%Y%m%dT%H%M%S')

        labels = "DateTime,TimeSSM,Status,DataStatus,PartCt,HistSum,PartCon,BL,BLTH,STD,MaxSTD,P,TofP, PumpLife_hrs,WidthSTD,AveWidth, POPS_Flow, PumpFB, LDTemp, LaserFB, LD_Mon, Temp, BatV, Laser_Current, Flow_Set,BL_Start,TH_Mult,nbins,logmin,logmax,Skip_Save,MinPeakPts,MaxPeakPts,RawPt"
        colnames_extra = ['instrument', 'serial_no', 'file_name_on_instrument'] + labels.split(',')
        colnames = colnames_extra + [f'bin_{i+1:03d}' for i in range(len(data)-len(colnames_extra))]
        colnames = [col.strip() for col in colnames]
#             df = df.append(pd.DataFrame([data], index = [ts]))
        df = pd.DataFrame([data], index = [ts], columns = colnames)
        return pops_gui.data.UdpData(df, test = self.test)
    
class Listen2Serial(object): 
    def __init__(self,
                 port = '/dev/ttyUSB0',
                 baudrate = 115200, #port 1: 9600/ port 2: 115200
                 verbose = False,
                 controller = None,
                 test = False):
        self.controller = controller
        self.port = port
        self.baudrate = baudrate
        self._verbose = verbose
        self.test = test
        
        self._socket_inbound = None
        self.data = pd.DataFrame()
    
    @property
    def socket_inbound(self):
        if isinstance(self._socket_inbound, type(None)):
            # socket_in = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # socket_in.bind(('',self.port))
            self._socket_inbound = serial.Serial(self.port, self.baudrate, timeout=1)
            if self._verbose:
                print(f'Listening on port {self.port}.')
        return self._socket_inbound
    
    def get_next_data(self):
        df = pd.DataFrame()
        # try:
#         for i in range(2):    #print ('Hello')
            # Receive UDP packets
        
        if self.test:
            data = 'POPS,POPS-190,/media/usb0/Data/F20210402/HK_20210402x003.csv,20210402T201453,72893.8042,3,0,553,553,185.83,2315,2335,6.72,7.49,839.88,34.65,141.43,15.14,29.24,2.98,229.45,43.63,610.11,1021.98,22.44,11.26,2.87,1.78,30000,3.0,16,1.75,4.81,0,8,255,512,102,100,87,75,45,65,54,13,8,2,0,1,1,0,0,0\r\n'
        else:
            # dataline, address = self.socket_inbound.recvfrom(8192)
            # show POPS name
            # data = dataline.decode('utf-8')
            line = self.socket_inbound.readline()   # read a '\n' terminated line
            data = line.decode(encoding='UTF-8')
        
        data = str(data).split(',')
        data = [d.strip() for d in data]
        #print(datastr)
    #     test = datastr.split(',')
    #     pName = test[1]


        # Echo to stdout
        # print ('Received string: %s' %dataline)
        # print('No Problem')
    #     df = df.append(datastr.split(','))
        ts = data[3]
        ts = pd.to_datetime(ts,#[:8+1+], 
                       format = '%Y%m%dT%H%M%S')

        labels = "DateTime,TimeSSM,Status,DataStatus,PartCt,HistSum,PartCon,BL,BLTH,STD,MaxSTD,P,TofP, PumpLife_hrs,WidthSTD,AveWidth, POPS_Flow, PumpFB, LDTemp, LaserFB, LD_Mon, Temp, BatV, Laser_Current, Flow_Set,BL_Start,TH_Mult,nbins,logmin,logmax,Skip_Save,MinPeakPts,MaxPeakPts,RawPt"
        colnames_extra = ['instrument', 'serial_no', 'file_name_on_instrument'] + labels.split(',')
        colnames = colnames_extra + [f'bin_{i+1:03d}' for i in range(len(data)-len(colnames_extra))]
        colnames = [col.strip() for col in colnames]
#             df = df.append(pd.DataFrame([data], index = [ts]))
        df = pd.DataFrame([data], index = [ts], columns = colnames)
        return pops_gui.data.UdpData(df, test = self.test)
    
if __name__ == "__main__":
    com = Listen2UDP(test = True)


