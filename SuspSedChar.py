# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 13:33:20 2024

@author: haddadchia
"""
# %%
def suspchar (main_dir,sediment_size_file):
    # fine sediment size classes that will be modelled 
    # input: directory to CSV file with sediment classifications
    # output variables: size classes with sediment size and sediment concentration profile (c_alpha)
    import os
    import pandas as pd
    main_dir='C:/Users/haddadchia/OneDrive - NIWA/TEST-River/Calib4-files'
    sediment_size_file='sediment-size-classes_Paper.csv'
    sediment_size=pd.read_csv(os.path.join(main_dir,sediment_size_file), header=0, sep=',')         # sediment size in micrometer
    size_class=sediment_size['class size'].values
    di=sediment_size['size'].values/1000000         # particle size in [m] for each size class
    c_alpha=sediment_size['alpha']                  # alpha parameter for concentration profile
    print (di)
    return size_class, di, c_alpha