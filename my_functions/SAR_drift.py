# -*- coding: utf-8 -*-
"""
Created on Wed Jul 30 17:03:20 2014

@author: lselyuzh
"""
import numpy as np
import datetime
import gdal
from gdalconst import *

class drift_gcp (object):
    
    """ object manually derived ice drift from SAR  """
    def __init__(self,time1,time2,x1,y1,x2,y2,point_ID,point_act):
        self.time1 = time1
        self.time2 = time2
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.point_ID = point_ID
        self.point_act = point_act
        self.drift = None
        self.error = None

def load_drift_gcp(fpath,fname):
    #image1 time
    year1 = int(fname[0:4])
    month1 = int(fname[4:6])
    date1 = int(fname[6:8])
    hour1 = int(fname[9:11])
    minute1 = int(fname[11:13])
    second1 = int(fname[13:15])
    #image2 time
    year2 = int(fname[16:20])
    month2 = int(fname[20:22])
    date2 = int(fname[22:24])
    hour2 = int(fname[25:27])
    minute2 = int(fname[27:29])
    second2 = int(fname[29:31])

    time1 = datetime.datetime(year1, month1, date1, hour1, minute1, second1)
    time2 = datetime.datetime(year2, month2, date2, hour2, minute2, second2)

    
    x1,y1,x2,y2,act = np.loadtxt(fpath+fname,skiprows=5, usecols = (0,1,2,3,8), unpack = True)
    

    for i in range(len(act)):
        if act[i] != False:
            act[i] = True
    point_ID = np.arange(1,len(x1)+1,1)

    drift_points = drift_gcp(time1,time2,x1,y1,x2,y2,point_ID,act)
    return drift_points
    
    
def remove_points(drift_point_object, wrong_points):
    
    for p in range(len(drift_point_object.x1)):
        if drift_point_object.point_ID[p] in wrong_points:
            drift_point_object.point_act[p]=False
    return drift_point_object
    

def calc_drift(drift_gcp_object):
    #pixel resolution in cm
    resolution = 15000
    #timedifference btw images
    dtime = drift_gcp_object.time2-drift_gcp_object.time1    
    #convert dtime to seconds
    dtime = dtime.total_seconds()
    
    dist =  np.sqrt(np.square(drift_gcp_object.x2-drift_gcp_object.x1)+np.square(drift_gcp_object.y2-drift_gcp_object.y1))
    
    drift = dist*resolution/dtime
    
#    #accuracy in pixels
#    acc = 3
#    error = np.sqrt(acc**2+acc**2)
#    error_rel = error*resolution/dtime
    
    return drift
    
    
def tiff_to_latlon(geotiff_fname, x_im,y_im):
    dataset = gdal.Open(geotiff_fname, GA_ReadOnly)
    geotransform = dataset.GetGeoTransform()
    originX = geotransform[0]
    originY = geotransform[3]
    pixelWidth = geotransform[1]
    pixelHeigh = geotransform[5]
    
    from osgeo import osr
    # get the existing coordinate system
    old_cs= osr.SpatialReference()
    old_cs.ImportFromWkt(dataset.GetProjectionRef())
    
    # create the new coordinate system
    wgs84_wkt = """
    GEOGCS["WGS 84",
        DATUM["WGS_1984",
            SPHEROID["WGS 84",6378137,298.257223563,
                AUTHORITY["EPSG","7030"]],
            AUTHORITY["EPSG","6326"]],
        PRIMEM["Greenwich",0,
            AUTHORITY["EPSG","8901"]],
        UNIT["degree",0.01745329251994328,
            AUTHORITY["EPSG","9122"]],
        AUTHORITY["EPSG","4326"]]"""
    new_cs = osr.SpatialReference()
    new_cs .ImportFromWkt(wgs84_wkt)
    
    # create a transform object to convert between coordinate systems
    transform = osr.CoordinateTransformation(old_cs,new_cs) 
         
    #get the coordinates in lat long
    x = x_im*pixelWidth+originX
    y = y_im*pixelHeigh+originY
    lonlat = transform.TransformPoint(x,y)
    lon =lonlat[0]
    lat = lonlat[1]
    return lon, lat