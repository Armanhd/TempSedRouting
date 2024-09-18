# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 16:26:10 2024

@author: haddadchia
"""

# %%

def disperustar (fromArrayList,depthinterp_dict,slope_dict, g, Dispersioncoeff_dict):
    # calculating dispersion term in mass conservation using the approach
    #proposed by Fischer et al. (1979)
    
    import numpy as np
    ustar_dict={}
    Dispersion_dict={}
    for n in fromArrayList:
        if n!=fromArrayList[-1]:
            ustar_dict[n]=np.sqrt(g*depthinterp_dict[n]*slope_dict[n])
            Dispersion_dict[n]=Dispersioncoeff_dict[n]*depthinterp_dict[n]*ustar_dict[n] # k=250u*h [m^2/s] as suggested by Fischer et al. (1979), coefficient for dispersion term is considered as 250
        else:
            print ('Sink!',n)
    return (ustar_dict, Dispersion_dict)