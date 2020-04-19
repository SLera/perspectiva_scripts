# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 11:29:25 2015

@author: lselyuzh
"""
import datetime
import numpy as np

# functions import an array of datetime instance from txt
def import_datetime_txt(fname):
    f = open(fname)
    table = [row.strip().split('\t') for row in f]
    f.close()
    date_of_event = np.array(table, int)
    
    dates = []
    for i in range(len(date_of_event)):
        year = date_of_event[i][0]
        month = date_of_event[i][1]
        day = date_of_event[i][2]
        date = datetime.date(year, month, day)
        dates.append(date)

        
    return np.array(dates)
    
#function converts doy to datetime

def doy_datetime(doy,years):
    dates = []
    for i in range(len(years)):
        Jan1 = datetime.date(years[i],1,1)
        date = Jan1+datetime.timedelta((int(doy[i])))
        dates.append(date)
    return dates