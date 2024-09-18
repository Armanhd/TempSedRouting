# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 17:02:17 2024

@author: haddadchia
"""

def icbc (fromArrayList, Qinterp_dict,c_alpha,main_dir, sediment_conc_file ):
    # Initial and boundary condition data of the model
    # sediment concentration from upstream reaches
    
    import numpy as np
    C_dict={}
    mnumb=0
    for n in fromArrayList:
        print(n)
        if n!=fromArrayList[-1]:
            Ctemp_dict={}
            for k in range(len(c_alpha)):
                Ctemp_dict[k]=np.zeros_like(Qinterp_dict[n])        
            C_dict[n]=Ctemp_dict
            mnumb=mnumb+1

        else:
            Ctemp_dict={}
            for k in range(len(c_alpha)):
                Ctemp_dict[k]=np.zeros_like(Qinterp_dict[n-1])        
            C_dict[n]=Ctemp_dict
            del Ctemp_dict
            print ('Sink!',n)
    return (C_dict) 