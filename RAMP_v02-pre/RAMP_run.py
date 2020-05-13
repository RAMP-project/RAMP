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

from stochastic_process import Stochastic_Process
from stochastic_process_mobility import Stochastic_Process_Mobility
from charging_process import Charging_Process

import post_process as pp
# from post_process import*
import numpy as np
from datetime import datetime
startTime = datetime.now()

'''
Calls the stochastic process and saves the result in a list of stochastic profiles [kW]
In this default example, the model runs for 1 input files ("IT"),
but single or multiple files can be run increasing the list of countries to be run
and naming further input files with corresponding country code
'''
#%% Inputs definition

mobility = True # True or False to select the mobility version of the stochastic process
charging = True # True or False to select to activate the calculation of the charging profiles
af_calculation = True # To choose if availability factors calculation is needed
write_variables = False # Choose to write variables to csv

# Define folder where results are saved: it will be:
# "results/inputfile/simulation_name" leave simulation_name = False (or "")
# to avoid the additional folder
inputfile = 'DE - Validation'
simulation_name = ''

# Define country and year to be considered when generating profiles
country = 'DE'
year = 2015

# Define attributes for the charging profiles
charging_mode = 'Uncontrolled' # Select charging mode ('Until SOC_max', 'Travel Based')
logistic = False # Select the use of a logistic curve to model the probability of charging based on the SOC of the car
SOC_initial = 'random' # Initial SOC at first minute ('random', number between SOC_min (default 0.2) and 1)
infr_prob = 0.5 # Probability of finding the infrastructure when parking ('piecewise', number between 0 and 1)

#inputfile for the external data needed for the different charging profiles: 
inputfile_temp = r"Input_data\temp_ninja_pop.csv"
inputfile_pv = r"Input_data\ninja_pv_europe_v1.1_merra2.csv"
inputfile_wind = r"Input_data\ninja_wind_europe_v1.1_current_national.csv"
inputfile_cap = "Input_data\TIMES_Capacities_technology_2050.csv"
inputfile_load = r"Input_data\time_series_60min_singleindex_filtered.csv"

#%% Call the functions for the simulation

# if mobility == 'False':
#     Profiles_list = Stochastic_Process(j)
if mobility:
    (Profiles_list, Usage_list, User_list, Profiles_user_list, 
    dummy_days) = Stochastic_Process_Mobility(inputfile, country, year)

# Post-processes the results and generates plots
    Profiles_avg, Profiles_list_kW, Profiles_series = pp.Profile_formatting(Profiles_list)
    Usage_avg, Usage_series = pp.Usage_formatting(Usage_list)
    Profiles_user = pp.Profiles_user_formatting(Profiles_user_list)
    
#Create a dataframe with the profile
    Profiles_df = pp.Profile_dataframe(Profiles_series, year) 
    Usage_df = pp.Usage_dataframe(Usage_series, year)

# Time zone correction for profiles and usage
    Profiles_utc = pp.Time_correction(Profiles_df, country, year) 
    Usage_utc = pp.Time_correction(Usage_df, country, year)    

# Add temperature correction to the Power Profiles 
# To be done after the UTC correction because source data for Temperatures have time in UTC
    temp_profile = pp.temp_import(country, year, inputfile_temp) #Import temperature profiles, change the default path to the custom one
    Profiles_temp = pp.Profile_temp(Profiles_utc, year = year, temp_profile = temp_profile)

    Profiles_user_temp = pp.Profile_temp_users(Profiles_user, temp_profile,  year, dummy_days)
    
    del Profiles_user #Removing heavy variable not useful anymore

# Resampling the UTC Profiles
    Profiles_temp_h = pp.Resample(Profiles_temp)

# by default, profiles and usage are plotted as a DataFrame
    pp.Profile_df_plot(Profiles_df, start = '01-01 00:00:00', end = '12-31 23:59:00', year = year, country = country)
    pp.Usage_df_plot(Usage_utc, start = '01-01 00:00:00', end = '12-31 23:59:00', year = year, country = country, User_list = User_list)
    # Profile_series_plot(Profiles_series) #by default, profiles and usage are plotted as a series
    # Usage_series_plot(Usage_series)

#if more than one daily profile is generated, also cloud plots are shown
    if len(Profiles_list) > 1:
        pp.Profile_cloud_plot(Profiles_list, Profiles_avg)

#Exporting all the main quantities
    if write_variables:
        pp.export_csv('Profiles', Profiles_temp, inputfile, simulation_name)
        pp.export_csv('Profiles Hourly', Profiles_temp_h, inputfile, simulation_name)
        pp.export_csv('Usage', Usage_utc, inputfile, simulation_name)
       
