# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 14:14:22 2024

@author: haddadchia
"""

# %%
def sedcoeff (main_dir,median_sed_file,size_class,fromArrayList,hydroDF):
    
    # Coefficients for solving mass consrvation equation and calculating
    # deposition and re-entrainment rates
    # input: directory to csv file with coeffcients and reach characterstics 
    # from  RiverRouting.py
    # output: river bed sediment size and fine sediment deposition maximum 
    # depth, dispersion coeffcient (constant), F coefficient (constant) and
    # number of interpolation steps (user defined)
    import os
    import pandas as pd
    import numpy as np
    
    DmDF=pd.read_csv(os.path.join(main_dir,median_sed_file), header=0, sep=',').sort_values(by = ["HYDSEQ"]) 
    # Dictionary for critical coefficients and max deposition depth
    cri_all_dict={}
    y_dict={}   # maximum deposition depth

    for n in fromArrayList:
        cri_temp=np.zeros((1,len(size_class)))
        reach_interest=hydroDF.index[hydroDF['FROM_NODE']==n]
        cri_temp[0,0]=DmDF.loc[DmDF['nzsegv2']==reach_interest[0], 'critical_strmpow_coef_d1'].iloc[0]
        cri_temp[0,1]=DmDF.loc[DmDF['nzsegv2']==reach_interest[0], 'critical_strmpow_coef_d2'].iloc[0]
        cri_temp[0,2]=DmDF.loc[DmDF['nzsegv2']==reach_interest[0], 'critical_strmpow_coef_d3'].iloc[0]
        cri_temp[0,3]=DmDF.loc[DmDF['nzsegv2']==reach_interest[0], 'critical_strmpow_coef_d4'].iloc[0]
        y_dict[n]=DmDF.loc[DmDF['nzsegv2']==reach_interest[0], 'depo-depth'].iloc[0]
        cri_all_dict[n]=cri_temp # critical streampower coefficients as dictionary for 4 fractions
        del cri_temp
    # Dictionary xpoints
    xpoints_dict={} # 
    for n in fromArrayList:
        reach_interest=hydroDF.index[hydroDF['FROM_NODE']==n]
        xpoints_dict[n]=DmDF.loc[DmDF['nzsegv2']==reach_interest[0], 'xpoints'].iloc[0]
    # Dictionary effective fraction of excess streampower in sediment removal for ryd [-]    
    Fi_dict={}    
    for n in fromArrayList:
        Fi_temp=np.zeros((1,len(size_class)))
        reach_interest=hydroDF.index[hydroDF['FROM_NODE']==n]
        Fi_temp[0,0]=DmDF.loc[DmDF['nzsegv2']==reach_interest[0], 'Fd1'].iloc[0]
        Fi_temp[0,1]=DmDF.loc[DmDF['nzsegv2']==reach_interest[0], 'Fd2'].iloc[0]
        Fi_temp[0,2]=DmDF.loc[DmDF['nzsegv2']==reach_interest[0], 'Fd3'].iloc[0]
        Fi_temp[0,3]=DmDF.loc[DmDF['nzsegv2']==reach_interest[0], 'Fd4'].iloc[0]
        Fi_dict[n]=Fi_temp # F coefficients as dictionary for 4 fractions
        del Fi_temp   
     
    return DmDF , cri_all_dict, Fi_dict, y_dict, xpoints_dict