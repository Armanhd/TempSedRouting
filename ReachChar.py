# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 14:31:33 2024

@author: haddadchia
"""

# %% 
def reachchar (DmDF,uniqueNodeList,fromArrayList,  hydroDF, main_dir, 
               reach_charac_file):
    # River reach characteristics including river bed gradient and distance 
    # from next reach downstream
    import os
    import pandas as pd
    import numpy as np
    slope_dict={}
    reach_distance_dict={}
    reachID_dict={}
    Dm_dict={}
    Dispersioncoeff_dict={}

    reach_charac=pd.read_csv(os.path.join(main_dir,reach_charac_file), 
                             header=0, sep=',')         # reach characteristics
    for n in uniqueNodeList:
        res_temp=fromArrayList.count(n)
        if res_temp>0:
            reach_interest=hydroDF.index[hydroDF['FROM_NODE']==n]
            slope=reach_charac.loc[reach_charac['nzsegv2']==reach_interest[0],
                                   'rch_slope_grad'].iloc[0]
            slope_dict[n]=slope # River bed slope [m/m]
            reach_distance=reach_charac.loc[reach_charac['nzsegv2']==reach_interest[0],
                                            'rch_length_m'].iloc[0]
            Dm_dict[n]=DmDF.loc[DmDF['nzsegv2']==reach_interest[0], \
                                'median_diameter'].iloc[0]  # dictionary for the median size of sediment [m] for each reach
            Dispersioncoeff_dict[n]=DmDF.loc[DmDF['nzsegv2']==reach_interest[0],\
                                             'Dispersion'].iloc[0]  # dictionary for the dispersion coefficient for each reach - Dispersion has a multiplier of 250
            reach_distance_dict[n]=reach_distance
            reachID_dict[n]=reach_interest[0]
            del slope, reach_distance        
        else: 
            reach_interest=hydroDF.index[hydroDF['TO_NODE']==n]
            print ('This is the sink reach', reach_interest[0])
           
    return slope_dict, reach_distance_dict, reachID_dict, Dm_dict, Dispersioncoeff_dict