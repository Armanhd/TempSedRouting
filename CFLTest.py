# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 16:36:12 2024

@author: haddadchia
"""

def cfl (fromArrayList, Dispersion_dict,depthinterp_dict,reach_distance_dict,xpoints_dict, dt ):
    #The Courant-Friedrichs-Lewy (CFL) condition provides a stability criterion 
    # for numerical solutions of partial differential equations, 
    # In solving the mass conservation equation numerically, 
    # a conservative CFL number of 0.1 was used to avoid significant numerical dispersion. 
    import numpy as np
    
    CFL_min_dict={}
    CFL_max_dict={}
    for n in fromArrayList:
        if n!=fromArrayList[-1]:
            Dispersion_min=np.min(Dispersion_dict[n])
            depth_min=np.min(depthinterp_dict[n])
            Dispersion_max=np.max(Dispersion_dict[n])
            depth_max=np.max(depthinterp_dict[n])
            dx=reach_distance_dict[n]/(xpoints_dict[n]+2)
            CFL_min_dict[n]=(Dispersion_min*dt)/(dx**2) # Minimum of CFL number
            CFL_max_dict[n]=(Dispersion_max*dt)/(dx**2)
        else:
            print ('Sink!',n)
    return CFL_min_dict, CFL_max_dict