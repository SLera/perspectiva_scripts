import numpy as np
import matplotlib
matplotlib.use('qt5agg')
import matplotlib.pyplot as plt
import datetime
import os
import glob
from scipy import nanmean
import sys
sys.path.append('/home/lera/GOIN/Perspektiva/Scripts/my_functions/')
import SAR_tiff as Stf
import pygeoj

def mask_land_basemap(lat,lon):
    from mpl_toolkits.basemap import Basemap
    m = Basemap(resolution="i", projection='laea', lat_ts=90, lat_0=90., lon_0=0.,llcrnrlon= 131.73705463408294, llcrnrlat= 79.651813071006984 ,urcrnrlon= 133.06651815041363, urcrnrlat= 68.673879575562182,rsphere=6371228)
    x,y = m (lon,lat)
    land = m.is_land(x,y)
    return land


OUTDIR = '/home/lera/GOIN/Perspektiva/Scripts/input-output/read_drift/'
#tif_name = '/home/lera/GOIN/tmp/st26.tif'
drift_infile = '/home/lera/GOIN/Denis/Results/LS_26Oct2007/20px_ICEDRIFT_20071126T123042_20071127T020852.json'

drift_json = pygeoj.load(drift_infile)


lats1 = []
lons1 = []
lats2 = []
lons2 = []
drift_m = []

for feature in drift_json:
    lat1 = feature._data['properties']['lat1']
    lon1 = feature._data['properties']['lon1']
    land = mask_land_basemap(lat1,lon1)
    if land != 1:
        lats1.append(feature._data['properties']['lat1'])
        lons1.append(feature._data['properties']['lon1'])
        lats2.append(feature._data['properties']['lat2'])
        lons2.append(feature._data['properties']['lon2'])
        #drift_m.append(feature._data['properties']['drift_m'])
        drift_m.append(np.float(feature._data['properties']['drift_m']))
    else:
        print 'land'

table = np.column_stack((lats1,lons1,lats2,lons2,drift_m))
np.savetxt(OUTDIR+'20px_ICEDRIFT_20071126T123042_20071127T020852.json_lm.txt', table, header = 'lats1 lons1 lats2 lon2 drift_m', fmt='%1.2f')
