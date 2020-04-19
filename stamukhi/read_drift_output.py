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

tif_name = '/home/lera/GOIN/tmp/st26.tif'
drift_txt = '/home/lera/GOIN/Denis/resCBMpirPC_st26_st27_2.txt'
x1,y1,x2,y2,dx,dy, _ = np.loadtxt(drift_txt, unpack='True')

lats1 = []
lons1 = []
lats2 = []
lons2 = []
for i in range(len(x1)):
    lat1, lon1 = Stf. tiff_to_latlon(tif_name, x1[i], y1[i])
    lat2, lon2 = Stf. tiff_to_latlon(tif_name, x2[i], y2[i])
    lats1.append(lat1)
    lons1.append(lon1)
    lats2.append(lat2)
    lons2.append(lon2)
disp = np.sqrt(dx*dx+dy*dy)
table = np.column_stack((lats1,lons1,lats2,lons2,x1,y1,x2,y2,dx,dy,disp))
np.savetxt('resCBMpirPC_st26_st27_2.txt', table, header = 'lats1 lons1 lats2 lon2 x1 y1 x2 y2 dx dy disp_pix', fmt='%1.2f')
