# -*- coding: utf-8 -*-

#%% Import required libraries
import numpy as np
import numpy.ma as ma
import random 
import math
import pandas as pd
from initialise import Initialise_model, Initialise_inputs, charge_prob, charge_prob_const, infrastructure_prob, infrastructure_prob_const, SOC_initial_f, SOC_initial_f_const

#%% Core model stochastic script

def Stochastic_Process_Mobility(country, year):
    
    (peak_enlarg, mu_peak, s_peak, Year_behaviour, User_list, 
     Profile, Usage, Profile_user, num_profiles_user, 
     num_profiles_sim, dummy_days) = Initialise_inputs(country, year)
    
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
                                    if np.in1d(peak_time_range,indexes_adj).any() and App.fixed == 'no': #check if indexes are in peak window and if the coincident behaviour is locked by the "fixed" attribute
                                        coincidence = min(App.number,max(1,math.ceil(random.gauss(math.ceil(App.number*mu_peak),(s_peak*App.number*mu_peak))))) #calculates coincident behaviour within the peak time range
                                    elif np.in1d(peak_time_range,indexes_adj).any()== False and App.fixed == 'no': #check if indexes are off-peak and if coincident behaviour is locked or not
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
                                    if np.in1d(peak_time_range,indexes).any() and App.fixed == 'no':
                                        coincidence = min(App.number,max(1,math.ceil(random.gauss(math.ceil(App.number*mu_peak),(s_peak*App.number*mu_peak)))))
                                    elif np.in1d(peak_time_range,indexes).any() == False and App.fixed == 'no':
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
        if (dummy_days - 1) < prof_i < (num_profiles_sim - 7): # Do not append dummy days
            Profile.append(Tot_Classes) #appends the total load to the list that will contain all the generated profiles
            Usage.append(Tot_Usage)#appends the total usage to the list that will contain all the generated profiles
            Profile_user.append(Profile_dict)
        
        if (dummy_days - 1) < prof_i < (num_profiles_sim - 7):
            print(f'Profile {prof_i - dummy_days +1}/{num_profiles_user} completed') #screen update about progress of computation
    
    return(Profile, Usage, User_list, Profile_user)

    
