# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 17:11:34 2024

@author: haddadchia
"""

def critical_strmpow_q_Q (fromArrayList,SF, kv, rho, Rrho, g, Dm_dict, di, mcoef, slope_dict,Qinterp_dict, qinterp_dict ):
    #Calculation of critical stream power, critical flow and critical unitflow 
    # using logarithmic flow resistance law
    
    
    import scipy
    import numpy as np
    interceptregressi_dict={} # intercept of regression 
    sloperegressi_dict={}
    qcr_dict={} # unit critical flow for each reach (n=1,2...), and each fraction (i=1,2,3,4)
    Qcr_dict={} # critical flow for each reach (n=1,2...), each fraction (i=1,2,3,4) and each interpolated flow ([xinterp+2])
    Strmpowcri_dict={} # critical stream power for each reach (n=1,2...), each fraction (i=1,2,3,4) and each interpolated flow ([xinterp+2])
    Strmpow_dict={} # streampower for each reach (n=1,2...), and each interpolated flow ([xinterp+2])
    widthcr_dict={} # width for critical flow for each reach (n=1,2...), each fraction (i=1,2,3,4) and each interpolated flow ([xinterp+2])

    for n in fromArrayList:
        if n!=fromArrayList[-1]:
        # calculate tetarm, taurm, bfunc, tetari for each fraction
            tetarm=0.021+(0.015*np.exp(-20*SF))
            taurm=tetarm*rho*g*Rrho*Dm_dict[n]
            bfunci=0.67/(1+(np.exp(1.5-(di/Dm_dict[n]))))
            tetari=taurm*(((di/Dm_dict[n])**bfunci)/(rho*Rrho*g*di))        
            Logi=np.log10((30*tetari*Rrho*di)/(2.718*mcoef*slope_dict[n]*Dm_dict[n]))
            Wcri=(2.3/kv)*rho*((tetari*Rrho*g*di)**1.5)*Logi #Unit critical streampower [w/m2]
            qcri=Wcri/(rho*g*slope_dict[n])      # critical unit discharge [m^2/s]
                
            Qcr=np.zeros((len(Qinterp_dict[n]),len(qcri)))
            widthcr=np.zeros((len(Qinterp_dict[n]),len(qcri)))
            Strmpowcri=np.zeros((len(Qinterp_dict[n]),len(qcri)))
            sloperegressi=np.zeros(len(Qinterp_dict[n]))    # slope for rows of interpolated flow [xinterp+2]
            interceptregressi=np.zeros(len(Qinterp_dict[n])) # intercept for rows of interpolatedflow [xinterp+2]
            
            #calculate stream power
            Qtemp=np.array(Qinterp_dict[n])
            Strmpow=rho*g*Qtemp*slope_dict[n]
            Strmpow_dict[n]=Strmpow        
            
            for l in range (len(Qinterp_dict[n])):
                # calculate regression 
                sloperegressi[l],interceptregressi[l], r_value, p_value, std_err=scipy.stats.linregress (qinterp_dict[n][l],(Qinterp_dict[n][l]/qinterp_dict[n][l]))
                for k in range(len(qcri)):
                    widthcr[l,k]=sloperegressi[l]*qcri[k] + interceptregressi[l]
                    Qcr[l,k]=widthcr[l,k]*qcri[k]
                    Strmpowcri[l,k]=Wcri[k]*widthcr[l,k]
            
            interceptregressi_dict[n]=interceptregressi        
            sloperegressi_dict[n]=sloperegressi
            
            Strmpowcri_dict[n]=Strmpowcri
            Qcr_dict[n]=Qcr
            qcr_dict[n]=qcri
            widthcr_dict[n]=widthcr
        else:
            print ('Sink!',n)
            
    return Strmpowcri_dict,Qcr_dict, qcr_dict, widthcr_dict, Strmpow_dict, qcri
