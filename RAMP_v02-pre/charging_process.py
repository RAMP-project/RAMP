# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 12:03:48 2020

@author: Andrea Mangipinto
"""

#%% Import required libraries
import numpy as np
import random 
import pandas as pd
import datetime as dt
import initialise
# from initialise import (charge_prob, charge_prob_const, SOC_initial_f, 
# SOC_initial_f_const, charge_check_smart, charge_check_normal, pv_indexing, 
# tot_users_calc)

#%% Charging process calculation script

def Charging_Process(Profiles_user, User_list, country, year, dummy_days, inputfile_load, inputfile_pv, inputfile_wind, inputfile_cap, charging_mode = 'Uncontrolled', logistic = False, infr_prob = 0.5, Ch_stations = ([3.7, 11, 120], [0.6, 0.3, 0.1])):
    
    #SOC value at the beginning of the simulation, relevant only for
    # Perfect Foresight charging strategy, as is the maximum SOC that the car 
    # will always try to go back to
    SOC_initial = 0.8
    SOC_min_rand = 0.5 # Minimum SOC level with which the car can start the simulation

    # Definition of battery limits to avoid degradation
    SOC_max = 0.8 # Maximum SOC at which the battery is charged
    SOC_min = 0.25 # Minimum SOC level that forces the charging event
    
    eff = 0.90  # Charging/discharging efficiency
    
    P_ch_station_list = Ch_stations[0] # Nominal power of the charging station [kW]
    prob_ch_station = Ch_stations[1]    
    
    # Parameters for the piecewise infrastructure probability function
    prob_max = 0.9
    prob_min = 0.4
    t1 = '06:00'
    t2 = '19:00'
    
    # Calculate the number of users in simulation for screen update
    tot_users = initialise.tot_users_calc(User_list)
      
    # Load multiplier for the residual load calculation
    load_multiplier = 2.5
    
    # Check that the charging mode is one of the expected ones
    charging_mode_types = ['Uncontrolled', 'Night Charge', 'Self-consumption', 'RES Integration', 'Perfect Foresight']
    assert charging_mode in charging_mode_types, f"[WARNING] Invalid Charging Mode. Expected one of: {charging_mode_types}"
    
    # Check that the initial SOC is in the expected way
    if (SOC_initial != 'random' and 
        not isinstance(SOC_initial, (int, float))): 
            raise ValueError(f"[WARNING] Invalid SOC initial. Expected etiher 'random', or a value between {SOC_min} and 1")                    

    # Check that the infrastructure probability is in the expected way
    if (infr_prob != 'piecewise' and 
        not isinstance(infr_prob, (int, float))): 
            raise ValueError("[WARNING] Invalid Infrastructure probability. Expected etiher 'piecewise', or a value between 0 and 1")                        
    
    # Initialization of output variables
    Charging_profile_user = {}
    Charging_profile = np.zeros(len(Profiles_user['Working - Large car']))
    en_sys_tot = np.zeros(len(Profiles_user['Working - Large car']))
    SOC_user = {}
    plug_in_user = {}
    num_us = 0
    
    # Creation of date array 
    start_day = dt.datetime(year, 1, 1) - dt.timedelta(days=dummy_days)
    n_periods = len(Profiles_user['Working - Large car'])
    minutes = pd.date_range(start=start_day, periods = n_periods, freq='T')

    # Check if introducing the logistic function for behavioural modeling
    if logistic: # Probability of charging based on the SOC of the car 
        ch_prob = initialise.charge_prob
    else: # The user will always try to charge (probability = 1 for every SOC)
        ch_prob = initialise.charge_prob_const
    
    # Check which infrastructure probability function to use 
    if infr_prob == 'piecewise': # Use of piecewise function based on hour of the day 
        # Windows for piecewise infrastructure probability
        window_1 = minutes.indexer_between_time('0:00', t1, include_start=True, include_end=False)
        window_2 = minutes.indexer_between_time(t1, t2, include_start=True, include_end=False)
        window_3 = minutes.indexer_between_time(t2, '0:00', include_start=True, include_end=True)
        infr_pr = np.zeros(len(minutes))
        infr_pr[window_1] = prob_max
        infr_pr[window_2] = prob_min
        infr_pr[window_3] = prob_max
    elif isinstance(infr_prob, (int, float)): # Constant probability of finding infrastructure
        infr_pr = np.ones(len(minutes)) * infr_prob
        window_1 = 0
        window_2 = 0
        window_3 = 0

    # Definition of range in which the charging is shifted
    if charging_mode == 'Night Charge':
        charge_range = minutes.indexer_between_time('22:00', '7:00', include_start=True, include_end=False)
        charge_range_check = initialise.charge_check_smart
    elif charging_mode == 'Self-consumption':
        charge_range = initialise.pv_indexing(minutes, country, year, inputfile_pv = r"Input_data\ninja_pv_europe_v1.1_merra2.csv")
        charge_range_check = initialise.charge_check_smart
    elif charging_mode == "RES Integration":
        charge_range = initialise.residual_load(minutes, country, load_multiplier, inputfile_load, inputfile_pv, inputfile_wind, inputfile_cap)
        charge_range_check = initialise.charge_check_smart
    else: 
        charge_range = 0
        charge_range_check = initialise.charge_check_normal

    print('\nPlease wait for the charging profiles...')   
    
    for us_num, Us in enumerate(User_list): # Simulates for each user type
        
        #Initialise lists
        Charging_profile_user[Us.user_name] = []
        SOC_user[Us.user_name] = []
        plug_in_user[Us.user_name] = []
        
        plug_in_Us = np.zeros((len(Profiles_user[Us.user_name]), Us.num_users), dtype = int) # Initialise plug-in array

        # Brings tha values put to 0.001 for the mask to 0
        Profiles_user[Us.user_name] = np.where(Profiles_user[Us.user_name] < 0.1, 0, Profiles_user[Us.user_name]) 
        # Sets to power consumed by the car to negative values
        power_Us = np.where(Profiles_user[Us.user_name] > 0, -Profiles_user[Us.user_name], 0) 
        power_Us = power_Us / 1000 #kW
        
        # Users who never take the car in the considered period are skipped
        power_Us = power_Us[:,np.where(power_Us.any(axis=0))[0]] 
        
        Battery_cap_Us_min = Us.App_list[0].Battery_cap * 60 # Capacity multiplied by 60 to evaluate the capacity in kWmin
        
        for i in range(power_Us.shape[1]): # Simulates for each single user with at least one travel
            
            # Filter power for the specific user            
            plug_in = plug_in_Us[:,i]
            power = power_Us[:, i] 
            
            # Variation of SOC for each minute, 
            delta_soc = power / Battery_cap_Us_min 
            
            #Control rountine on the Initial SOC value
            if SOC_initial == 'random': #function to select random value
                SOC_init = initialise.SOC_initial_f(SOC_max, SOC_min_rand, SOC_initial)           
            elif isinstance(SOC_initial, (int, float)): # If initial SOC is a number, that will be the initial SOC
                SOC_init = initialise.SOC_initial_f_const(SOC_max, SOC_min_rand, SOC_initial)    
            
            # Calculation of the SOC array
            SOC = delta_soc
            SOC[0] = SOC_init
            SOC = np.cumsum(SOC)
            
            # Calculation of the indexes of each parking start and end 
            park_ind = np.where(power == 0)[0]
            park_ind = np.split(park_ind, np.where(np.diff(park_ind) != 1)[0]+1)
            park_ind = [[ind[0],ind[-1]+1] for ind in park_ind] #list of array of index of when there is a mobility travel
            
            en_to_charge = 0  # Initialise value for perfect foresight chaging mode          
            
            # Iterates over all parkings (park = 0 corresponds to the period where no travel was made yet, so is not evaluated)
            for park in range(0, len(park_ind)): 
                
                # The iteration for park = 0 is needed only for Perfect Foresight strategy. For the other cases the first loop is skipped.
                if charging_mode != 'Perfect Foresight' and park == 0:
                    continue
                else:
                    pass
                
                # SOC at the beginning of the parking
                SOC_park = SOC[park_ind[park][0]]
                
                
                # For the time based charging methods, the index of the parking period is calculated.
                # In the other cases is set to a dummy variable to avoid interection with "dummy" charge range
                if charging_mode in ['Night Charge', 'Self-consumption', 'RES Integration']:
                    # Index range of when the car is parked                
                    ind_park_range = np.arange(park_ind[park][0], park_ind[park][1])                    
                else:
                    ind_park_range = 1
                
                try:  # Energy used in the following travel
                    next_travel_ind_range = np.arange(park_ind[park][1], park_ind[park+1][0])
                    len_next_park =  park_ind[park+1][1] - park_ind[park+1][0]
                    if len_next_park < 10:
                        next_travel_ind_range = np.arange(park_ind[park][1], park_ind[park+2][0])
                    en_next_travel = abs(np.sum(power[next_travel_ind_range]))                 
                except IndexError: # If there is an index error means we are in the last parking, special case
                    en_next_travel = 0

                if charging_mode != 'Perfect Foresight':  # If not perfect foresight set energy charge tot=0, will be calculated only if parking
                    en_charge_tot = 0
                else: # Calculating the energy consumed in the following travel   
                    en_charge_tot = (en_next_travel + en_to_charge)/eff
                
                residual_energy = Battery_cap_Us_min*SOC_park  # Residual energy in the EV Battery

                # Control to check if the user can charge based on infrastructure 
                # availability, SOC, time of the day (Depending on the options activated)
                if (
                    (ch_prob(SOC_park) > np.random.rand() and
                    infr_pr[park_ind[park][0]] > np.random.rand() and
                    charge_range_check(ind_park_range, charge_range)
                    ) or 
                    (np.around(SOC_park, 2) <= SOC_min) or
                    (np.floor(residual_energy) <= np.ceil(en_next_travel/eff))
                    ): 
                                        
                    # Calculates the parking time
                    t_park = park_ind[park][1] - park_ind[park][0]                 
                    
                    # Fills the array of plug in (1 = plugged, 0 = not plugged)
                    plug_in[park_ind[park][0]:park_ind[park][1]] = 1
                    
                    # Samples the nominal power of the charging station
                    P_ch_nom = random.choices(P_ch_station_list, weights=prob_ch_station)[0]                
                                        
                    # In the case of perfect foresight the charging is shifted at the end of the parking, so a special routine is needed
                    if charging_mode == 'Perfect Foresight': 
                        P_charge = P_ch_nom # Charge at nominal power
                        t_ch_tot = int(round(en_charge_tot/P_ch_nom)) 
                        t_ch = min(t_ch_tot, t_park) # charge until SOC max, if parking time allows                   
                        charge_end = park_ind[park][1]
                        charge_start = charge_end - t_ch
                        power[charge_start: charge_end] = P_charge
                        en_to_charge = en_charge_tot - (t_ch * P_charge)
                    else: # In the other charging modes a common routine is defined
                        en_charge_tot = Battery_cap_Us_min*(SOC_max - SOC_park)/eff
                        with np.errstate(divide='raise'):
                            try: # Charging strategy for time based modes (Night charge, RES integration, Self-consumption)
                                charge_ind_range = np.intersect1d(ind_park_range, charge_range)
                                # Minimum charging power (charging during night time)
                                P_ch_min = min(en_charge_tot/len(charge_ind_range), P_ch_nom)
                                P_charge = P_ch_min
                                t_ch = len(charge_ind_range)
                                charge_start = charge_ind_range[0]
                                charge_end = charge_ind_range[-1] + 1
                                np.put(power, charge_ind_range, P_charge)
                            # if intersection array is empty means that we are in forced charging 
                            # (SOC<0.2 / too low SOC residual), or in uncontrolled charging mode
                            except (FloatingPointError, ZeroDivisionError): 
                                # Total charging time at P nominal 
                                t_ch_tot = int(round(en_charge_tot/P_ch_nom)) 
                                t_ch = min(t_ch_tot, t_park) # charge until SOC max, if parking time allows                   
                                # charge_ind_range = np.arange(park_ind[park][0], park_ind[park][0] + t_ch)
                                charge_start = park_ind[park][0]
                                charge_end = charge_start + t_ch
                                P_charge = P_ch_nom # Charge at nominal power
                                power[charge_start: charge_end] = P_charge
                                                
                    delta_soc = power / Battery_cap_Us_min 
                    SOC = delta_soc
                    SOC[0] = SOC_init
                    SOC = np.cumsum(SOC)
                
                else: # if the user does not charge, then the energy consumed will be charged in a following parking                         
                    en_to_charge = en_charge_tot                        
            
            charging_power = np.where(power<0, 0, power) # Filtering only for the charging power 
            
            # SOC_user[Us.user_name].append(SOC)
            # Charging_profile_user[Us.user_name].append(power_pos)
            # plug_in_user[Us.user_name].append(plug_in)
            
            Charging_profile = Charging_profile + charging_power
            SOC_user[Us.user_name].append(SOC)
            Charging_profile_user[Us.user_name].append(charging_power)
            plug_in_user[Us.user_name].append(plug_in)

            if charging_mode == 'Perfect Foresight':
                en_system = (Battery_cap_Us_min - charging_power) * plug_in
                en_sys_tot = en_sys_tot + en_system

            if all(SOC > 0): #Check that the car never has SOC < 0
                continue
            else: 
                SOC_user[Us.user_name].append(SOC)
                Charging_profile_user[Us.user_name].append(charging_power)
                plug_in_user[Us.user_name].append(plug_in)

                neg_soc_ind = np.where(SOC < 0)[0]
                neg_soc_ind = np.split(neg_soc_ind, np.where(np.diff(neg_soc_ind) != 1)[0]+1)
                neg_soc_ind = [[ind[0],ind[-1]+1] for ind in neg_soc_ind] #list of array of index of when there is a mobility travel
                print(f"[WARNING: Charging process User {i + 1} ({Us.user_name}) not properly constructed, SOC < 0 in time {neg_soc_ind}]") 
                # SOC_user[Us.user_name].append(SOC)
                # Charging_profile_user[Us.user_name].append(power_pos)
                # plug_in_user[Us.user_name].append(plug_in)

        num_us = num_us + Us.num_users
        print(f'Charging Profile of "{Us.user_name}" user completed ({num_us}/{tot_users})') #screen update about progress of computation
    
    dummy_minutes = 1440 * dummy_days
    Charging_profile = Charging_profile[dummy_minutes:-dummy_minutes]
    en_sys_tot = en_sys_tot[dummy_minutes:-dummy_minutes]

    
    return (Charging_profile_user, Charging_profile, SOC_user, plug_in_user, en_sys_tot)

