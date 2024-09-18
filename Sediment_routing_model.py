# -*- coding: utf-8 -*-
"""
Created on Tue Feb  7 11:54:58 2023

@author: haddadchia
"""

# %% Sediment routing model
# one dimensional sediment routing model with the relationship describing 
# conservation of sediment mass subjected to advection and dispersion


#%% import packages
import pandas as pd
import numpy as np
import os
import scipy
# %% reading hydroDF file which has all nzsegv2, HYDSEQ, FROM_NODE, TO_NODE

import RiverRouting
hydroDF, US_reach, fromArrayList, toArray, toArrayList,uniqueNodeList=RiverRouting.riverrouting(
    main_dir_routing,routing_file)


#%% import suspended sediment sizes, and alpha coefficients for each fraction

import SuspSedChar
size_class, di, c_alpha=SuspSedChar.suspchar(main_dir,sediment_size_file)

#%% import median riverbed diameter and critical stream power coefficients as dataframe

import SedimentCoeff
DmDF, cri_all_dict, Fi_dict, y_dict, xpoints_dict=SedimentCoeff.sedcoeff(main_dir,median_sed_file,size_class,fromArrayList,hydroDF)

#%% import reach characteristics data (slope and distance from do)


import ReachChar
slope_dict, reach_distance_dict, reachID_dict, Dm_dict, Dispersioncoeff_dict\
    = ReachChar.reachchar (DmDF,uniqueNodeList,fromArrayList,  hydroDF, main_dir,
                           reach_charac_file)
#%% import constants
Rrho=1.65       # R=((rohs/rho)-1),rhos=2650, rho=1000 - no unit
g=9.806         # acceleration gravity [m/s^2]
mcoef=1             # drag/roughness coefficients (1-10) [-]
kv=0.4          # von-Karman coefficient
SF=0.1  # sand fraction in proportion (0 - 1)
rho=1000        # Density of water [kg/m^3]
rhos=2650 # sediment density [kg/m^3]
Rrho=1.65       # R=((rohs/rho)-1),rhos=2650, rho=1000 - no unit
g=9.805         # acceleration gravity [m/s^2]
nu=0.0000010533 # kinematic viscosity [m^2/s]
#% import time step
dt=60 *60   # time step 1 hour [s]

#%% read flow data from TopNet

import Hydrologicalinput
datearray, unitflowdict, depthdict, Qdict=Hydrologicalinput.\
    hydrologydata(firstdate,lastdate, hydroDF, US_reach, fromArrayList,
                  flow_dir_name)

#%--------------------Calculations-----------------------
#%% Interpolation of unitflow (qinterp_dict), flow (Qinterp_dict), depth (depthinterp_dict)

import InterploationHydro
qinterp_dict, depthinterp_dict, Qinterp_dict, interp_out=InterploationHydro.interpolhydro (
    fromArrayList,toArray, unitflowdict, depthdict, Qdict, xpoints_dict)


#%% calculate dispersion coefficient [m^2/s] and ustar [m/s]

import DispersionUstar
ustar_dict, Dispersion_dict=DispersionUstar.disperustar(fromArrayList,depthinterp_dict,slope_dict, g, Dispersioncoeff_dict)

#%% Courant-Friedrichs-Lewy (CFL) condition
# To avoid numerical dispersion, the CFL number should be less than or equal to 0.5: CFL<=0.5

import CFLTest
CFL_min_dict, CFL_max_dict=CFLTest.cfl(fromArrayList, Dispersion_dict,depthinterp_dict,
                                       reach_distance_dict,xpoints_dict, dt )

#%% calculation of alpha, beta, lambda for matrix
# calculate A(left matrix) and M(right matrix)

import MatrixVars
A1_dict, A2_dict, A3_dict, M1_dict, M2_dict, M3_dict=MatrixVars.matrixvar (
    fromArrayList,dt,reach_distance_dict, depthinterp_dict,qinterp_dict,xpoints_dict, Dispersion_dict )
    

