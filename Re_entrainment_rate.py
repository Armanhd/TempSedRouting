# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 17:28:15 2024

@author: haddadchia
"""

def reentrainment (fromArrayList, qcri,Qinterp_dict , Fi_dict,Strmpow_dict,\
                   cri_all_dict,Strmpowcri_dict,depthinterp_dict,rhos, rho, g ):
    
    # calculation of the rate of re-entrainment of particles of size d 
    # using equation developed by  Haddadchi and Rose (2022).
    
    import numpy as np
    ki=0.3 # the fraction of depth through which sediment is lifted [-]
    ryd_dict={}
    for n in fromArrayList: #loop for each reachID 
        if n!=fromArrayList[-1]:
            rydtemp_dict={}    
            for k in range(len(qcri)):  #loop for each fraction 
                ryd_temp=np.zeros_like(Qinterp_dict[n])
                for l in range (len(Qinterp_dict[n])):  #loop for each interpolated data array
                    ryd_temp[l,:]=((Fi_dict[n][0,k]*(Strmpow_dict[n][l,:]-(cri_all_dict[n][0,k]*Strmpowcri_dict[n][l,k]))
                                    /(ki*g*depthinterp_dict[n][l,:])))*(rhos/(rhos-rho))
                    # change negative ryd to zero (-ryd=0 --> E<0 --> scenario 2, only deposition since critical stream power > stream power)
                    ryd_temp[ryd_temp<0]=0
                rydtemp_dict[k]=ryd_temp
                del ryd_temp
            ryd_dict[n]=rydtemp_dict # re-entrainment rate  [kg/m^2/s]
            del rydtemp_dict
        else:
            print ('Sink!',n)
            
    return ryd_dict