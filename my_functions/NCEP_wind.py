# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 19:30:50 2015

@author: lselyuzh
"""

from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
import datetime
import math
import matplotlib.dates as mdates

#Plots probability density dunctions of wind speed in four sectors

def read_ncep_wind_6h(year):
    upath = 'D:\\DATA\\NCEP1\\Wind_6h@10m\\UWind\\uwnd.10m.gauss.'
    vpath = 'D:\\DATA\\NCEP1\\Wind_6h@10m\\VWind\\vwnd.10m.gauss.'
    #get u-wind component and the grid
    f = Dataset(upath+str(year)+'.nc')
    time = f.variables['time'][:]
    lats = f.variables['lat'][:]
    lons = f.variables['lon'][:]
    uwind = f.variables['uwnd'][:]
    #get v-wind component (time, lats, long identical to u-wind vars)
    f = Dataset(vpath+str(year)+'.nc')
    vwind = f.variables['vwnd'][:]
#    #reagion borgers      
#    LIMIT_Southeastern = [71., 125., 78., 139.]
#    #find coords of point which belong to the difined reion       
#    lats_region = np.where((lats>LIMIT_Southeastern[0])&(lats<LIMIT_Southeastern[2]))
#    lons_region = np.where((lons>LIMIT_Southeastern[1])&(lons<LIMIT_Southeastern[3]))
 
    #slice data for the region based on lats_region and lons_region
    uwind_reg = uwind[:,6:10,67:75]
    vwind_reg = vwind[:,6:10,67:75]
    lats_reg = lats[6:10]
    lons_reg = lons[67:75]
    #return uwind_reg,vwind_reg,lats_reg,lons_reg,time
    
    ##central part of the SELS
#    uwind_reg = uwind[:,7:9,69:73]
#    vwind_reg = vwind[:,7:9,69:73]
#    lats_reg = lats[7:9]
#    lons_reg = lons[69:73]

#   ##73N135E
#    uwind_reg = uwind[:,8:9,71:72]
#    vwind_reg = vwind[:,8:9,71:72]
#    lats_reg = lats[8:9]
#    lons_reg = lons[71:72]
    
    wtime = np.arange(0,(len(time)/4)+0.25,0.25)
    
    return uwind_reg.flatten(),vwind_reg.flatten(),lats_reg,lons_reg, wtime
    
#u,v,lats,lons,time = read_ncep_wind(1999)

class Wind(object):
    
    """ mean ncep wind, 4 sectors"""

    def __init__(self,sectors,date1,date2):    
       #24 sector 0-360
       self.sectors = sectors
       #timeframe of the period of integration
       self.date1 = date1
       self.date2 = date2
    


def wind_speed_direction_6h(date1,date2):
#     ''' Returns: 6-hours value of mean wind speed (speed), azimuth of wind vector (direction), 
#    horisontal and vertical wind speed components (U,V),day of year(doy)  btw date1 and date2
#    Input:date1, date2 consequtive dates as datetime.date variables'''
    #ddays = (date2-date1).days
    u_year1,v_year1,lats,lons,time1 = read_ncep_wind(date1.year)
    u_year2,v_year2,lats,lons,time2 = read_ncep_wind(date2.year)
    if date1.year == date2.year:
        u_year,v_year,lats,lons,time = u_year1,v_year1,lats,lons,time1
        #dates relative to Jan1 of year1 (index of u and v for respective dates)
        date1_index = (date1 - datetime.date(date1.year,1,1)).days+1
        date2_index = (date2 - datetime.date(date1.year,1,1)).days+1
    else:
        u_year = np.concatenate((u_year1,u_year2))
        v_year = np.concatenate((v_year1,v_year2))
        #dates relative to Jan1 of year1 (index of u and v for respective dates)
        date1_index = (date1 - datetime.date(date1.year,1,1)).days+1
        date2_index = (date2 - datetime.date(date2.year,1,1)).days+1+(len(time1)/4)
    
    time = np.arange(date1_index,(date2_index+1),0.25)
 
    speed = np.zeros(len(time))
    direction = np.zeros(len(time))
    U = np.zeros(len(time))
    V = np.zeros(len(time))
    doy_6h = np.zeros(len(time))
        
    for i in range(len(time)):
        #print i
        u = u_year[i].mean()
        v = v_year[i].mean()
        wspeed = np.sqrt(np.square(v)+np.square(u))
        wdir_sin = np.abs(u/wspeed)
        #print wdir_sin
        if u == 0. and v > 0:
            wdir = 0
        if u == 0. and v < 0:
            wdir = 180
         
        if (u > 0.) and (v >= 0.) :
            wdir = math.degrees(np.arcsin(wdir_sin))

        if (u > 0.) and ( v < 0.):
            wdir = 180 - math.degrees(np.arcsin(wdir_sin))

        if (u < 0.) and (v < 0.) :
            wdir = 180 + math.degrees(np.arcsin(wdir_sin))
            
        if (u < 0.) and ( v >= 0.):
            wdir = 360 - math.degrees(np.arcsin(wdir_sin))

            
        speed[i]=wspeed
        direction[i]=wdir
        U[i]=u
        V[i]=v
        doy_6h[i]=time[i]
        
    return speed, direction, U,V, doy_6h
    