#%% import C 
# Add initial and boundary conditions for C (sediment concentration)    
import ICBCsediment
C_dict=ICBCsediment.icbc (fromArrayList, Qinterp_dict,c_alpha,main_dir, sediment_conc_file )

#%% calculate fall velocity from separate Python
import FallVelocity

falveli=FallVelocity.fallvelocity (di)
falvel_alphai=falveli*c_alpha

#%% Calculate critical discharge and critical streampower (regression)

import CriticalValues
Strmpowcri_dict,Qcr_dict, qcr_dict, widthcr_dict, Strmpow_dict, qcri=CriticalValues.critical_strmpow_q_Q (fromArrayList,SF, kv, rho, Rrho, g, Dm_dict, di, mcoef, slope_dict,Qinterp_dict, qinterp_dict )


#%% calculate re-entrainment rate [kg/m^2/s]
# re-entrainment rate for each reach (n=1,2...), each fraction (i=1,2,3,4) and each interpolated flow ([xinterp+2])
     
import Re_entrainment_rate

ryd_dict=Re_entrainment_rate.reentrainment (fromArrayList, qcri,Qinterp_dict , Fi_dict,Strmpow_dict,\
                   cri_all_dict,Strmpowcri_dict,depthinterp_dict,rhos, rho, g )
#%% scenario selection: Scenario 2 is when StreamPower < StreamPower_Cr; Scenario 4 is when StreamPower > StreamPower_Cr

        
import Scenario_model        

scen_dict, E_dict, dyd_dict=Scenario_model.scenario_model (fromArrayList, qcri, Strmpow_dict, Qinterp_dict,Strmpowcri_dict )


#%% deposition rate [kg/m^2/s]

    
import Deposition_rate
ded_dict=Deposition_rate.depositionrate(fromArrayList,qcri, Qinterp_dict, C_dict, falvel_alphai )