#        pp.export_pickle('Profiles_User', Profiles_user_temp, inputfile, simulation_name)
   
    if charging:
        # Ch_profile_user1, Charging_profile1, SOC_user1, plug_in_user1, en_sys_tot1 = Charging_Process(Profiles_user_temp, User_list, country, year, dummy_days, inputfile_load, inputfile_pv, inputfile_wind, inputfile_cap , charging_mode = 'Uncontrolled', logistic = False, infr_prob = 0.5, Ch_stations = ([3.7, 11, 120], [0.6, 0.3, 0.1]))        
        # Ch_profile_user2, Charging_profile2, SOC_user2, plug_in_user2, en_sys_tot2 = Charging_Process(Profiles_user_temp, User_list, country, year, dummy_days, inputfile_load, inputfile_pv, inputfile_wind, inputfile_cap , charging_mode = 'Night Charge', logistic = False, infr_prob = 0.5, Ch_stations = ([3.7, 11, 120], [0.6, 0.3, 0.1]))
        # Ch_profile_user3, Charging_profile3, SOC_user3, plug_in_user3, en_sys_tot3 = Charging_Process(Profiles_user_temp, User_list, country, year, dummy_days, inputfile_load, inputfile_pv, inputfile_wind, inputfile_cap , charging_mode = 'Self-consumption', logistic = False, infr_prob = 0.5, Ch_stations = ([3.7, 11, 120], [0.6, 0.3, 0.1]))
        Ch_profile_user4, Charging_profile4, SOC_user4, plug_in_user4, en_sys_tot4 = Charging_Process(Profiles_user_temp, User_list, country, year, dummy_days, inputfile_load, inputfile_pv, inputfile_wind, inputfile_cap , charging_mode = 'Perfect Foresight', logistic = False, infr_prob = 0.5, Ch_stations = ([3.7, 11, 120], [0.6, 0.3, 0.1]))
        # Ch_profile_user5, Charging_profile5, SOC_user5, plug_in_user5, en_sys_tot5 = Charging_Process(Profiles_user_temp, User_list, country, year, dummy_days, inputfile_load, inputfile_pv, inputfile_wind, inputfile_cap , charging_mode = 'RES Integration', logistic = False, infr_prob = 0.5, Ch_stations = ([3.7, 11, 120], [0.6, 0.3, 0.1]))
        
        ## Charging parameters for the NL Elaad validation
        # Ch_profile_user1, Charging_profile1, SOC_user1, plug_in_user1, en_sys_tot1 = Charging_Process(Profiles_user_temp, User_list, country, year, dummy_days, inputfile_load, inputfile_pv, inputfile_wind, inputfile_cap, charging_mode = 'Uncontrolled', logistic = False, SOC_initial = 'random', infr_prob = 'piecewise', 
        #                   Ch_stations = (list(np.arange(0.5, 12.5, 1)), [0.009, 0.007, 0.022, 0.786, 0.006, 0.005, 0.005, 0.016, 0.042, 0.024, 0.047, 0.04 ]))

        # (Charging_profile_us1, SOC_us1, plug_in_us1) = list(map(
        # Charging_user_formatting, [Ch_profile_user1, SOC_user1, plug_in_user1], [dummy_days, dummy_days, dummy_days]))       
        # (Charging_profile_us2, SOC_us2, plug_in_us2) = list(map(
        # Charging_user_formatting, [Ch_profile_user2, SOC_user1, plug_in_user1], [dummy_days, dummy_days, dummy_days]))
        # (Charging_profile_us3, SOC_us3, plug_in_us3) = list(map(
        # Charging_user_formatting, [Ch_profile_user3, SOC_user3, plug_in_user3], [dummy_days, dummy_days, dummy_days]))

        
        # Charging_profile1_df = pp.Charging_Profile_dataframe(Charging_profile1, year) 
        # Charging_profile2_df = pp.Charging_Profile_dataframe(Charging_profile2, year) 
        # Charging_profile3_df = pp.Charging_Profile_dataframe(Charging_profile3, year) 
        Charging_profile4_df = pp.Charging_Profile_dataframe(Charging_profile4, year) 
        # Charging_profile5_df = pp.Charging_Profile_dataframe(Charging_profile5, year) 
        
        # Postprocess of charging profiles 
        Charging_profiles_utc = pp.Time_correction(Charging_profile4_df, country, year) 

        pp.export_csv('Charging Profiles', Charging_profiles_utc, inputfile, simulation_name)

        pp.Charging_Profile_df_plot(Charging_profiles_utc, color = 'green', start = '01-01 00:00:00', end = '12-31 23:59:00', year = year, country = country)
        
        # Function to calculate the Availability factors, only with the "Perfect Foresight" charging strategy
        if af_calculation: 
            
            AF = pp.Availability_factors(en_sys_tot4, User_list, security_margin = 0.5)
            AF_df = pp.AF_dataframe(AF, year) 
            AF_df_utc = pp.Time_correction(AF_df, country, year) 

            pp.export_csv('Availability Factors', AF_df_utc, inputfile, simulation_name)


        # ax = pp.Charging_Profile_df_plot(AF_df, start = '01-01 00:00:00', end = '12-31 23:59:00', year = year, country = country)
        # ax.set_title('AF - Perfect Foresight charging mode')
        # ax.set_ylabel('')
        
#%% Comparison plots between mobility and charging profiles
        
        # Charging_profile_df = Charging_Profile_dataframe(Charging_profile3, year) 
    
    
        # ax1 = Comparison_plot(Profiles_df, Charging_profile1_df, start = '01-01 00:00:00', end = '12-31 23:59:00', year = year, country = country)
        # ax1.legend(["Moblity Profile", "Uncontrolled"])
        # ax1.set_ylim(0,1000)
        
        # ax2 = Comparison_plot(Profiles_df, Charging_profile2_df, start = '01-01 00:00:00', end = '12-31 23:59:00', year = year, country = country)
        # ax2.legend(["Moblity Profile", "Night Charge"])
        # ax2.set_ylim(0,1000)

print('\nExecution Time:', datetime.now() - startTime)