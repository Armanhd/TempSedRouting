# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 12:51:28 2024

@author: haddadchia
"""

#%%
def riverrouting (main_dir_routing, routing_file):
    # using river charctersitics to use for connectivity of river network
    # this code use River Environment Classificatio (REC) v2.5 
    # input: file and access folder to the CSV file which hasreach ID, 
    # reach Node info
    import pandas as pd
    import numpy as np
    import os
    hydroDF=pd.read_csv(os.path.join(main_dir_routing,routing_file)
                        ).sort_values(by = ["HYDSEQ"]) # read routing file          
    US_reach=hydroDF["nzsegv2"].values 
    hydroDF = hydroDF.set_index("nzsegv2") # US_reach is now index in dataframe
    fromArray = hydroDF["FROM_NODE"].values      
    toArray = hydroDF["TO_NODE"].values
    nodeArray = np.append(toArray, fromArray) #join arrays to make single array with all nodes
    uniqueNodeArray = np.unique(nodeArray) #remove duplicates since nodes are found in both arrays
    uniqueNodeList =uniqueNodeArray.tolist() #make list of keys 
    entryArray = np.zeros(len(uniqueNodeList)).astype(float) #make array of initial entries, i.e, zero
    fromArrayList=fromArray.tolist()    # list for fromArray (which is FROM_NODE)
    uniquetoArray=np.unique(toArray)
    toArrayList=uniquetoArray.tolist()
    return hydroDF, US_reach, fromArrayList, toArray, toArrayList,uniqueNodeList