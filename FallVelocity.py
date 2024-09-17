# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 20:00:23 2024

@author: haddadchia
"""

#%% calculate fall velocity
def fallvelocity (di):
    # function to calculate fall velocity using
    # input is sediment diameter in meter [m]
    
    Rrho=1.65       # R=((rohs/rho)-1),rhos=2650, rho=1000 - no unit
    nu=0.0000010533 # kinematic viscosity [m^2/s]
    g=9.805         # acceleration gravity [m/s^2]
    
    distar=(((Rrho*g)/(nu**2))**(1/3))*(di)
    falveli= (nu/di)*(((25+(1.2*(distar**2)))**(0.5))-5)**(1.5)     # fall velocity in [m/s]
    print ('fall velocity(s) are:', falveli)
    return falveli