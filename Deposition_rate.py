# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 17:44:46 2024

@author: haddadchia
"""

def depositionrate (fromArrayList,qcri, Qinterp_dict, C_dict, falvel_alphai ):
    
    
    
    # calculation of the rate of deposition of particles of size d 
    # using equation developed by  Haddadchi and Rose (2022).
    
    import numpy as np
    ded_dict={}
    for n in fromArrayList:  #loop for each reachID
        if n!=fromArrayList[-1]:    
            dedtemp_dict={}
            for k in range(len(qcri)):  #loop for each fraction 
                ded_temp=np.zeros_like(Qinterp_dict[n])
                for l in range (len(Qinterp_dict[n])):  #loop for each interpolated ata array
                    ded_temp[l,:]=falvel_alphai[k]*C_dict[n][k][l,:]
                    # change negative ded to zero (-ded=0)
                    ded_temp[ded_temp<0]=0
                    
                dedtemp_dict[k]=ded_temp
                del ded_temp
            ded_dict[n]=dedtemp_dict    # deposition rate [kg/m^2/s]
            del dedtemp_dict
        else:
            print ('Sink!',n)
    return ded_dict