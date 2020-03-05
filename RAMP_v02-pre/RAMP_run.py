# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 14:35:00 2019
This is the code for the open-source stochastic model for the generation of 
multi-energy load profiles in off-grid areas, called RAMP, v.0.2.1-pre.

@authors:
- Francesco Lombardi, Politecnico di Milano
- Sergio Balderrama, Université de Liège
- Sylvain Quoilin, KU Leuven
- Emanuela Colombo, Politecnico di Milano

Copyright 2019 RAMP, contributors listed above.
Licensed under the European Union Public Licence (EUPL), Version 1.1;
you may not use this file except in compliance with the License.

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations
under the License.
"""

#%% Import required modules

import pandas as pd
from stochastic_process import Stochastic_Process
from stochastic_process_mobility import Stochastic_Process_Mobility

from post_process import*

from datetime import datetime
startTime = datetime.now()

#do something

# Calls the stochastic process and saves the result in a list of stochastic profiles
# In this default example, the model runs for 2 input files ("input_file_1", "input_file_2"),
# but single or multiple files can be run restricting or enlarging the iteration range 
# and naming further input files with progressive numbering

mobility = 'True' # 'True' or 'False' to select the mobility version of the stochastic process

# Define country and year to be considered when generating profiles
country = 'IT'
#NOTE: for the time being only 2016 can be 
# simulated with temperature correction
year = 2016

#inputfile for the temperature profile: 
inputfile = r"TimeSeries\temp_ninja_pop.csv"

# if mobility == 'False':
#     Profiles_list = Stochastic_Process(j)
if mobility == 'True':
    Profiles_list, Usage_list = Stochastic_Process_Mobility(country, year)

# Post-processes the results and generates plots
    Profiles_avg, Profiles_list_kW, Profiles_series = Profile_formatting(Profiles_list)
    Usage_avg, Usage_series = Usage_formatting(Usage_list)
    
    Profile_series_plot(Profiles_series) #by default, profiles are plotted as a series
    Profile_usage_plot(Usage_series)
    
    Profiles_df = Profile_dataframe(Profiles_series, year) #Create a dataframe with the profile
    Usage_df = Usage_dataframe(Usage_series, year)
    
    export_series('Profiles', Profiles_df, country)
    export_series('Usage', Usage_df, country)

    temp_profile = temp_import(country, year, inputfile = inputfile) #Import temperature profiles, change the default path to the custom one
    
    Profiles_temp = Profile_temp(Profiles_df, year = year, temp_profile = temp_profile)

    Profiles_utc = Time_correction(Profiles_temp, country) 
    
    if len(Profiles_list) > 1: #if more than one daily profile is generated, also cloud plots are shown
        Profile_cloud_plot(Profiles_list, Profiles_avg)
        
# Profiles_df['2014-01-04':'2014-01-10'].plot()

print('\nExecution Time:', datetime.now() - startTime)
