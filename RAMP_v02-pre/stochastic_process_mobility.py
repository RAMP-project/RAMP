# -*- coding: utf-8 -*-

#%% Import required libraries
import numpy as np
import numpy.ma as ma
import random 
import math
import pandas as pd
import datetime
from initialise import Initialise_model, Initialise_inputs 

#%% Core model stochastic script

def Stochastic_Process_Mobility(inputfile, country, year):
    
    (peak_enlarg, mu_peak, s_peak, Year_behaviour, User_list, 
     Profile, Usage, Profile_user, num_profiles_user, 
     num_profiles_sim, dummy_days) = Initialise_inputs(inputfile, country, year)
    
    '''
    Calculation of the peak time range, which is used to discriminate between off-peak and on-peak coincident switch-on probability
    Calculates first the overall Peak Window (taking into account all User classes). 
    The peak window is just a time window in which coincident switch-on of multiple appliances assumes a higher probability than off-peak
    Within the peak window, a random peak time is calculated and then enlarged into a peak_time_range following again a random procedure
    '''
    windows_curve = np.zeros(1440) #creates an empty daily profile
    Tot_curve = np.zeros(1440) #creates another empty daily profile
          
    for Us in User_list:
        App_count = 0
        for App in Us.App_list:
            #Calculate windows curve, i.e. the theoretical maximum curve that can be obtained, for each app, by switching-on always all the 'n' apps altogether in any time-step of the functioning windows
            single_wcurve = Us.App_list[App_count].daily_use*np.mean(Us.App_list[App_count].POWER)*Us.App_list[App_count].number #this computes the curve for the specific App
            windows_curve = np.vstack([windows_curve, single_wcurve]) #this stacks the specific App curve in an overall curve comprising all the Apps within a User class
            App_count += 1
        Us.windows_curve = windows_curve #after having iterated for all the Apps within a User class, saves the overall User class theoretical maximum curve
        Us.windows_curve = np.transpose(np.sum(Us.windows_curve, axis = 0))*Us.num_users
        Tot_curve = Tot_curve + Us.windows_curve #adds the User's theoretical max profile to the total theoretical max comprising all classes
    peak_window = np.transpose(np.argwhere(Tot_curve == np.amax(Tot_curve))) #Find the peak window within the theoretical max profile
    peak_time = round(random.normalvariate(round(np.average(peak_window)),1/3*(peak_window[0,-1]-peak_window[0,0]))) #Within the peak_window, randomly calculate the peak_time using a gaussian distribution
    peak_time_range = np.arange((peak_time-round(math.fabs(peak_time-(random.gauss(peak_time,(peak_enlarg*peak_time)))))),(peak_time+round(math.fabs(peak_time-random.gauss(peak_time,(peak_enlarg*peak_time)))))) #the peak_time is randomly enlarged based on the calibration parameter peak_enlarg
    
    '''
    The core stochastic process starts here. For each profile requested by the software user, 
    each Appliance instance within each User instance is separately and stochastically generated
    '''
    for prof_i in range(num_profiles_sim): #the whole code is repeated for each profile that needs to be generated
        Tot_Classes = np.zeros(1440) #initialise an empty daily profile that will be filled with the sum of the hourly profiles of each User instance
        Tot_Usage = np.zeros(1440) #initialise an empty daily usage profile that will be filled with the sum of the hourly usage of each User instance
        Profile_dict = {}
        for Us in User_list: #iterates for each User instance (i.e. for each user class)
            Us.load = np.zeros(1440) #initialise empty load for User instance
            Us.usage = np.zeros(1440) #initialise empty usage profile for User instance
            # Profile_dict[Us.user_name] = np.zeros((1440 * (prof_i + 1),Us.num_users)) #initialise empty user-detailed usage profile for User instance
            # Profile_dict[Us.user_name] = np.zeros((1440,Us.num_users)) #initialise empty user-detailed usage profile for User instance
            # daily_use_tot = np.zeros((1440,Us.num_users))
            Profile_dict[Us.user_name] = []
            for i in range(Us.num_users): #iterates for every single user within a User class. Each single user has its own separate randomisation
                daily_use_tot = np.zeros(1440)
                if Us.user_preference == 0:
                    rand_daily_pref = 0
                    pass
                else:
                    rand_daily_pref = random.randint(1,Us.user_preference)
                for App in Us.App_list: #iterates for all the App types in the given User class
                    #initialises variables for the cycle
                    tot_time = 0
                    App.daily_use = np.zeros(1440)
                    App.usage = np.zeros(1440)
                    if random.uniform(0,1) > App.occasional_use: #evaluates if occasional use happens or not
                        continue
                    else:
                        pass
                    
                    if App.Pref_index == 0:
                        pass
                    else:
                        if rand_daily_pref == App.Pref_index: #evaluates if daily preference coincides with the randomised daily preference number
                            pass
                        else:
                            continue
                    if App.wd_we == Year_behaviour[prof_i] or App.wd_we == 3 : #checks if the app is allowed in the given yearly behaviour pattern
                        pass
                    else:
                        continue

                    #recalculate windows start and ending times randomly, based on the inputs
                    rand_window_1 = np.array([int(random.uniform((App.window_1[0]-App.random_var_1),(App.window_1[0]+App.random_var_1))),int(random.uniform((App.window_1[1]-App.random_var_1),(App.window_1[1]+App.random_var_1)))])
                    if rand_window_1[0] < 0:
                        rand_window_1[0] = 0
                    if rand_window_1[1] > 1440:
                        rand_window_1[1] = 1440
    
                    rand_window_2 = np.array([int(random.uniform((App.window_2[0]-App.random_var_2),(App.window_2[0]+App.random_var_2))),int(random.uniform((App.window_2[1]-App.random_var_2),(App.window_2[1]+App.random_var_2)))])
                    if rand_window_2[0] < 0:
                        rand_window_2[0] = 0
                    if rand_window_2[1] > 1440:
                        rand_window_2[1] = 1440
                            
                    rand_window_3 = np.array([int(random.uniform((App.window_3[0]-App.random_var_3),(App.window_3[0]+App.random_var_3))),int(random.uniform((App.window_3[1]-App.random_var_3),(App.window_3[1]+App.random_var_3)))])
                    if rand_window_3[0] < 0:
                        rand_window_3[0] = 0
                    if rand_window_3[1] > 1440:
                        rand_window_3[1] = 1440
                        
                    #Define all the variables here, with their variability
                    
                    random_var_v = random.uniform((1-App.r_v),(1+App.r_v))
                    random_var_d = random.uniform((1-App.r_d),(1+App.r_d))

                    rand_dist = round(random.uniform(App.dist_tot,int(App.dist_tot*random_var_d))) 
                    
                    App.vel = App.func_dist/App.func_cycle * 60 
                    
                    rand_vel = np.maximum(20, round(random.uniform(App.vel,int(App.vel*random_var_v)))) #average velocity of the trip, minimum value is 20 km/h to get reasonable values from the power curve
                    
                    rand_time = int(round(rand_dist/rand_vel * 60))  #Function to calculate the total time based on total distance and average velocity 
                                                           
                    App.power = (App.Par_power[0] * rand_vel**2 + App.Par_power[1] * rand_vel + App.Par_power[2]) * 12
                    
                    #redefines functioning windows based on the previous randomisation of the boundaries
                    if App.flat == 'yes': #if the app is "flat" the code stops right after filling the newly created windows without applying any further stochasticity
                        App.daily_use[rand_window_1[0]:rand_window_1[1]] = np.full(np.diff(rand_window_1),App.power*App.number)
                        App.daily_use[rand_window_2[0]:rand_window_2[1]] = np.full(np.diff(rand_window_2),App.power*App.number)
                        App.daily_use[rand_window_3[0]:rand_window_3[1]] = np.full(np.diff(rand_window_3),App.power*App.number)
                        Us.load = Us.load + App.daily_use
                        continue
                    else: #otherwise, for "non-flat" apps it puts a mask on the newly defined windows and continues    
                        App.daily_use[rand_window_1[0]:rand_window_1[1]] = np.full(np.diff(rand_window_1),0.001)
                        App.daily_use[rand_window_2[0]:rand_window_2[1]] = np.full(np.diff(rand_window_2),0.001)
                        App.daily_use[rand_window_3[0]:rand_window_3[1]] = np.full(np.diff(rand_window_3),0.001)
                    App.daily_use_masked = np.zeros_like(ma.masked_not_equal(App.daily_use,0.001))
                                  
                    #random variability is applied to the total functioning time and to the duration of the duty cycles, if they have been specified
                    if App.activate == 1:
                        App.p_11 = App.P_11*(random.uniform((1-App.P_var),(1+App.P_var))) #randomly variates the power of thermal apps, otherwise variability is 0
                        App.p_12 = App.P_12*(random.uniform((1-App.P_var),(1+App.P_var))) #randomly variates the power of thermal apps, otherwise variability is 0
                        random_cycle1 = np.concatenate(((np.ones(int(App.t_11*(random.uniform((1+App.r_c1),(1-App.r_c1)))))*App.p_11),(np.ones(int(App.t_12*(random.uniform((1+App.r_c1),(1-App.r_c1)))))*App.p_12))) #randomise also the fixed cycle
                        random_cycle2 = random_cycle1
                        random_cycle3 = random_cycle1
                    elif App.activate == 2:
                        App.p_11 = App.P_11*(random.uniform((1-App.P_var),(1+App.P_var))) #randomly variates the power of thermal apps, otherwise variability is 0
                        App.p_12 = App.P_12*(random.uniform((1-App.P_var),(1+App.P_var))) #randomly variates the power of thermal apps, otherwise variability is 0
                        App.p_21 = App.P_21*(random.uniform((1-App.P_var),(1+App.P_var))) #randomly variates the power of thermal apps, otherwise variability is 0
                        App.p_22 = App.P_22*(random.uniform((1-App.P_var),(1+App.P_var))) #randomly variates the power of thermal apps, otherwise variability is 0
                        random_cycle1 = np.concatenate(((np.ones(int(App.t_11*(random.uniform((1+App.r_c1),(1-App.r_c1)))))*App.p_11),(np.ones(int(App.t_12*(random.uniform((1+App.r_c1),(1-App.r_c1)))))*App.p_12))) #randomise also the fixed cycle
                        random_cycle2 = np.concatenate(((np.ones(int(App.t_21*(random.uniform((1+App.r_c2),(1-App.r_c2)))))*App.p_21),(np.ones(int(App.t_22*(random.uniform((1+App.r_c2),(1-App.r_c2)))))*App.p_22))) #randomise also the fixed cycle
                        random_cycle3 = random_cycle1
                    elif App.activate == 3:
                        App.p_11 = App.P_11*(random.uniform((1-App.P_var),(1+App.P_var))) #randomly variates the power of thermal apps, otherwise variability is 0
                        App.p_12 = App.P_12*(random.uniform((1-App.P_var),(1+App.P_var))) #randomly variates the power of thermal apps, otherwise variability is 0
                        App.p_21 = App.P_12*(random.uniform((1-App.P_var),(1+App.P_var))) #randomly variates the power of thermal apps, otherwise variability is 0
                        App.p_22 = App.P_22*(random.uniform((1-App.P_var),(1+App.P_var))) #randomly variates the power of thermal apps, otherwise variability is 0
                        App.p_31 = App.P_31*(random.uniform((1-App.P_var),(1+App.P_var))) #randomly variates the power of thermal apps, otherwise variability is 0
                        App.p_32 = App.P_32*(random.uniform((1-App.P_var),(1+App.P_var))) #randomly variates the power of thermal apps, otherwise variability is 0
                        random_cycle1 = random.choice([np.concatenate(((np.ones(int(App.t_11*(random.uniform((1+App.r_c1),(1-App.r_c1)))))*App.p_11),(np.ones(int(App.t_12*(random.uniform((1+App.r_c1),(1-App.r_c1)))))*App.p_12))),np.concatenate(((np.ones(int(App.t_12*(random.uniform((1+App.r_c1),(1-App.r_c1)))))*App.p_12),(np.ones(int(App.t_11*(random.uniform((1+App.r_c1),(1-App.r_c1)))))*App.p_11)))]) #randomise also the fixed cycle
                        random_cycle2 = random.choice([np.concatenate(((np.ones(int(App.t_21*(random.uniform((1+App.r_c2),(1-App.r_c2)))))*App.p_21),(np.ones(int(App.t_22*(random.uniform((1+App.r_c2),(1-App.r_c2)))))*App.p_22))),np.concatenate(((np.ones(int(App.t_22*(random.uniform((1+App.r_c2),(1-App.r_c2)))))*App.p_22),(np.ones(int(App.t_21*(random.uniform((1+App.r_c2),(1-App.r_c2)))))*App.p_21)))])                    
                        random_cycle3 = random.choice([np.concatenate(((np.ones(int(App.t_31*(random.uniform((1+App.r_c3),(1-App.r_c3)))))*App.p_31),(np.ones(int(App.t_32*(random.uniform((1+App.r_c3),(1-App.r_c3)))))*App.p_32))),np.concatenate(((np.ones(int(App.t_32*(random.uniform((1+App.r_c3),(1-App.r_c3)))))*App.p_32),(np.ones(int(App.t_31*(random.uniform((1+App.r_c3),(1-App.r_c3)))))*App.p_31)))])#this is to avoid that all cycles are sincronous                      
                    else:
                        pass
                                        
                    #control to check that the total randomised time of use does not exceed the total space available in the windows
                    if rand_time > 0.99*(np.diff(rand_window_1)+np.diff(rand_window_2)+np.diff(rand_window_3)):
                        rand_time = int(0.99*(np.diff(rand_window_1)+np.diff(rand_window_2)+np.diff(rand_window_3)))
                    max_free_spot = rand_time #free spots are used to detect if there's still space for switch_ons. Before calculating actual free spots, the max free spot is set equal to the entire randomised func_time
                           
                    while tot_time <= rand_time: #this is the key cycle, which runs for each App until the switch_ons and their duration equals the randomised total time of use of the App
                            #check how many windows to consider
                            if App.num_windows == 1:
                                switch_on = int(random.choice([random.uniform(rand_window_1[0],(rand_window_1[1]))]))
                            elif App.num_windows == 2:
                                switch_on = int(random.choice([random.uniform(rand_window_1[0],(rand_window_1[1])),random.uniform(rand_window_2[0],(rand_window_2[1]))]))
                            else: 
                                switch_on = int(random.choice([random.uniform(rand_window_1[0],(rand_window_1[1])),random.uniform(rand_window_2[0],(rand_window_2[1])),random.uniform(rand_window_3[0],(rand_window_3[1]))]))
                            #Identifies a random switch on time within the available functioning windows
                            if App.daily_use[switch_on] == 0.001: #control to check if the app is not already on at the randomly selected switch-on time
                                if switch_on in range(rand_window_1[0],rand_window_1[1]):
                                    if np.any(App.daily_use[switch_on:rand_window_1[1]]!=0.001): #control to check if there are any other switch on times after the current one    
                                        next_switch = [switch_on + k[0] for k in np.where(App.daily_use[switch_on:]!=0.001)] #identifies the position of next switch on time and sets it as a limit for the duration of the current switch on
                                        if (next_switch[0] - switch_on) >= App.func_cycle and max_free_spot >= App.func_cycle:
                                            upper_limit = min((next_switch[0]-switch_on),min(rand_time,rand_window_1[1]-switch_on))
                                        elif (next_switch[0] - switch_on) < App.func_cycle and max_free_spot >= App.func_cycle: #if next switch_on event does not allow for a minimum functioning cycle without overlapping, but there are other larger free spots, the cycle tries again from the beginning
                                            continue
                                        else:
                                            upper_limit = next_switch[0]-switch_on #if there are no other options to reach the total time of use, empty spaces are filled without minimum cycle restrictions until reaching the limit                                              
                                    else:
                                        upper_limit = min(rand_time,rand_window_1[1]-switch_on) #if there are no other switch-on events after the current one, the upper duration limit is set this way
                                    
                                    if upper_limit >= App.func_cycle: #if the upper limit is higher than minimum functioning time, an array of indexes is created to be later put in the profile
                                        indexes = np.arange(switch_on,switch_on+(int(random.uniform(App.func_cycle,upper_limit)))) #a random duration is chosen between the upper limit and the minimum cycle
                                    else:
                                        indexes = np.arange(switch_on,switch_on+upper_limit) #this is the case in which empty spaces need to be filled without constraints to reach the total time goal
                                        
                                elif switch_on in range(rand_window_2[0],rand_window_2[1]): #if random switch_on happens in windows2, same code as above is repeated for windows2
                                    if np.any(App.daily_use[switch_on:rand_window_2[1]]!=0.001):
                                        next_switch = [switch_on + k[0] for k in np.where(App.daily_use[switch_on:]!=0.001)]
                                        if (next_switch[0] - switch_on) >= App.func_cycle and max_free_spot >= App.func_cycle:
                                            upper_limit = min((next_switch[0]-switch_on),min(rand_time,rand_window_2[1]-switch_on))
                                        elif (next_switch[0] - switch_on) < App.func_cycle and max_free_spot >= App.func_cycle:
                                            continue
                                        else:
                                            upper_limit = next_switch[0]-switch_on
                                    
                                    else:
                                        upper_limit = min(rand_time,rand_window_2[1]-switch_on)
                                    
                                    if upper_limit >= App.func_cycle:
                                        indexes = np.arange(switch_on,switch_on+(int(random.uniform(App.func_cycle,upper_limit))))
                                    else:    
                                        indexes = np.arange(switch_on,switch_on+upper_limit)
                                        
                                else: #if switch_on is not in window1 nor in window2, it shall be in window3. Same code is repreated
                                    if np.any(App.daily_use[switch_on:rand_window_3[1]]!=0.001):
                                        next_switch = [switch_on + k[0] for k in np.where(App.daily_use[switch_on:]!=0.001)]
                                        if (next_switch[0] - switch_on) >= App.func_cycle and max_free_spot >= App.func_cycle:
                                            upper_limit = min((next_switch[0]-switch_on),min(rand_time,rand_window_3[1]-switch_on))
                                        elif (next_switch[0] - switch_on) < App.func_cycle and max_free_spot >= App.func_cycle:
                                            continue
                                        else:
                                            upper_limit = next_switch[0]-switch_on
                                    
                                    else:
                                        upper_limit = min(rand_time,rand_window_3[1]-switch_on)
                                    
                                    if upper_limit >= App.func_cycle:
                                        indexes = np.arange(switch_on,switch_on+(int(random.uniform(App.func_cycle,upper_limit))))
                                    else:    
                                        indexes = np.arange(switch_on,switch_on+upper_limit)
                                        
                                tot_time = tot_time + indexes.size #the count of total time is updated with the size of the indexes array
                                
                                if tot_time > rand_time: #control to check when the total functioning time is reached. It will be typically overcome, so a correction is applied to avoid this
                                    indexes_adj = indexes[:-(tot_time-rand_time)] #correctes indexes size to avoid overcoming total time
                                    if np.isin(peak_time_range,indexes_adj, assume_unique = True).any() and App.fixed == 'no': #check if indexes are in peak window and if the coincident behaviour is locked by the "fixed" attribute
                                        coincidence = min(App.number,max(1,math.ceil(random.gauss(math.ceil(App.number*mu_peak),(s_peak*App.number*mu_peak))))) #calculates coincident behaviour within the peak time range
                                    elif (not np.isin(peak_time_range,indexes_adj, assume_unique = True).any()) and App.fixed == 'no': #check if indexes are off-peak and if coincident behaviour is locked or not
                                        Prob = random.uniform(0,(App.number-1)/App.number) #calculates probability of coincident switch_ons off-peak
                                        array = np.arange(0,App.number)/App.number
                                        try:
                                            on_number = np.max(np.where(Prob>=array))+1
                                        except ValueError:
                                            on_number = 1 
                                        coincidence = on_number #randomly selects how many apps are on at the same time for each app type based on the above probabilistic algorithm
                                    else:
                                        coincidence = App.number #this is the case when App.fixed is activated. All 'n' apps of an App instance are switched_on altogether
                                    if App.activate > 0: #evaluates if the app has some duty cycles to be considered
                                        if indexes_adj.size > 0:
                                            evaluate = round(np.mean(indexes_adj)) #calculates the mean time position of the current switch_on event, to later select the proper duty cycle
                                        else:
                                            evaluate = 0 
                                        #based on the evaluate value, selects the proper duty cycle and puts the corresponding power values in the indexes range
                                        if evaluate in range(App.cw11[0],App.cw11[1]) or evaluate in range(App.cw12[0],App.cw12[1]):
                                            np.put(App.daily_use,indexes_adj,(random_cycle1*coincidence))
                                            np.put(App.daily_use_masked,indexes_adj,(random_cycle1*coincidence),mode='clip')
                                        elif evaluate in range(App.cw21[0],App.cw21[1]) or evaluate in range(App.cw22[0],App.cw22[1]):
                                            np.put(App.daily_use,indexes_adj,(random_cycle2*coincidence))
                                            np.put(App.daily_use_masked,indexes_adj,(random_cycle2*coincidence),mode='clip')
                                        else:
                                            np.put(App.daily_use,indexes_adj,(random_cycle3*coincidence))
                                            np.put(App.daily_use_masked,indexes_adj,(random_cycle3*coincidence),mode='clip')
                                    else: #if no duty cycles are specififed, a regular switch_on event is modelled
                                        np.put(App.daily_use,indexes_adj,(App.power*(random.uniform((1-App.P_var),(1+App.P_var)))*coincidence)) #randomises also the App Power if P_var is on
                                        np.put(App.daily_use_masked,indexes_adj,(App.power*(random.uniform((1-App.P_var),(1+App.P_var)))*coincidence),mode='clip')
                                    App.daily_use_masked = np.zeros_like(ma.masked_greater_equal(App.daily_use_masked,0.001)) #updates the mask excluding the current switch_on event to identify the free_spots for the next iteration
                                    tot_time = (tot_time - indexes.size) + indexes_adj.size #updates the total time correcting the previous value
                                    break #exit cycle and go to next App
                                else: #if the tot_time has not yet exceeded the App total functioning time, the cycle does the same without applying corrections to indexes size
                                    if (np.isin(peak_time_range,indexes, assume_unique = True).any()) and App.fixed == 'no':
                                        coincidence = min(App.number,max(1,math.ceil(random.gauss(math.ceil(App.number*mu_peak),(s_peak*App.number*mu_peak)))))
                                    elif not np.isin(peak_time_range,indexes, assume_unique = True).any() and App.fixed == 'no':
                                        Prob = random.uniform(0,(App.number-1)/App.number)
                                        array = np.arange(0,App.number)/App.number
                                        try:
                                            on_number = np.max(np.where(Prob>=array))+1
                                        except ValueError:
                                            on_number = 1
                                        coincidence = on_number
                                    else:
                                        coincidence = App.number
                                    if App.activate > 0:
                                        if indexes.size > 0:
                                            evaluate = round(np.mean(indexes))
                                        else:
                                            evaluate = 0
                                        if evaluate in range(App.cw11[0],App.cw11[1]) or evaluate in range(App.cw12[0],App.cw12[1]):
                                            np.put(App.daily_use,indexes,(random_cycle1*coincidence))
                                            np.put(App.daily_use_masked,indexes,(random_cycle1*coincidence),mode='clip')
                                        elif evaluate in range(App.cw21[0],App.cw21[1]) or evaluate in range(App.cw22[0],App.cw22[1]):
                                            np.put(App.daily_use,indexes,(random_cycle2*coincidence))
                                            np.put(App.daily_use_masked,indexes,(random_cycle2*coincidence),mode='clip')
                                        else:
                                            np.put(App.daily_use,indexes,(random_cycle3*coincidence))
                                            np.put(App.daily_use_masked,indexes,(random_cycle3*coincidence),mode='clip')
                                    else:
                                        np.put(App.daily_use,indexes,(App.power*(random.uniform((1-App.P_var),(1+App.P_var)))*coincidence))
                                        np.put(App.daily_use_masked,indexes,(App.power*(random.uniform((1-App.P_var),(1+App.P_var)))*coincidence),mode='clip')
                                    App.daily_use_masked = np.zeros_like(ma.masked_greater_equal(App.daily_use_masked,0.001))
                                    tot_time = tot_time #no correction applied to previously calculated value
                                                    
                                free_spots = [] #calculate how many free spots remain for further switch_ons
                                try:
                                    for j in ma.notmasked_contiguous(App.daily_use_masked):
                                        free_spots.append(j.stop-j.start)
                                except TypeError:
                                    free_spots = [0]
                                max_free_spot = max(free_spots) 
    
                            else:
                                continue #if the random switch_on falls somewhere where the App has been already turned on, tries again from beginning of the while cycle
                    App.usage = App.daily_use   #Save the daily use to calculate the usage profile, i.e. without considering the power of the appliance. 
                    App.usage = np.where(App.usage > 1, 10, App.usage)
                    Us.load = Us.load + App.daily_use #adds the App profile to the User load
                    Us.usage = Us.usage + App.usage #adds the App usage to the User usage profile
                    daily_use_tot = daily_use_tot + App.daily_use
                Profile_dict[Us.user_name].append(daily_use_tot)
            Tot_Classes = Tot_Classes + Us.load #adds the User load to the total load of all User classes
            Tot_Usage = Tot_Usage + Us.usage
        Profile_user.append(Profile_dict)
        if (dummy_days - 1) < prof_i < (num_profiles_sim - dummy_days): # Do not append dummy days
            Profile.append(Tot_Classes) #appends the total load to the list that will contain all the generated profiles
            Usage.append(Tot_Usage)#appends the total usage to the list that will contain all the generated profiles
        
            print(f'Profile {prof_i - dummy_days +1}/{num_profiles_user} completed') #screen update about progress of computation
    
    return(Profile, Usage, User_list, Profile_user, dummy_days)