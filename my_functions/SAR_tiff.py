# -*- coding: utf-8 -*-
"""
Created on Tue Aug 05 14:27:07 2014

@author: lselyuzh
"""

import gdal
from gdalconst import * 
import matplotlib
matplotlib.use('qt5agg')
import matplotlib.pyplot as plt

def read_SAR_tiff(filename):
    dataset = gdal.Open(filename, GA_ReadOnly)
    
    cols = dataset.RasterXSize
    rows = dataset.RasterYSize
    bands = dataset.RasterCount
    driver = dataset.GetDriver().LongName
    geotransform = dataset.GetGeoTransform()
    
    originX = geotransform[0]
    originY = geotransform[3]
    pixelWidth = geotransform[1]
    pixelHeigh = geotransform[5]
    
    band = dataset.GetRasterBand(1)
    
    data = band.ReadAsArray(0, 0, cols, rows)
    
    return data
    
def tiff_to_latlon(filename, x_im,y_im):
    dataset = gdal.Open(filename, GA_ReadOnly)
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
    latlong = transform.TransformPoint(x,y) 
    return (latlong[0],latlong[1])