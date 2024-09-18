# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 15:49:30 2024

@author: haddadchia
"""
# %%

def hydrologydata (firstdate,lastdate, hydroDF, US_reach, fromArrayList, flow_dir_name):
    # extracting unitflow, depth and flow for each river reach
    # from hydrological model
    # For this study NZWAM - TopNet model
    # Input date and time of start and end of flood, reachID, and 
    # directory for hydrological data
    # date and time should be entered in this format, format= 'yyyy-mm-dd HH:MM:SS' 
    # data in a format of Netcdf, compressed CSV, or anytime series format can be used
    # for this study input data were in 1 hour intervals
    import os
    import pandas as pd
    import numpy as np
    from datetime import datetime
    firststpart_file='Manawatu_TeacherCollege-STEC-Hrly_output-nzsegment_'  # first part of the flow csv files (common on all files)
    lastpart_file='_20170101-20191231_P1..csv.gz'   # last part of the flow csv files (common on all files)
    difference_dates=datetime.strptime(lastdate, '%Y-%m-%d %H:%M:%S')-datetime.strptime(firstdate, '%Y-%m-%d %H:%M:%S')
    hours=int(difference_dates.total_seconds() / 3600)
    # read flow data and make timeseries
    datearray=pd.DataFrame()
    unitflowarray=np.zeros((len(hydroDF),(hours-1)))
    Qarray=np.zeros((len(hydroDF),(hours-1)))
    deptharray=np.zeros((len(hydroDF),(hours-1)))
    # a loop to read flow data and depth data from list of csv files
    for m in range(len(hydroDF)):    
        print (US_reach[m])       
        interestreach_file=firststpart_file+str(US_reach[m])+lastpart_file        
        #rows_to_ignore=list(range (1,firstrow_to_include))+list(range ((lastrow_to_include+1),totalrow_flowdata))
        #print (rows_to_ignore)
        # flowdata=pd.read_csv(os.path.join(flow_dir_name,interestreach_file), 
        #                      compression='gzip',skiprows=lambda x: x in rows_to_ignore, 
        #                      header=0, sep=',', quotechar='"')         # nrows=100, , error_bad_lines=False
        
        #++++++++++++++++++++++++++++++
        # Alternative flow extraction using dates
        flowdata1=pd.read_csv(os.path.join(flow_dir_name,interestreach_file), 
                             compression='gzip', header=0, sep=',',
                             parse_dates=["datetime"], quotechar='"')         # nrows=100, , error_bad_lines=False
        #flowdata=pd.read_csv(os.path.join(flow_dir_name,interestreach_file), compression='gzip',skiprows=lambda x: x in rows_to_ignore, header=0, sep=',',parse_dates=["datetime"], quotechar='"')# flow selection based on row number (not first and last date)
        mask=(flowdata1['datetime']>firstdate)& (flowdata1['datetime']<lastdate)
        flowdata=flowdata1.loc[mask]
        #+++++++++++++++++++++++++++++++
        
        datetime=flowdata['datetime'].values
        temp_datetime=pd.DataFrame({'datetime': datetime})
        unitflow=flowdata['unit_flow'].values
        depth=flowdata['water_level'].values
        Q=flowdata['mod_streamq'].values
        datearray=pd.concat([datearray,temp_datetime], axis=1)
        unitflowarray[m,:]=unitflow
        deptharray[m,:]=depth
        Qarray[m,:]=Q
    datetimearray=np.array(datearray, dtype='datetime64[s]')
    # make unitflow, flow and depth dictionary including fromArray (FROM_NODE) as index and arrays of input flow for each reach
    listunitflow=unitflowarray.tolist()
    unitflowdict=dict(zip(fromArrayList,listunitflow)) # dictionary of fromArray(index) and flow data
    listdepth=deptharray.tolist()
    depthdict=dict(zip(fromArrayList,listdepth)) # dictionary of fromArray(index) and depth data
    listQ=Qarray.tolist()
    Qdict=dict(zip(fromArrayList,listQ)) # dictionary of fromArray(index) and depth data
    return datearray, unitflowdict, depthdict, Qdict