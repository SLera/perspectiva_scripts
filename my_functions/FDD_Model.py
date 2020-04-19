# -*- coding: utf-8 -*-
"""
Created on Tue Jun 09 18:35:29 2015

@author: lselyuzh
"""

#calculate ice thickness based on a Freezing degee days model (assuming no snow)
#ait temperatures taken from NCEP reanalysis

from netCDF4 import Dataset
import numpy as np
import datetime
from scipy import stats
import matplotlib.pyplot as plt

INDIR = 'D:\\DATA\\NCEP1\\AirT_daily@2m\\'

def read_ncep_airT_manual_reg(year):
    from netCDF4 import Dataset
    INDIR = 'D:\\DATA\\NCEP1\\AirT_daily@2m\\'
    f = Dataset(INDIR +'air.2m.gauss.'+str(year)+'.nc')
    time = f.variables['time'][:]
    airT = f.variables['air'][:]
    lats = f.variables['lat'][:]
    lons = f.variables['lon'][:]
    f.close()
    #convert temperature from Kelvin to Celsius
    airT = airT-273.15 
    #region borgers      
    LIMIT_Southeastern = [71., 125., 78., 139.]
    #find coords of point which belong to the difined region       
    lats_region = np.where((lats>LIMIT_Southeastern[0])&(lats<LIMIT_Southeastern[2]))
    lons_region = np.where((lons>LIMIT_Southeastern[1])&(lons<LIMIT_Southeastern[3]))
    
    #slice data for the region based on lats_region and lons_region
    airT_reg = airT[:,8:10,69:71]
    #point in Buor Khaya
    #airT_Bh = airT[:,68,70]
    #pix at land:
    #lats_reg[1] lons_reg[7]
    #lats_reg[2] lons_reg[0,1]
    #lats_reg[3] lons_reg[0,1,2,4,5,6,7]
    #remove land pixs
   
    airT_reg_nland = np.zeros((len(airT_reg)))
    for i in range(len(airT_reg)):
        nland = airT_reg[i].flatten()
        airT_reg_nland[i] = np.delete(nland, [2]).mean()
    
    return airT_reg_nland



#Hi = (1.33*abs(QDD))**0.58

year = 2011
air_2011 = read_ncep_airT_manual_reg(2011)

date1 = datetime.date(2011,12,6)
date2 = datetime.date(2011,12,10)

date1 = (date1-datetime.date(2011,1,1)).days
date2 = (date2-datetime.date(2011,1,1)).days

FDD=(air_2011[date1:date2+1]).sum()

Hi = (1.33*abs(FDD))**0.58