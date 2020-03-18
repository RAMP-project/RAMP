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
from stochastic_process_mobility import Stochastic_Process_Mobility, Charging_Process

from post_process import*

from datetime import datetime
startTime = datetime.now()

# Calls the stochastic process and saves the result in a list of stochastic profiles [kW]
# In this default example, the model runs for 1 input files ("IT"),
# but single or multiple files can be run increasing the list of countries to be run
# and naming further input files with corresponding country code

mobility = 'True' # 'True' or 'False' to select the mobility version of the stochastic process

# Define country and year to be considered when generating profiles
country = 'IT'
year = 2016

write_variables = False

#inputfile for the temperature profile: 
inputfile = r"TimeSeries\temp_ninja_pop.csv"

# if mobility == 'False':
#     Profiles_list = Stochastic_Process(j)
if mobility == 'True':
    Profiles_list, Usage_list, User_list, Profiles_user_list = Stochastic_Process_Mobility(country, year)

# Post-processes the results and generates plots
    Profiles_avg, Profiles_list_kW, Profiles_series = Profile_formatting(Profiles_list)
    Usage_avg, Usage_series = Usage_formatting(Usage_list)
    Profiles_user = Profiles_user_formatting(Profiles_user_list)
    
#Create a dataframe with the profile
    Profiles_df = Profile_dataframe(Profiles_series, year) 
    Usage_df = Usage_dataframe(Usage_series, year)

# Add temperature correction to the Power Profiles
    temp_profile = temp_import(country, year, inputfile = inputfile) #Import temperature profiles, change the default path to the custom one
    Profiles_temp = Profile_temp(Profiles_df, year = year, temp_profile = temp_profile)

# Time zone correction for profiles and usage
    Profiles_utc = Time_correction(Profiles_temp, country, year) 
    Usage_utc = Time_correction(Usage_df, country, year)    

# Resampling the UTC Profiles
    Profiles_utc_h = Resample(Profiles_utc)

# by default, profiles and usage are plotted as a DataFrame
    Profile_df_plot(Profiles_df, start = '01-01 00:00:00', end = '12-31 23:59:00', year = year, country = country)
    Usage_df_plot(Usage_utc, start = '01-01 00:00:00', end = '12-31 23:59:00', year = year, country = country, User_list = User_list)
    # Profile_series_plot(Profiles_series) #by default, profiles and usage are plotted as a series
    # Usage_series_plot(Usage_series)

# The same processing is applied also to the user-detailed profiles
### Commented, as they are just an intermediate step to calculate the charging 
  # profiles, the post processing will be applied on those profiles afterwards
    # Profiles_user_df, Profiles_user_temp, Profiles_user_utc = ({}, {}, {})
    # for us_type in Profiles_user:
    #     Profiles_user_df[us_type] = Profile_dataframe(Profiles_user[us_type], year)
    #     Profiles_user_temp[us_type] = Profile_temp(Profiles_user_df[us_type], year = year, temp_profile = temp_profile)
    #     Profiles_user_utc[us_type] = Time_correction(Profiles_user_temp[us_type], country, year) 

#if more than one daily profile is generated, also cloud plots are shown
    if len(Profiles_list) > 1:
        Profile_cloud_plot(Profiles_list, Profiles_avg)

#Exporting all the main quantities
    if write_variables is True:
        export_csv('Profiles', Profiles_utc, country)
        export_csv('Profiles Hourly', Profiles_utc_h, country)
        export_csv('Usage', Usage_utc, country)
       
        export_pickle('Profiles_User', Profiles_user, country)
    
    Charging_profile_user1, Charging_profile1, SOC_user1 = Charging_Process(Profiles_user, User_list, simple = True)
    Charging_profile_user2, Charging_profile2, SOC_user2 = Charging_Process(Profiles_user, User_list, simple = False)

    Charging_profile1_df = Charging_Profile_dataframe(Charging_profile1, year) 
    Charging_profile2_df = Charging_Profile_dataframe(Charging_profile2, year) 

    ax = Charging_profile1_df.plot(color = 'gold', alpha = 0.5, legend = 'Travel Based Charging')
    ax = Charging_profile2_df.plot(color = 'blue', ax = ax, alpha = 0.5, legend = 'Charging as much as possible')
    ax.legend(["Charging as much as possible", "Travel Based Charging"])
         
    Charging_profile_df = Charging_Profile_dataframe(Charging_profile, year) 

    Charging_Profile_df_plot(Charging_profile_df, start = '01-01 00:00:00', end = '12-31 23:59:00', year = year, country = country)

    ax1 = Comparison_plot(Profiles_df, Charging_profile1_df, start = '01-01 00:00:00', end = '12-31 23:59:00', year = year, country = country)
    ax1.legend(["Moblity Profile", "Charging as much as possible"])
    
    ax2 = Comparison_plot(Profiles_df, Charging_profile2_df, start = '01-01 00:00:00', end = '12-31 23:59:00', year = year, country = country)
    ax2.legend(["Moblity Profile", "Travel Based Charging"])


print('\nExecution Time:', datetime.now() - startTime)

# check = np.zeros((len(Profiles_series), len(Profiles_user)))
# a = {}
# for i, us_type in enumerate(Profiles_user.keys2()):
#     check[:,i] = np.sum(Profiles_user[us_type], axis = 1)
# check = np.sum(check, axis = 1)
# a = np.round(check,0) == np.round(Profiles_series,0)
# if a.all():
#     print('Detailed Profile correctly extracted' )

daily_use_tot = np.random.random(1440)
daily_use_tot1 = np.random.random(1440)

# from timeit import default_timer as timer

# start1 = timer()
# power = daily_use_tot + daily_use_tot1
# end1 = timer()


# start2 = timer()
# power = np.sum([daily_use_tot, daily_use_tot1], axis = 0)
# end2 = timer()

# t1 = end1 - start1
# t2 = end2 - start2
