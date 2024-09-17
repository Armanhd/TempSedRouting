# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 20:00:23 2024

@author: haddadchia
"""

#%% calculate fall velocity
def fallvelocity (di):
    # function to calculate fall velocity
    # input is diameter in meter [m]
    distar=(((Rrho*g)/(nu**2))**(1/3))*(di)
    falveli= (nu/di)*(((25+(1.2*(distar**2)))**(0.5))-5)**(1.5)     # fall velocity in [m/s]
    print ('fall velocity(s) are:', falveli)
    return falveli