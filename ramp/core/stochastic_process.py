# -*- coding: utf-8 -*-

#%% Import required libraries
import numpy as np
import numpy.ma as ma
import random 
import math
from ramp.core.initialise import Initialise_model, Initialise_inputs

#%% Core model stochastic script


def calc_peak_time_range(user_list, peak_enlarge=0.15):
    """
    Calculate the peak time range, which is used to discriminate between off-peak and on-peak coincident switch-on probability
    Calculate first the overall Peak Window (taking into account all User classes).
    The peak time range corresponds to `peak time frame` variable in eq. (1) of [1]
    The peak window is just a time window in which coincident switch-on of multiple appliances assumes a higher probability than off-peak
    Within the peak window, a random peak time is calculated and then enlarged into a peak_time_range following again a random procedure

    Parameters
    ----------
    user_list: list
        list containing all the user types
    peak_enlarge: float
        percentage random enlargement or reduction of peak time range length
        corresponds to \delta_{peak} in [1]

    Notes
    -----
    [1] F. Lombardi, S. Balderrama, S. Quoilin, E. Colombo,
        Generating high-resolution multi-energy load profiles for remote areas with an open-source stochastic model,
        Energy, 2019, https://doi.org/10.1016/j.energy.2019.04.097.

    Returns
    -------
    peak time range: numpy array
    """

    tot_max_profile = np.zeros(1440)  # creates an empty daily profile
    # Aggregate each User's theoretical max profile to the total theoretical max
    for Us in user_list:
        tot_max_profile = tot_max_profile + Us.maximum_profile
    # Find the peak window within the theoretical max profile
    peak_window = np.squeeze(np.argwhere(tot_max_profile == np.amax(tot_max_profile)))
    # Within the peak_window, randomly calculate the peak_time using a gaussian distribution
    peak_time = round(random.normalvariate(
        mu=round(np.average(peak_window)),
        sigma=1 / 3 * (peak_window[-1] - peak_window[0])
    ))
    rand_peak_enlarge = round(math.fabs(peak_time - random.gauss(mu=peak_time, sigma=peak_enlarge * peak_time)))
    # The peak_time is randomly enlarged based on the calibration parameter peak_enlarge
    return np.arange(peak_time - rand_peak_enlarge, peak_time + rand_peak_enlarge)

