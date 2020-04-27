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
    m = Basemap(resolution="l", projection='laea', lat_ts=90, lat_0=90., lon_0=0., llcrnrlon=131.73705463408294,
                llcrnrlat=79.651813071006984, urcrnrlon=133.06651815041363, urcrnrlat=68.673879575562182,
                rsphere=6371228)
    x,y = m (lon,lat)
    land = m.is_land(x,y)
    return land


OUTDIR = '/home/lera/GOIN/Perspektiva/Scripts/input-output/read_drift/'
#tif_name = '/home/lera/GOIN/tmp/st26.tif'
drift_infile = '/home/lera/GOIN/Denis/Results/LS_03Dec2007/20px_ICEDRIFT_20071203T121532_20071206T022547.json'

def json_to_txt(jsonfile,maskland):

    drift_json = pygeoj.load(jsonfile)
    lats1 = []
    lons1 = []
    lats2 = []
    lons2 = []
    drift_m = []
    n=0
    for feature in drift_json:
        n+=1
        print 'new feature', n
        lat1 = feature._data['properties']['lat1']
        lon1 = feature._data['properties']['lon1']

        if maskland == True:
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
        else:
            lats1.append(feature._data['properties']['lat1'])
            lons1.append(feature._data['properties']['lon1'])
            lats2.append(feature._data['properties']['lat2'])
            lons2.append(feature._data['properties']['lon2'])
            drift_m.append(np.float(feature._data['properties']['drift_m']))

    return lats1,lons1,lats2,lons2,drift_m

ml = 1
lats1,lons1,lats2,lons2,drift_m = json_to_txt(drift_infile, ml)

table = np.column_stack((lats1,lons1,lats2,lons2,drift_m))
np.savetxt(OUTDIR+'20px_ICEDRIFT_20071203T121532_20071206T022547.json_lm.txt', table, header = 'lats1 lons1 lats2 lon2 drift_m', fmt='%1.2f')