#%% Calculate C: Matrix solution --> Main
n_us1=0 
n_us2=0
for n in fromArrayList:
    if n==n_us1 or n==n_us2 or n==fromArrayList[-1]:    # for not running again another upper tributary of 2-tribuaties situation
        continue
    else:        
        num_step, num_time=C_dict[n][0].shape      # number of interpolated steps+ up/down reaches (xpoints+2), number of time
        tonode_temp=hydroDF.TO_NODE[hydroDF['FROM_NODE']==n].iloc[0]
        toreach_temp=hydroDF.index[hydroDF['TO_NODE']==tonode_temp]
        # 2-tributaries    
        if len (toreach_temp)==2:   # 2-tributaries
            n_us1=hydroDF.FROM_NODE[toreach_temp[0]]
            n_us2=hydroDF.FROM_NODE[toreach_temp[1]]
            for k in range(len(qcri)): #loop for each fraction 
                # n_us1
                t_before=0
                for j in range(1,num_time): #step at each time step
                    ded_dict[n_us1][k][:,t_before]=falvel_alphai[k]*C_dict[n_us1][k][:,t_before]
                    # change negative ded to zero (-ded=0)
                    ded_dict[n_us1][k][:,t_before][ded_dict[n_us1][k][:,t_before]<0]=0
                    
                    for l in range (len(Qinterp_dict[n_us1])): ##step at each space step
                        # if  scen_dict[n_us1][k][l,t_before]==2:     # scenario 2 (deposition only)
                        #     E_dict[n_us1][k][l,t_before]=-1*ded_dict[n_us1][k][l,t_before]
                        #     dyd_dict[n_us1][k][l,t_before]=(ded_dict[n_us1][k][l,t_before]/rhos)*dt     # deposition depth rate [m]
                        # elif scen_dict[n_us1][k][l,t_before]==4:    # scenario 4 (erosion and deposition)
                        E_dict[n_us1][k][l,t_before]=ryd_dict[n_us1][k][l,t_before]-ded_dict[n_us1][k][l,t_before]    
                        dyd_dict[n_us1][k][l,t_before]=((ded_dict[n_us1][k][l,t_before]-ryd_dict[n_us1][k][l,t_before])/rhos)*dt    # deposition depth rate [m]
                    
                    # matrix solution
                    # making matrix A for time step ahead (t+1)= j
                    A=scipy.sparse.spdiags([np.append(A1_dict[n_us1][1:,j],[0]), A2_dict[n_us1][:,j], np.append([0],A3_dict[n_us1][:-1,j])], (-1,0,1), xpoints_dict[n_us1]+2, xpoints_dict[n_us1]+2).toarray()
                    # making matrix M for current time step (t)=j-1
                    M=scipy.sparse.spdiags([np.append(M1_dict[n_us1][1:,j-1],[0]), M2_dict[n_us1][:,j-1], np.append([0],M3_dict[n_us1][:-1,j-1])], (-1,0,1), xpoints_dict[n_us1]+2, xpoints_dict[n_us1]+2).toarray()
                    MC=np.matmul(M,C_dict[n_us1][k][:,t_before]) # matrix multiplication for right-hand eqn (M * Cj)
                    MCE= MC+E_dict[n_us1][k][:,t_before]    # MC+E which E is (E=r-d) for one time step back
                    Cleft_array=np.linalg.solve (A, MCE) # solve matrix to find Cj+1
                    # change negative C to zero (-C=0)
                    Cleft_array[Cleft_array<0]=0
                    
                    Cleft_array[0]=C_dict[n_us1][k][0,j]    # Add boundary condition to each step after solving the matrix
                    C_dict[n_us1][k][:,j]=Cleft_array
                    t_before=t_before+1
                    del Cleft_array, A, M, MC, MCE
                  
                # n_us2
                t_before=0
                for j in range(1,num_time): #step at each time step
                    ded_dict[n_us2][k][:,t_before]=falvel_alphai[k]*C_dict[n_us2][k][:,t_before]
                    # change negative ded to zero (-ded=0)
                    ded_dict[n_us2][k][:,t_before][ded_dict[n_us2][k][:,t_before]<0]=0
                                        
                    for l in range (len(Qinterp_dict[n_us2])): ##step at each space step
                        # if  scen_dict[n_us2][k][l,t_before]==2:     # scenario 2 (deposition only)
                        #     E_dict[n_us2][k][l,t_before]=-1*ded_dict[n_us2][k][l,t_before]
                        #     dyd_dict[n_us2][k][l,t_before]=(ded_dict[n_us2][k][l,t_before]/rhos)*dt     # deposition depth rate [m]
                        # elif scen_dict[n_us2][k][l,t_before]==4:    # scenario 4 (erosion and deposition)
                        E_dict[n_us2][k][l,t_before]=ryd_dict[n_us2][k][l,t_before]-ded_dict[n_us2][k][l,t_before]
                        dyd_dict[n_us2][k][l,t_before]=((ded_dict[n_us2][k][l,t_before]-ryd_dict[n_us2][k][l,t_before])/rhos)*dt    # deposition depth rate [m]
                        
                    # matrix solution
                    A=scipy.sparse.spdiags([np.append(A1_dict[n_us2][1:,j],[0]), A2_dict[n_us2][:,j], np.append([0],A3_dict[n_us2][:-1,j])], (-1,0,1), xpoints_dict[n_us2]+2, xpoints_dict[n_us2]+2).toarray()
                    M=scipy.sparse.spdiags([np.append(M1_dict[n_us2][1:,j-1],[0]), M2_dict[n_us2][:,j-1], np.append([0],M3_dict[n_us2][:-1,j-1])], (-1,0,1), xpoints_dict[n_us2]+2, xpoints_dict[n_us2]+2).toarray()
                    MC=np.matmul(M,C_dict[n_us2][k][:,t_before]) # matrix multiplication for right-hand eqn (M * Cj)
                    MCE= MC+E_dict[n_us2][k][:,t_before]    # MC+E which E is (E=r-d) for one time step back
                    Cleft_array=np.linalg.solve (A, MCE) # solve matrix to find Cj+1
                    # change negative C to zero (-C=0)
                    Cleft_array[Cleft_array<0]=0                    
                    
                    Cleft_array[0]=C_dict[n_us2][k][0,j]    # Add boundary condition to each step after solving the matrix
                    C_dict[n_us2][k][:,j]=Cleft_array
                    t_before=t_before+1
                    del Cleft_array, A, M, MC, MCE                    
                C_dict[tonode_temp][k][0,:]=C_dict[n_us1][k][num_step-1,:] + C_dict[n_us2][k][num_step-1,:] #BC for Downstream reach
                C_dict[tonode_temp][k][:,0]=C_dict[n_us1][k][0,0] + C_dict[n_us2][k][0,0] #IC for Downstream reach (or singl: C_dict[tonode_temp][k][:,0]=C_dict[n_us1][k][0,0] )
                #C_dict[tonode_temp][k][:,0]=C_dict[n_us1][k][0,0]    #IC for Downstream reach (or combined: C_dict[tonode_temp][k][:,0]=C_dict[n_us1][k][0,0] + C_dict[n_us2][k][0,0])
        
        # 1-tributary        
        elif len (toreach_temp)==1:    # 1-tributary
            n_us=hydroDF.FROM_NODE[toreach_temp[0]]
            for k in range(len(qcri)): #loop for each fraction 
                t_before=0
                for j in range(1,num_time): #step at each time step
                    ded_dict[n_us][k][:,t_before]=falvel_alphai[k]*C_dict[n_us][k][:,t_before]
                    # change negative ded to zero (-ded=0)
                    ded_dict[n_us][k][:,t_before][ded_dict[n_us][k][:,t_before]<0]=0                    
                    
                    for l in range (len(Qinterp_dict[n_us])): ##step at each space step
                        # if  scen_dict[n_us][k][l,t_before]==2:
                        #     E_dict[n_us][k][l,t_before]=-1*ded_dict[n_us][k][l,t_before]
                        #     dyd_dict[n_us][k][l,t_before]=(ded_dict[n_us][k][l,t_before]/rhos)*dt     # deposition depth rate [m]
                        # elif scen_dict[n_us][k][l,t_before]==4:
                            E_dict[n_us][k][l,t_before]=ryd_dict[n_us][k][l,t_before]-ded_dict[n_us][k][l,t_before]    
                            dyd_dict[n_us][k][l,t_before]=((ded_dict[n_us][k][l,t_before]-ryd_dict[n_us][k][l,t_before])/rhos)*dt    # deposition depth rate [m]
                            
                    # matrix solution
                    # making matrix A for time step ahead (t+1)= j
                    A=scipy.sparse.spdiags([np.append(A1_dict[n_us][1:,j],[0]), A2_dict[n_us][:,j], np.append([0],A3_dict[n_us][:-1,j])], (-1,0,1), xpoints_dict[n_us]+2, xpoints_dict[n_us]+2).toarray()
                    # making matrix M for current time step (t)=j-1
                    M=scipy.sparse.spdiags([np.append(M1_dict[n_us][1:,j-1],[0]), M2_dict[n_us][:,j-1], np.append([0],M3_dict[n_us][:-1,j-1])], (-1,0,1), xpoints_dict[n_us]+2, xpoints_dict[n_us]+2).toarray()
                    MC=np.matmul(M,C_dict[n_us][k][:,t_before]) # matrix multiplication for right-hand eqn (M * Cj)
                    MCE= MC+E_dict[n_us][k][:,t_before]    # MC+E which E is (E=r-d) for one time step back
                    Cleft_array=np.linalg.solve (A, MCE) # solve matrix to find Cj+1
                    # change negative C to zero (-C=0)
                    Cleft_array[Cleft_array<0]=0                  
                    
                    Cleft_array[0]=C_dict[n_us][k][0,j]    # Add boundary condition to each step after solving the matrix
                    C_dict[n_us][k][:,j]=Cleft_array
                    t_before=t_before+1
                    del Cleft_array, A, M, MC, MCE
                C_dict[tonode_temp][k][0,:]=C_dict[n_us][k][num_step-1,:]  #Boundary Condition
                C_dict[tonode_temp][k][:,0]=C_dict[n_us][k][0,0]    #Initial Condition 

