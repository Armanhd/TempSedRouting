# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 16:17:00 2024

@author: haddadchia
"""

# %%
def interpolhydro (fromArrayList,toArray, unitflowdict, depthdict, Qdict, xpoints_dict):
    # Linear interpolation of hydrological data
    import os
    import pandas as pd
    import numpy as np
    from datetime import datetime
    import scipy
    qinterp_dict={}     # empty disctionary for interpolated unitflow
    depthinterp_dict={} # empty dictionary for interpolated depth
    Qinterp_dict={} # empty dictionary for interpolated flow
    segment=0
    for n in fromArrayList:
        if n!=fromArrayList[-1]:
            print(n)
            #print(segment)
            q_US=np.array(unitflowdict[n])
            q_DS=np.array(unitflowdict[toArray[segment]])
            depth_US=np.array(depthdict[n])
            depth_DS=np.array(depthdict[toArray[segment]])
            Q_US=np.array(Qdict[n])
            Q_DS=np.array(Qdict[toArray[segment]])
            qinterp=np.zeros((len(q_US),xpoints_dict[n]+2))
            qinterp_struct=scipy.interpolate.interp1d([1,xpoints_dict[n]+2], np.vstack([q_US,q_DS]),kind='linear',axis=0)
            depthinterp=np.zeros((len(depth_US),xpoints_dict[n]+2))
            depthinterp_struct=scipy.interpolate.interp1d([1,xpoints_dict[n]+2], np.vstack([depth_US,depth_DS]),kind='linear',axis=0)
            Qinterp=np.zeros((len(Q_US),xpoints_dict[n]+2))
            Qinterp_struct=scipy.interpolate.interp1d([1,xpoints_dict[n]+2], np.vstack([Q_US,Q_DS]),kind='linear',axis=0)
            for i in range(xpoints_dict[n]+2):
                #depthinterp[:,i]=depthinterp_struct(i+1)
                qinterp[:,i]=qinterp_struct(i+1)
                depthinterp[:,i]=depthinterp_struct(i+1)
                Qinterp[:,i]=Qinterp_struct(i+1)
            qinterpt=np.transpose(qinterp)
            qinterp_dict[n]=qinterpt  # filled dictionary for interpolated unitflow
            depthinterpt=np.transpose(depthinterp)
            depthinterp_dict[n]=depthinterpt # filled dictionary for interpolated depth
            Qinterpt=np.transpose(Qinterp)
            Qinterp_dict[n]=Qinterpt # filled dictionary for interpolated flow
            segment=segment+1
        else:
            print ('Sink!',n)
    interp_out=pd.DataFrame({'depth_interp':depthinterp_dict,'q_interp':qinterp_dict}) # output of interpolations as data frame

    return (qinterp_dict, depthinterp_dict, Qinterp_dict, interp_out)
    
    
    