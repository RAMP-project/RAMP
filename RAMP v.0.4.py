# -*- coding: utf-8 -*-
"""
Created on Fri Jun 08 11:46:00 2018
This is the code for the open-source stochastic model for the generation of 
multi-energy load profiles in off-grid areas, called RAMP, v.0.4.

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
#%% Import required libraries
import matplotlib.pyplot as plt
import numpy as np
import numpy.ma as ma
import random 
import math
#%% Definition of Python classes that constitute the model architecture
'''
The code is based on two concatenated python classes, namely 'User' and
'Appliance', which are used to define at the outer level the User classes and 
at the inner level all the available appliances within each user class, with 
their own characteristics. Within the Appliance class, some other functions are
created to define windows of use and, if needed, specific duty cycles
'''

#Define the outer python class that represents 'User classes'
class User():
    
    def __init__(self, name = "", n_users = 1, us_pref = 0):
        self.user_name = name
        self.num_users = n_users #specifies the number of users within the class
        self.user_preference = us_pref #allows to check if random number coincides with user preference, to distinguish between various appliance_use options (e.g. different cooking options)
        self.App_list = [] #each instance of User (i.e. each user class) has its own list of Appliances

#Define the inner class for modelling user's appliances within the correspoding user class
    class Appliance():
    
        def __init__(self,user, n = 1, P = 0, w = 1, t = 0, r_t = 0, c = 0, fixed = 'no', fixed_cycle = 0, occasional_use = 1, flat = 'no', thermal_P_var = 0, pref_index = 0):
            self.user = user #user to which the appliance is bounded
            self.number = n #number of appliances of the specified kind
            self.POWER = P #nominal power of appliances of the specified kind
            self.num_windows = w #number of functioning windows to be considered
            self.func_time = t #total time the appliance is on during the day
            self.r_t = r_t #percentage of total time of use that is subject to random variability
            self.func_cycle = c #minimum time the appliance is kept on after switch-on event 
            self.fixed = fixed #if 'yes', all the 'n' appliances of this kind are always switched-on together
            self.activate = fixed_cycle #if equal to 1,2 or 3, respectively 1,2 or 3 duty cycles can be modelled, for different periods of the day
            self.occasional_use = occasional_use #probability that the appliance is always (i.e. everyday) included in the mix of appliances that the user actually switches-on during the day
            self.flat = flat #allows to model appliances that are not subject to any kind of random variability, such as public lighting
            self.Thermal_P_var = thermal_P_var #allows to randomly variate the App power within a range
            self.Pref_index = pref_index
        
        def windows(self, w1 = np.array([0,0]), w2 = np.array([0,0]),r_w = 0, w3 = np.array([0,0])):    
            self.window_1 = w1 #array of start and ending time for window of use #1
            self.window_2 = w2 #array of start and ending time for window of use #2
            self.window_3 = w3 #array of start and ending time for window of use #3
            self.random_var_w = r_w #percentage of variability in the start and ending times of the windows
            self.daily_use = np.zeros(1440) #create an empty daily use profile
            self.daily_use[w1[0]:(w1[1])] = np.full(np.diff(w1),0.001) #fills the daily use profile with infinitesimal values that are just used to identify the functioning windows
            self.daily_use[w2[0]:(w2[1])] = np.full(np.diff(w2),0.001) #same as above for window2
            self.daily_use[w3[0]:(w3[1])] = np.full(np.diff(w3),0.001) #same as above for window3
            self.daily_use_masked = np.zeros_like(ma.masked_not_equal(self.daily_use,0.001)) #apply a python mask to the daily_use array to make only functioning windows 'visibile'
            self.random_var_1 = int(r_w*np.diff(w1)) #calculate the random variability of window1, i.e. the maximum range of time they can be enlarged or shortened
            self.random_var_2 = int(r_w*np.diff(w2)) #same as above
            self.random_var_3 = int(r_w*np.diff(w3)) #same as above
            self.user.App_list.append(self) #automatically appends the appliance to the user's appliance list
            
            #if needed, specific duty cycles can be defined for each Appliance, for a maximum of three different ones
        def specific_cycle_1(self, P_11 = 0, t_11 = 0, P_12 = 0, t_12 = 0, r_c1 = 0):
            self.P_11 = P_11 #power absorbed during first part of the duty cycle
            self.t_11 = t_11 #duration of first part of the duty cycle
            self.P_12 = P_12 #power absorbed during second part of the duty cycle
            self.t_12 = t_12 #duration of second part of the duty cycle
            self.r_c1 = r_c1 #random variability of duty cycle segments duration
            self.fixed_cycle1 = np.concatenate(((np.ones(t_11)*P_11),(np.ones(t_12)*P_12))) #create numpy array representing the duty cycle
            
        def specific_cycle_2(self, P_21 = 0, t_21 = 0, P_22 = 0, t_22 = 0, r_c2 = 0):
            self.P_21 = P_21 #same as for cycle1
            self.t_21 = t_21
            self.P_22 = P_22
            self.t_22 = t_22
            self.r_c2 = r_c2
            self.fixed_cycle2 = np.concatenate(((np.ones(t_21)*P_21),(np.ones(t_22)*P_22)))
        
        def specific_cycle_3(self, P_31 = 0, t_31 = 0, P_32 = 0, t_32 = 0, r_c3 = 0):
            self.P_31 = P_31 #same as for cycle1
            self.t_31 = t_31
            self.P_32 = P_32
            self.t_32 = t_32
            self.r_c3 = r_c3
            self.fixed_cycle3 = np.concatenate(((np.ones(t_31)*P_31),(np.ones(t_32)*P_32)))
        
        #different time windows can be associated with different specific duty cycles
        def cycle_behaviour(self, cw11 = np.array([0,0]), cw12 = np.array([0,0]), cw21 = np.array([0,0]), cw22 = np.array([0,0]), cw31 = np.array([0,0]), cw32 = np.array([0,0])):
            self.cw11 = cw11 #first window associated with cycle1
            self.cw12 = cw12 #second window associated with cycle1
            self.cw21 = cw21 #same for cycle2
            self.cw22 = cw22
            self.cw31 = cw31 #same for cycle 3
            self.cw32 = cw32
            
#%% Initialisation of a model instance
'''
The model is ready to be initialised
'''
User_list = [] #creates an empty list to store all the needed User classes
num_profiles = int(input("please indicate the number of profiles to be generated: ")) #asks the user how many profiles (i.e. code runs) he wants
print('Please wait...') 
Profile = [] #creates an empty list to store the results of each code run, i.e. each stochastically generated profile

#%% Definition of the inputs
'''
Input data definition (this is planned to be externalised in a separate script)
'''

#User classes definition
HI = User("high income",1)
User_list.append(HI)

HI_Phone_charger = HI.Appliance(HI,1,10,2,300,0.2,5, thermal_P_var=0.2)
HI_Phone_charger.windows([1110,1440],[0,30],0.35)

#%%
'''
Calibration parameters. These can be changed in case the user has some real data against which the model can be calibrated
They regulate the probabilities defining the largeness of the peak window and the probability of coincident switch-on within the peak window
'''
peak_enlarg = 0 #percentage random enlargement or reduction of peak time range length
mu_peak = 0.5 #median value of gaussian distribution [0,1] by which the number of coincident switch_ons is randomly selected
s_peak = 1 #standard deviation (as percentage of the median value) of the gaussian distribution [0,1] above mentioned

#%% Core model stochastic script
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
        single_wcurve = Us.App_list[App_count].daily_use*Us.App_list[App_count].POWER*Us.App_list[App_count].number #this computes the curve for the specific App
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
                
                if App.Pref_index == 0:
                    pass
                else:
                    if rand_daily_pref == App.Pref_index: #evaluates if occasional use happens or not
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

                #redefines functioning windows based on the previous randomisation of the boundaries
                if App.flat == 'yes': #if the app is "flat" the code stops right after filling the newly created windows without applying any further stochasticity
                    App.daily_use[rand_window_1[0]:rand_window_1[1]] = np.full(np.diff(rand_window_1),App.POWER*App.number)
                    App.daily_use[rand_window_2[0]:rand_window_2[1]] = np.full(np.diff(rand_window_2),App.POWER*App.number)
                    App.daily_use[rand_window_3[0]:rand_window_3[1]] = np.full(np.diff(rand_window_3),App.POWER*App.number)
                    Us.load = Us.load + App.daily_use
                    continue
                else: #otherwise, for "non-flat" apps it puts a mask on the newly defined windows and continues    
                    App.daily_use[rand_window_1[0]:rand_window_1[1]] = np.full(np.diff(rand_window_1),0.001)
                    App.daily_use[rand_window_2[0]:rand_window_2[1]] = np.full(np.diff(rand_window_2),0.001)
                    App.daily_use[rand_window_3[0]:rand_window_3[1]] = np.full(np.diff(rand_window_3),0.001)
                App.daily_use_masked = np.zeros_like(ma.masked_not_equal(App.daily_use,0.001))
              
                App.power = App.POWER*(random.uniform((1-App.Thermal_P_var),(1+App.Thermal_P_var))) #randomly variates the power of thermal apps, otherwise variability is 0
                                    
                #random variability is also applied to the total functioning time and to the duration of the duty cycles, if they have been specified
                random_var_t = random.uniform((1-App.r_t),(1+App.r_t))
                if App.activate == 1:
                    App.p_11 = App.P_11*(random.uniform((1-App.Thermal_P_var),(1+App.Thermal_P_var))) #randomly variates the power of thermal apps, otherwise variability is 0
                    App.p_12 = App.P_12*(random.uniform((1-App.Thermal_P_var),(1+App.Thermal_P_var))) #randomly variates the power of thermal apps, otherwise variability is 0
                    random_cycle1 = np.concatenate(((np.ones(int(App.t_11*(random.uniform((1+App.r_c1),(1-App.r_c1)))))*App.p_11),(np.ones(int(App.t_12*(random.uniform((1+App.r_c1),(1-App.r_c1)))))*App.p_12))) #randomise also the fixed cycle
                    random_cycle2 = random_cycle1
                    random_cycle3 = random_cycle1
                elif App.activate == 2:
                    App.p_11 = App.P_11*(random.uniform((1-App.Thermal_P_var),(1+App.Thermal_P_var))) #randomly variates the power of thermal apps, otherwise variability is 0
                    App.p_12 = App.P_12*(random.uniform((1-App.Thermal_P_var),(1+App.Thermal_P_var))) #randomly variates the power of thermal apps, otherwise variability is 0
                    App.p_21 = App.P_21*(random.uniform((1-App.Thermal_P_var),(1+App.Thermal_P_var))) #randomly variates the power of thermal apps, otherwise variability is 0
                    App.p_22 = App.P_22*(random.uniform((1-App.Thermal_P_var),(1+App.Thermal_P_var))) #randomly variates the power of thermal apps, otherwise variability is 0
                    random_cycle1 = np.concatenate(((np.ones(int(App.t_11*(random.uniform((1+App.r_c1),(1-App.r_c1)))))*App.p_11),(np.ones(int(App.t_12*(random.uniform((1+App.r_c1),(1-App.r_c1)))))*App.p_12))) #randomise also the fixed cycle
                    random_cycle2 = np.concatenate(((np.ones(int(App.t_21*(random.uniform((1+App.r_c2),(1-App.r_c2)))))*App.p_21),(np.ones(int(App.t_22*(random.uniform((1+App.r_c2),(1-App.r_c2)))))*App.p_22))) #randomise also the fixed cycle
                    random_cycle3 = random_cycle1
                elif App.activate == 3:
                    App.p_11 = App.P_11*(random.uniform((1-App.Thermal_P_var),(1+App.Thermal_P_var))) #randomly variates the power of thermal apps, otherwise variability is 0
                    App.p_12 = App.P_12*(random.uniform((1-App.Thermal_P_var),(1+App.Thermal_P_var))) #randomly variates the power of thermal apps, otherwise variability is 0
                    App.p_21 = App.P_21*(random.uniform((1-App.Thermal_P_var),(1+App.Thermal_P_var))) #randomly variates the power of thermal apps, otherwise variability is 0
                    App.p_22 = App.P_22*(random.uniform((1-App.Thermal_P_var),(1+App.Thermal_P_var))) #randomly variates the power of thermal apps, otherwise variability is 0
                    App.p_31 = App.P_31*(random.uniform((1-App.Thermal_P_var),(1+App.Thermal_P_var))) #randomly variates the power of thermal apps, otherwise variability is 0
                    App.p_32 = App.P_32*(random.uniform((1-App.Thermal_P_var),(1+App.Thermal_P_var))) #randomly variates the power of thermal apps, otherwise variability is 0
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
                                    np.put(App.daily_use,indexes_adj,(App.power*coincidence))
                                    np.put(App.daily_use_masked,indexes_adj,(App.power*coincidence),mode='clip')
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
                                    np.put(App.daily_use,indexes,(App.power*coincidence))
                                    np.put(App.daily_use_masked,indexes,(App.power*coincidence),mode='clip')
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
    
#%% Post-processing
'''
Just some additional code lines to calculate useful indicators and generate plots
'''

Profile_avg = np.zeros(1440)
for pr in Profile:
    Profile_avg = Profile_avg + pr
Profile_avg = Profile_avg/len(Profile)
Profile_avg_kW = Profile_avg/1000

Profile_kW = []
for kW in Profile:
    Profile_kW.append(kW/1000)

Profile_series = np.array([])
for iii in Profile:
    Profile_series = np.append(Profile_series,iii)

x = np.arange(0,1440,5)
plt.figure(figsize=(10,5))
for n in Profile:
    plt.plot(np.arange(1440),n,'#b0c4de')
    plt.xlabel('Time (hours)')
    plt.ylabel('Power (W)')
    plt.ylim(ymin=0)
    #plt.ylim(ymax=5000)
    plt.margins(x=0)
    plt.margins(y=0)
plt.plot(np.arange(1440),Profile_avg,'#4169e1')
plt.xticks([0,240,480,(60*12),(60*16),(60*20),(60*24)],[0,4,8,12,16,20,24])
#plt.savefig('D:/OneDrive/Research/My Articles/Articolo MultiEnergyLoads/shower.eps', format='eps', dpi=1000)
plt.show()

'''
x = np.arange(0,1440,5)
plt.figure(figsize=(10,5))
for n in Profile:
    plt.plot(np.arange(1440),n,'#b0c4de')
    plt.xlabel('Time (hours)')
    plt.ylabel('Power (W)')
    plt.ylim(ymin=0)
    plt.ylim(ymax=200000)
    plt.margins(x=0)
    plt.margins(y=0)
#plt.plot(np.arange(1440),(Nov_minute),'r', label='Measured')
#plt.plot(np.arange(1440),(January_minute*1000),'g')
plt.plot(np.arange(1440),Profile_avg,'#4169e1',label='Coliseum+Cooking scenario')
#plt.boxplot(Nov_days[0:1440:5], positions = x)
plt.xticks([0,240,480,(60*12),(60*16),(60*20),(60*24)],[0,4,8,12,16,20,24])
plt.legend(loc=2)
plt.savefig('Coliseum+Cooking.svg', format='svg', dpi=1000)

plt.show()
'''
#%% Export individual profiles
'''
for i in range (len(Profile)):
    np.save('p0%d.npy' % (i), Profile[i])
'''
'''
Profile = []
for i in range(21):
    Profile.append(np.load('November/Nov%d.npy' % i))
'''