def Charging_Process(Profiles_user, User_list, year, charging_mode = 'Uncontrolled', logistic = False, SOC_initial = 'random', infr_prob = 0.5):
    
    # Definition of battery limits to avoid degradation
    SOC_max = 0.8 # Maximum SOC at which the battery is charged
    SOC_min_rand = 0.5 # Minimum SOC level with which the car can start the simulation
    SOC_min = 0.2 # Minimum SOC level that forces the charging event
    
    # Calculate the number of users in simulation for screen update
    num = {}
    for i in range(len(User_list)):
        num[User_list[i].user_name] = User_list[i].num_users
        tot_users = sum(num.values())    
    
    # Check that the charging mode is one of the expected ones
    charging_mode_types = ['Travel Based', 'Uncontrolled', 'Night Charge']
    if charging_mode not in charging_mode_types:
        raise ValueError(f"[WARNING] Invalid Charging Mode. Expected one of: {charging_mode_types}")                    
    
    # Check that the initial SOC is in the expected way
    if (SOC_initial != 'random' and 
        not isinstance(SOC_initial, (int, float))): 
            raise ValueError(f"[WARNING] Invalid SOC initial. Expected etiher 'random', or a value between {SOC_min} and 1")                    

    # Check that the infrastructure probability is in the expected way
    if (infr_prob != 'piecewise' and 
        not isinstance(infr_prob, (int, float))): 
            raise ValueError("[WARNING] Invalid Infrastructure probability. Expected etiher 'piecewise', or a value between 0 and 1")                        
    
    eff = 0.95  # Charging/discharging efficiency
    
    P_ch_station_list = [3.7, 11, 120] # Nominal power of the charging station [kW]
    prob_ch_station = [0.6, 0.3, 0.1]
    
    # Initialization of output variables
    Charging_profile_user = {}
    Charging_profile = np.zeros(len(Profiles_user['Working - Large car']))
    SOC_user = {}
    plug_in_user = {}
    num_us = 0
    
    # Creation of date array 
    minutes = pd.date_range(start=str(year) + '-01-01', periods = len(Profiles_user['Working - Large car']), freq='T')
    
    # Check if introducing the logistic function for behavioural modeling
    if logistic is True: # Probability of charging based on the SOC of the car 
        ch_prob = charge_prob
    else: # The user will always try to charge (probability = 1 for every SOC)
        ch_prob = charge_prob_const
    
    # Check which infrastructure probability function to use 
    if infr_prob == 'piecewise': # Use of piecewise function based on hour of the day 
        infr_p = infrastructure_prob 
    elif isinstance(infr_prob, (int, float)): # Constant probability of finding infrastructure
        infr_p = infrastructure_prob_const

    # Definition of range in which the charging is shifted
    if charging_mode == 'Night Charge':
        charge_range = minutes.indexer_between_time('22:00', '7:00', include_start=True, include_end=False)
    else: 
        charge_range = np.arange(0, len(minutes))

    # if SOC_initial == 'random': #Control rountine on the Initial SOC value
    #     SOC_i = SOC_initial_f              #function to select random value
    # elif isinstance(SOC_initial, (int, float)): 
    #     SOC_i = SOC_initial_f_const        #function to select constant value as the one indiated by the user

    print('\nPlease wait for the charging profiles...')   
    
    for us_num, Us in enumerate(User_list): # Simulates for each user type
        
        #Initialise lists
        Charging_profile_user[Us.user_name] = []
        SOC_user[Us.user_name] = []
        plug_in_user[Us.user_name] = []
        
        # Brings tha values put to 0.001 for the mask to 0
        Profiles_user[Us.user_name] = np.where(Profiles_user[Us.user_name] < 0.1, 0, Profiles_user[Us.user_name]) 
        #Sets to power consumed by the car to negative values
        power_Us = np.where(Profiles_user[Us.user_name] > 0, -Profiles_user[Us.user_name], 0) 
        power_Us = power_Us / 1000 #kW
        
        # Users who never take the car in the considered period are skipped
        power_Us = power_Us[:,np.where(power_Us.any(axis=0))[0]] 
        
        for i in range(power_Us.shape[1]): # Simulates for each single user with at least one travel
                        
            plug_in = np.zeros(len(Profiles_user[Us.user_name])) # Initialise plug-in array
            
            power = power_Us[:, i] # Filter power for the specific user
            
            # Variation of SOC for each minute, capacity multiplied by 60 to evaluate the capacity in kW - min
            delta_soc = power / (Us.App_list[0].Battery_cap * 60) 
            
            #Control rountine on the Initial SOC value
            if SOC_initial == 'random': #function to select random value
                SOC_init = SOC_initial_f(SOC_max, SOC_min_rand, SOC_initial)           
            elif isinstance(SOC_initial, (int, float)): # If initial SOC is a number, that will be the initial SOC
                SOC_init = SOC_initial_f_const(SOC_max, SOC_min_rand, SOC_initial)    
            
            # Calculation of the SOC array
            SOC = delta_soc
            SOC[0] = SOC_init
            SOC = np.cumsum(SOC)
            
            # travel_ind = np.where(power < 0)[0] 
            # travel_ind = np.split(travel_ind, np.where(np.diff(travel_ind) != 1)[0]+1)
            # travel_ind = [np.array([ind[0],ind[-1]]) for ind in travel_ind] #list of array of index of when there is a mobility travel
            
            # Calculation of the indexes of each parking start and end 
            park_ind = np.where(power == 0)[0]
            park_ind = np.split(park_ind, np.where(np.diff(park_ind) != 1)[0]+1)
            park_ind = [np.array([ind[0],ind[-1]+1]) for ind in park_ind] #list of array of index of when there is a mobility travel
                
            en_to_charge = 0  # Initialise value for Travel Based chaging mode          
            
            # Iterates over all parkings (park = 0 corresponds to the period where no travel was made yet, so is not evaluated)
            for park in range(1, len(park_ind)-1): 
                
                # SOC at the beginning of the parking
                SOC_park = SOC[park_ind[park][0]]
                
                # Index range of when the car is parked                
                ind_park_range = np.arange(park_ind[park][0], park_ind[park][1])                    
                
                #Charging only the energy consumed in the last travel                
                if charging_mode == 'Travel Based':   
                    travel_ind_range = np.arange(park_ind[park-1][1], park_ind[park][0])
                    en_travel = abs(np.sum(power[travel_ind_range])) 
                    en_charge_tot = en_travel + en_to_charge
                else: 
                    en_charge_tot = 0
                    
                # if logistic is True:                      # Option of introducing the probability of charging based on the SOC of the car (Behavioural aspect)
                #     ch_prob = charge_prob(SOC[park_ind[park][0]])
                # else:                                     # If the behavioural mode is not active, the user will always try to charge 
                #     ch_prob = 1
                # if infr_prob == 'piecewise':              # Use of piecewise function based on hour of the day 
                #     infr_p = infrastructure_prob(minutes[park_ind[park][0]].hour, infr_prob) 
                # elif isinstance(infr_prob, (int, float)): # Constant probability of finding infrastructure
                #     infr_p = infr_prob
                
                # Energy used in the following travel
                if park == range(1, len(park_ind))[-1]: # In the last park there is no following travel
                    en_next_travel = 0
                else:       
                    next_travel_ind_range = np.arange(park_ind[park][1], park_ind[park+1][0])
                    en_next_travel = abs(np.sum(power[next_travel_ind_range]))                 
                
                # Residual energy in the EV Battery
                residual_energy = (Us.App_list[0].Battery_cap*60)*SOC_park
                                
                # Control to check if the user can charge based on infrastructure 
                # availability, SOC, time of the day (Depending on the options activated)
                if ((ch_prob(SOC_park) > np.random.rand() and
                    infr_p(minutes, park_ind[park][0], infr_prob) > np.random.rand() and
                    np.isin(ind_park_range, charge_range).any()) or # If parking happens during night
                    np.around(SOC_park, 2) <= SOC_min or
                    residual_energy < en_next_travel): 
                    
                # if (ch_prob > np.random.rand() and infr_p > np.random.rand()) or SOC[park_ind[park][0]] < SOC_min: #control to check if the user can charge based on infrastructure availability and SOC level (if behavioural modelling is activated)
                    
                    # Calculates the parking time
                    t_park = int(park_ind[park][1] - park_ind[park][0])                    
                    
                    # Fills the array of plug in (1 = plugged, 0 = not plugged)
                    plug_ind_range = np.arange(park_ind[park][0], park_ind[park][0] + t_park)
                    np.put(plug_in, plug_ind_range, 1)
                    
                    # Samples the nominal power of the charging station
                    P_ch_nom = random.choices(P_ch_station_list, weights=prob_ch_station)[0]                
                    
                    #Trying to charge always until SOC max
                    if charging_mode != 'Travel Based': 
                        en_charge_tot = (Us.App_list[0].Battery_cap*60)*(SOC_max - SOC_park)
                    
                    # Total charging time at P nominal 
                    t_ch_tot = int(round(en_charge_tot/P_ch_nom)) 

                    if charging_mode == 'Uncontrolled' or charging_mode == 'Travel Based':
                        t_ch = min(t_ch_tot, t_park) # charge until SOC max, if parking time allows                   
                        charge_ind_range = np.arange(park_ind[park][0], park_ind[park][0] + t_ch)
                        P_charge = P_ch_nom # Charge at nominal power

                    # elif charging_mode == 'Night Charge':
                    if charging_mode == 'Night Charge':                        
                        charge_ind_range = np.intersect1d(ind_park_range, charge_range)
                        t_ch = len(charge_ind_range)
                        if not charge_ind_range.size: # if array is empty means that we are in an extreme charging condition (SOC < 0.2 or next travel energy > SOC residual)
                            t_ch = min(t_ch_tot, t_park) # charge until SOC max, if parking time allows                   
                            charge_ind_range = np.arange(park_ind[park][0], park_ind[park][0] + t_ch)
                            P_charge = P_ch_nom # Charge at nominal power
                        # Minimum charging power (charging during night time)
                        P_ch_min = min(en_charge_tot/len(charge_ind_range), P_ch_nom)
                        P_charge = P_ch_min
                        
                    np.put(power, charge_ind_range, P_charge)
                    en_to_charge = en_charge_tot - (t_ch * P_charge)
                        
                    delta_soc = power / (Us.App_list[0].Battery_cap * 60) # To evaluate the capacity in kW - min
                    SOC = delta_soc
                    SOC[0] = SOC_init
                    SOC = np.cumsum(SOC)
                
                else: # if the user does not want to charge, then the energy consumed will be charged in a following parking                         
                    en_to_charge = en_charge_tot                        
                                    
            power_pos = np.where(power<0, 0, power)
            
            SOC_user[Us.user_name].append(SOC)
            Charging_profile_user[Us.user_name].append(power_pos)
            plug_in_user[Us.user_name].append(plug_in)
            
            Charging_profile = Charging_profile + power_pos
            
            if all(SOC > 0): #Check that the car never has SOC < 0
                continue
            else: 
                print(f"[WARNING: Charging process User {i + 1} ({Us.user_name}) not properly constructed, SOC < 0 in time {list(np.where(SOC<0)[0])}]") 
        
        num_us = num_us +  Us.num_users
        print('Charging Profile', num_us, '/', tot_users, 'completed') #screen update about progress of computation
    
    return (Charging_profile_user, Charging_profile, SOC_user, plug_in_user)


# SOC_user = SOC_user1
# SOC_av = 0.8 - SOC_user['Working - Large car'][0]
# SOC_av = SOC_av*100
