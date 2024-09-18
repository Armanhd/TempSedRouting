# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 17:38:13 2024

@author: haddadchia
"""

def scenario_model (fromArrayList, qcri, Strmpow_dict, Qinterp_dict,Strmpowcri_dict ):
    # Selecting modelling scenarios based on deposition and re-entrainment rate = 
    # using Haddadchi and Rose (2022)
    
    #scenario selection: Scenario 2 is when StreamPower < StreamPower_Cr; Scenario 4 is when StreamPower > StreamPower_Cr
    
    import numpy as np
    dyd_dict={}     # deposition depth rate [m]
    E_dict={}       # E rate (deposition - erosion rate) [kg/m^2/s]
    scen_dict={}
    for n in fromArrayList:
        if n!=fromArrayList[-1]:
            scentemp_dict={}
            Etemp_dict={}
            dydtemp_dict={}
            for k in range(len(qcri)):
                scentemp=np.zeros_like(Strmpow_dict[n])+2
                Etemp=np.zeros_like(Strmpow_dict[n])
                dydtemp=np.zeros_like(Strmpow_dict[n])
                for l in range (len(Qinterp_dict[n])):
                    scentemp[l,:]=np.where(Strmpow_dict[n][l,:]>Strmpowcri_dict[n][l,k]+(0.000000001*Strmpowcri_dict[n][l,k]), 4, scentemp[l,:])
                    #scentemp[l,:]=np.where(Strmpow_dict[n][l,:]>Strmpowcri_dict[n][l,k], 4, scentemp[l,:]) # if equal does not get involved
                    #if critical coefficients to be included in scenario decision making    
                    #scentemp[l,:]=np.where(Strmpow_dict[n][l,:]>((Strmpowcri_dict[n][l,k]*cri_all_dict[n][0,k])+(0.000000001*Strmpowcri_dict[n][l,k])), 4, scentemp[l,:])
                     #Etemp[l,:]=np.where(Strmpow_dict[n][l,:]>Strmpowcri_dict[n][l,k]+(0.000000001*Strmpowcri_dict[n][l,k]),ryd_dict[n]-ded,(-1*ded ))    
                scentemp_dict[k]=scentemp
                Etemp_dict[k]=Etemp
                dydtemp_dict[k]=dydtemp
                del scentemp
            scen_dict[n]=scentemp_dict
            E_dict[n]=Etemp_dict
            dyd_dict[n]=dydtemp_dict
            del scentemp_dict, Etemp_dict, dydtemp_dict 
        else:
            print ('Sink!',n)
       
    return scen_dict, E_dict, dyd_dict