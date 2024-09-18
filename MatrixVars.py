# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 16:49:55 2024

@author: haddadchia
"""

# 
def matrixvar (fromArrayList,dt,reach_distance_dict, depthinterp_dict,qinterp_dict,xpoints_dict, Dispersion_dict ):
    # Matrix variables for solving mass conservation
    alpha_dict={}
    beta_dict={}
    lamba_dict={}
    A1_dict={}
    A2_dict={}
    A3_dict={}
    M1_dict={}
    M2_dict={}
    M3_dict={}
    for n in fromArrayList:
        if n!=fromArrayList[-1]:
            alpha_dict[n]=depthinterp_dict[n]/dt
            dx=reach_distance_dict[n]/(xpoints_dict[n]+2)
            beta_dict[n]=qinterp_dict[n]/(4*dx)
            lamba_dict[n]=(Dispersion_dict[n]*depthinterp_dict[n])/(2*(dx**2))
            A1_dict[n]=(-1*beta_dict[n])+lamba_dict[n]
            A2_dict[n]=alpha_dict[n]+(2*lamba_dict[n])
            A3_dict[n]=beta_dict[n]-lamba_dict[n]
            M1_dict[n]=beta_dict[n]+lamba_dict[n]
            M2_dict[n]=alpha_dict[n]-(2*lamba_dict[n])
            M3_dict[n]=lamba_dict[n]-beta_dict[n]
        else:
            print ('Sink!',n)
                
    return A1_dict, A2_dict, A3_dict, M1_dict, M2_dict, M3_dict