def Stochastic_Process(j=None, fname=None, num_profiles=None):
    Profile, num_profiles = Initialise_model(num_profiles)
    peak_enlarge, mu_peak, s_peak, op_factor, Year_behaviour, User_list = Initialise_inputs(j, fname)
    # Calculation of the peak time range, which is used to discriminate between off-peak and on-peak coincident switch-on probability
    peak_time_range = calc_peak_time_range(User_list, peak_enlarge)

    '''
    The core stochastic process starts here. For each profile requested by the software user, 
    each Appliance instance within each User instance is separately and stochastically generated
    '''
    for prof_i in range(num_profiles): #the whole code is repeated for each profile that needs to be generated
        Tot_Classes = np.zeros(1440) #initialise an empty daily profile that will be filled with the sum of the hourly profiles of each User instance
        for Us in User_list: #iterates for each User instance (i.e. for each user class)
            Us.load = np.zeros(1440) #initialise empty load for User instance
            for i in range(Us.num_users): #iterates for every single user within a User class. Each single user has its own separate randomisation
                if Us.user_preference == 0:
                    rand_daily_pref = 0
                    pass
                else:
                    rand_daily_pref = random.randint(1,Us.user_preference)
                for App in Us.App_list: #iterates for all the App types in the given User class
                    #initialises variables for the cycle
                    tot_time = 0
                    App.daily_use = np.zeros(1440)
                    if random.uniform(0,1) > App.occasional_use: #evaluates if occasional use happens or not
                        continue
                    else:
                        pass
                    
                    if App.pref_index == 0:
                        pass
                    else:
                        if rand_daily_pref == App.pref_index: #evaluates if daily preference coincides with the randomised daily preference number
                            pass
                        else:
                            continue
                    if App.wd_we_type == Year_behaviour[prof_i] or App.wd_we_type == 2 : #checks if the app is allowed in the given yearly behaviour pattern
                        pass
                    else:
                        continue

                    # recalculate windows start and ending times randomly, based on the inputs
                    rand_window_1 = App.calc_rand_window(window_idx=1)
                    rand_window_2 = App.calc_rand_window(window_idx=2)
                    rand_window_3 = App.calc_rand_window(window_idx=3)
                    rand_windows = [rand_window_1, rand_window_2, rand_window_3]
                    #redefines functioning windows based on the previous randomisation of the boundaries
                    if App.flat == 'yes': #if the app is "flat" the code stops right after filling the newly created windows without applying any further stochasticity
                        App.daily_use[rand_window_1[0]:rand_window_1[1]] = np.full(np.diff(rand_window_1),App.power[prof_i]*App.number)
                        App.daily_use[rand_window_2[0]:rand_window_2[1]] = np.full(np.diff(rand_window_2),App.power[prof_i]*App.number)
                        App.daily_use[rand_window_3[0]:rand_window_3[1]] = np.full(np.diff(rand_window_3),App.power[prof_i]*App.number)
                        Us.load = Us.load + App.daily_use
                        continue
                    else: #otherwise, for "non-flat" apps it puts a mask on the newly defined windows and continues    
                        App.daily_use[rand_window_1[0]:rand_window_1[1]] = np.full(np.diff(rand_window_1),0.001)
                        App.daily_use[rand_window_2[0]:rand_window_2[1]] = np.full(np.diff(rand_window_2),0.001)
                        App.daily_use[rand_window_3[0]:rand_window_3[1]] = np.full(np.diff(rand_window_3),0.001)
                    App.daily_use_masked = np.zeros_like(ma.masked_not_equal(App.daily_use,0.001))
                    
                    #random variability is applied to the total functioning time and to the duration of the duty cycles, if they have been specified
                    random_var_t = random.uniform((1-App.time_fraction_random_variability),(1+App.time_fraction_random_variability))
                    if App.fixed_cycle == 1:
                        App.p_11 = App.p_11*(random.uniform((1-App.thermal_p_var),(1+App.thermal_p_var))) #randomly variates the power of thermal apps, otherwise variability is 0
                        App.p_12 = App.p_12*(random.uniform((1-App.thermal_p_var),(1+App.thermal_p_var))) #randomly variates the power of thermal apps, otherwise variability is 0
                        random_cycle1 = np.concatenate(((np.ones(int(App.t_11*(random.uniform((1+App.r_c1),(1-App.r_c1)))))*App.p_11),(np.ones(int(App.t_12*(random.uniform((1+App.r_c1),(1-App.r_c1)))))*App.p_12))) #randomise also the fixed cycle
                        random_cycle2 = random_cycle1
                        random_cycle3 = random_cycle1
                    elif App.fixed_cycle == 2:
                        App.p_11 = App.p_11*(random.uniform((1-App.thermal_p_var),(1+App.thermal_p_var))) #randomly variates the power of thermal apps, otherwise variability is 0
                        App.p_12 = App.p_12*(random.uniform((1-App.thermal_p_var),(1+App.thermal_p_var))) #randomly variates the power of thermal apps, otherwise variability is 0
                        App.p_21 = App.p_21*(random.uniform((1-App.thermal_p_var),(1+App.thermal_p_var))) #randomly variates the power of thermal apps, otherwise variability is 0
                        App.p_22 = App.p_22*(random.uniform((1-App.thermal_p_var),(1+App.thermal_p_var))) #randomly variates the power of thermal apps, otherwise variability is 0
                        random_cycle1 = np.concatenate(((np.ones(int(App.t_11*(random.uniform((1+App.r_c1),(1-App.r_c1)))))*App.p_11),(np.ones(int(App.t_12*(random.uniform((1+App.r_c1),(1-App.r_c1)))))*App.p_12))) #randomise also the fixed cycle
                        random_cycle2 = np.concatenate(((np.ones(int(App.t_21*(random.uniform((1+App.r_c2),(1-App.r_c2)))))*App.p_21),(np.ones(int(App.t_22*(random.uniform((1+App.r_c2),(1-App.r_c2)))))*App.p_22))) #randomise also the fixed cycle
                        random_cycle3 = random_cycle1
                    elif App.fixed_cycle == 3:
                        App.p_11 = App.p_11*(random.uniform((1-App.thermal_p_var),(1+App.thermal_p_var))) #randomly variates the power of thermal apps, otherwise variability is 0
                        App.p_12 = App.p_12*(random.uniform((1-App.thermal_p_var),(1+App.thermal_p_var))) #randomly variates the power of thermal apps, otherwise variability is 0
                        App.p_21 = App.p_21*(random.uniform((1-App.thermal_p_var),(1+App.thermal_p_var))) #randomly variates the power of thermal apps, otherwise variability is 0
                        App.p_22 = App.p_22*(random.uniform((1-App.thermal_p_var),(1+App.thermal_p_var))) #randomly variates the power of thermal apps, otherwise variability is 0
                        App.p_31 = App.p_31*(random.uniform((1-App.thermal_p_var),(1+App.thermal_p_var))) #randomly variates the power of thermal apps, otherwise variability is 0
                        App.p_32 = App.p_32*(random.uniform((1-App.thermal_p_var),(1+App.thermal_p_var))) #randomly variates the power of thermal apps, otherwise variability is 0
                        random_cycle1 = random.choice([np.concatenate(((np.ones(int(App.t_11*(random.uniform((1+App.r_c1),(1-App.r_c1)))))*App.p_11),(np.ones(int(App.t_12*(random.uniform((1+App.r_c1),(1-App.r_c1)))))*App.p_12))),np.concatenate(((np.ones(int(App.t_12*(random.uniform((1+App.r_c1),(1-App.r_c1)))))*App.p_12),(np.ones(int(App.t_11*(random.uniform((1+App.r_c1),(1-App.r_c1)))))*App.p_11)))]) #randomise also the fixed cycle
                        random_cycle2 = random.choice([np.concatenate(((np.ones(int(App.t_21*(random.uniform((1+App.r_c2),(1-App.r_c2)))))*App.p_21),(np.ones(int(App.t_22*(random.uniform((1+App.r_c2),(1-App.r_c2)))))*App.p_22))),np.concatenate(((np.ones(int(App.t_22*(random.uniform((1+App.r_c2),(1-App.r_c2)))))*App.p_22),(np.ones(int(App.t_21*(random.uniform((1+App.r_c2),(1-App.r_c2)))))*App.p_21)))])                    
                        random_cycle3 = random.choice([np.concatenate(((np.ones(int(App.t_31*(random.uniform((1+App.r_c3),(1-App.r_c3)))))*App.p_31),(np.ones(int(App.t_32*(random.uniform((1+App.r_c3),(1-App.r_c3)))))*App.p_32))),np.concatenate(((np.ones(int(App.t_32*(random.uniform((1+App.r_c3),(1-App.r_c3)))))*App.p_32),(np.ones(int(App.t_31*(random.uniform((1+App.r_c3),(1-App.r_c3)))))*App.p_31)))])#this is to avoid that all cycles are sincronous                      
                    else:
                        pass
                    rand_time = round(random.uniform(App.func_time,int(App.func_time*random_var_t)))
                    #control to check that the total randomised time of use does not exceed the total space available in the windows
                    if rand_time > 0.99*(np.diff(rand_window_1)+np.diff(rand_window_2)+np.diff(rand_window_3)):
                        rand_time = int(0.99*(np.diff(rand_window_1)+np.diff(rand_window_2)+np.diff(rand_window_3)))
                    max_free_spot = rand_time #free spots are used to detect if there's still space for switch_ons. Before calculating actual free spots, the max free spot is set equal to the entire randomised func_time
                           
                    while tot_time <= rand_time: #this is the key cycle, which runs for each App until the switch_ons and their duration equals the randomised total time of use of the App
                            #check how many windows to consider
                            switch_on = App.switch_on(*rand_windows)
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
                                        coincidence = min(App.number,max(1,math.ceil(random.gauss((App.number*mu_peak+0.5),(s_peak*App.number*mu_peak))))) #calculates coincident behaviour within the peak time range
                                    elif np.in1d(peak_time_range,indexes_adj).any()== False and App.fixed == 'no': #check if indexes are off-peak and if coincident behaviour is locked or not
                                        Prob = random.uniform(0,(App.number-op_factor)/App.number) #calculates probability of coincident switch_ons off-peak
                                        array = np.arange(0,App.number)/App.number
                                        try:
                                            on_number = np.max(np.where(Prob>=array))+1
                                        except ValueError:
                                            on_number = 1 
                                        coincidence = on_number #randomly selects how many apps are on at the same time for each app type based on the above probabilistic algorithm
                                    else:
                                        coincidence = App.number #this is the case when App.fixed is activated. All 'n' apps of an App instance are switched_on altogether
                                    if App.fixed_cycle > 0: #evaluates if the app has some duty cycles to be considered
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
                                        np.put(App.daily_use,indexes_adj,(App.power*(random.uniform((1-App.thermal_p_var),(1+App.thermal_p_var)))*coincidence)) #randomises also the App Power if thermal_p_var is on
                                        np.put(App.daily_use_masked,indexes_adj,(App.power*(random.uniform((1-App.thermal_p_var),(1+App.thermal_p_var)))*coincidence),mode='clip')
                                    App.daily_use_masked = np.zeros_like(ma.masked_greater_equal(App.daily_use_masked,0.001)) #updates the mask excluding the current switch_on event to identify the free_spots for the next iteration
                                    tot_time = (tot_time - indexes.size) + indexes_adj.size #updates the total time correcting the previous value
                                    break #exit cycle and go to next App
                                else: #if the tot_time has not yet exceeded the App total functioning time, the cycle does the same without applying corrections to indexes size
                                    if np.in1d(peak_time_range,indexes).any() and App.fixed == 'no':
                                        coincidence = min(App.number,max(1,math.ceil(random.gauss((App.number*mu_peak+0.5),(s_peak*App.number*mu_peak)))))
                                    elif np.in1d(peak_time_range,indexes).any() == False and App.fixed == 'no':
                                        Prob = random.uniform(0,(App.number-op_factor)/App.number)
                                        array = np.arange(0,App.number)/App.number
                                        try:
                                            on_number = np.max(np.where(Prob>=array))+1
                                        except ValueError:
                                            on_number = 1
                                        coincidence = on_number
                                    else:
                                        coincidence = App.number
                                    if App.fixed_cycle > 0:
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
                                        np.put(App.daily_use,indexes,(App.power*(random.uniform((1-App.thermal_p_var),(1+App.thermal_p_var)))*coincidence))
                                        np.put(App.daily_use_masked,indexes,(App.power*(random.uniform((1-App.thermal_p_var),(1+App.thermal_p_var)))*coincidence),mode='clip')
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
                    Us.load = Us.load + App.daily_use #adds the App profile to the User load
            Tot_Classes = Tot_Classes + Us.load #adds the User load to the total load of all User classes
        Profile.append(Tot_Classes) #appends the total load to the list that will contain all the generated profiles
        print('Profile',prof_i+1,'/',num_profiles,'completed') #screen update about progress of computation
    return(Profile)
