ReadMe

RiverRouting.py
  Using river characteristics to determine connectivity of river network
  This code use River Environment Classification data (REC) v2.5
(Reference for data: Snelder, T. H., & Biggs, B. J. F. (2002). Multiscale river environment classification for water resources management. JAWRA Journal of the American Water Resources Association, 38(5), 1225-1239. https://doi.org/10.1111/j.1752-1688.2002.tb04344.x)
Input: file and access folder to the CSV file which has: reach ID, reach Nodes information


SuspSedChar.py
  fine sediment size classes that will be modelled 
  input: directory to CSV file with sediment classifications
  output variables: size classes with sediment size and sediment concentration profile (c_alpha)

SedimentCoeff.py
    # Coefficients for solving mass consrvation equation and calculating
    # deposition and re-entrainment rates
    # input: directory to csv file with coeffcients and reach characterstics 
    # from  RiverRouting.py
    # output: river bed sediment size and fine sediment deposition maximum 
    # depth, dispersion coeffcient (constant), F coefficient (constant) and
    # number of interpolation steps (user defined)

ReachChar.py
    # River reach characteristics including river bed gradient and distance 
    # from next reach downstream




Hydrologicalinput.py
    # extracting unitflow, depth and flow for each river reach from hydrological model
  # Input date and time of start and end of flood, reachID, and 
    # directory for hydrological data
    # date and time should be entered in this format, format= 'yyyy-mm-dd HH:MM:SS' 
    # data in a format of Netcdf, compressed CSV, or anytime series format can be used
    # for this study input data were in 1 hour intervals
Time series of hydrological data (i.e. flow, depth and unit flow data) for all river reaches within the study catchment were predicted using the TopNet hydrological model
Reference: Clark, M. P., Rupp, D. E., Woods, R. A., Zheng, X., Ibbitt, R. P., Slater, A. G., et al. (2008). Hydrological data assimilation with the ensemble Kalman filter: Use of streamflow observations to update states in a distributed hydrological model. Advances in Water Resources, 31(10), 1309-1324. https://doi.org/10.1016/j.advwatres.2008.06.005 


InterpolationHydro.py
# Linear interpolation of hydrological data using scipy 


DispersionUstar.py
    # calculating dispersion term in mass conservation using the approach
    #proposed by Fischer et al. (1979)
Reference: Fischer, H. B., List, J. E., Koh, C. R., Imberger, J., & Brooks, N. H. (1979). Mixing in Inland and Coastal Waters (1st Edition ed.). 

CFLTest.py
The Courant-Friedrichs-Lewy (CFL) condition provides a stability criterion for numerical solutions of partial differential equations. In solving the mass conservation equation numerically, a conservative CFL number of 0.1 was used to avoid significant numerical dispersion.

MatrixVars.py
The advection-dispersion equation in a linear system problem using a matrix form.
This code will calculate left and right matrix variables in mass conservation equation. 

ICBCsediment.py

Initial and boundary condition data for running the model
Continuous sediment concentration from upstream reaches during the flood will be used as the input of the model to route sediment downstream

CriticalValues.py
Calculation of critical stream power, critical flow and critical unitflow using logarithmic flow resistance law

Re_entrainment_rate.py
Calculation of the rate of re-entrainment of particles of size d using equation developed by  Haddadchi and Rose (2022).
Reference: Haddadchi, A., & Rose, C. (2024). Calibration and validation data to build an advection-dispersion model for routing suspended sediment down the river network. https://doi.org/10.17632/mxp89v7pfv.1


Scenario_model.py
    # Selecting modelling scenarios based on deposition and re-entrainment rate = 
    # using Haddadchi and Rose (2022)
    

Deposition_rate.py
Calculation of the rate of deposition of particles of size d using equation developed by  Haddadchi and Rose (2022).

Sediment_routing_model.py
Integrating subfunction and routing sediment down a river network using: # one dimensional sediment routing model with the relationship describing conservation of sediment mass subjected to advection and dispersion.

