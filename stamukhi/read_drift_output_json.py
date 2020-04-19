import numpy as np
import matplotlib
matplotlib.use('qt5agg')
import matplotlib.pyplot as plt
import datetime
import os
import glob
from scipy import nanmean
import sys
sys.path.append('/home/lera/GOIN/Scripts/My_functions/')
import SAR_tiff as Stf
import pygeoj



#tif_name = '/home/lera/GOIN/tmp/st26.tif'
drift_infile = '/home/lera/GOIN/Denis/Results/LS_26Oct2007/20px_ICEDRIFT_20071126T123042_20071127T020852.json'

drift_json = pygeoj.load(drift_infile)


lats1 = []
lons1 = []
lats2 = []
lons2 = []
drift_m = []

for feature in drift_json:
    lats1.append(feature._data['properties']['lat1'])
    lons1.append(feature._data['properties']['lon1'])
    lats2.append(feature._data['properties']['lat2'])
    lons2.append(feature._data['properties']['lon2'])
    #drift_m.append(feature._data['properties']['drift_m'])
    drift_m.append(np.float(feature._data['properties']['drift_m']))

table = np.column_stack((lats1,lons1,lats2,lons2,drift_m))
np.savetxt('20px_ICEDRIFT_20071126T123042_20071127T020852.json.txt', table, header = 'lats1 lons1 lats2 lon2 drift_m', fmt='%1.2f')
