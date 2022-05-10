# -*- coding: utf-8 -*-

#%% Import required libraries
import numpy as np
import numpy.ma as ma
import pandas as pd
from ramp.core.constants import NEW_TO_OLD_MAPPING, OLD_TO_NEW_MAPPING

#%% Definition of Python classes that constitute the model architecture
'''
The code is based on two concatenated python classes, namely 'User' and
'Appliance', which are used to define at the outer level the User classes and 
at the inner level all the available appliances within each user class, with 
their own characteristics. Within the Appliance class, some other functions are
created to define windows of use and, if needed, specific duty cycles
'''


class User:
    def __init__(self, user_name="", num_users=1, user_preference=0):
        self.user_name = user_name
        self.num_users = num_users  # specifies the number of users within the class
        self.user_preference = user_preference  # allows to check if random number coincides with user preference, to distinguish between various appliance_use options (e.g. different cooking options)
        self.App_list = (
            []
        )  # each instance of User (i.e. each user class) has its own list of Appliances

    def add_appliance(self, *args, **kwargs):
        # I would add the appliance explicitely here, unless the appliance works only if a windows is defined
        return Appliance(self, *args, **kwargs)
    def Appliance(
        self,
        user,
        n=1,
        POWER=0,
        w=1,
        t=0,
        r_t=0,
        c=1,
        fixed="no",
        fixed_cycle=0,
        occasional_use=1,
        flat="no",
        thermal_P_var=0,
        pref_index=0,
        wd_we_type=2,
        P_series=False,
        name="",
    ):
        """Back-compatibility with legacy code"""
        return self.add_appliance(
            number=n,
            power=POWER,
            num_windows=w,
            func_time=t,
            time_fraction_random_variability=r_t,
            func_cycle=c,
            fixed=fixed,
            fixed_cycle=fixed_cycle,
            occasional_use=occasional_use,
            flat=flat,
            thermal_p_var=thermal_P_var,
            pref_index=pref_index,
            wd_we_type=wd_we_type,
            P_series=P_series,
            name=name,
        )
# Define the inner class for modelling user's appliances within the correspoding user class
class Appliance:
    def __init__(
        self,
        user,
        number=1,
        power=0,
        num_windows=1,
        func_time=0,
        time_fraction_random_variability=0,
        func_cycle=1,
        fixed="no",
        fixed_cycle=0,
        occasional_use=1,
        flat="no",
        thermal_p_var=0,
        pref_index=0,
        wd_we_type=2,
        p_series=False,
        name="",
    ):
        self.user = user  #user to which the appliance is bounded
        self.name = name
        self.number = number  #number of appliances of the specified kind
        self.num_windows = num_windows  #number of functioning windows to be considered
        self.func_time = func_time  #total time the appliance is on during the day
        self.time_fraction_random_variability = time_fraction_random_variability  #percentage of total time of use that is subject to random variability
        self.func_cycle = (
            func_cycle  #minimum time the appliance is kept on after switch-on event
        )
        self.fixed = fixed  #if 'yes', all the 'n' appliances of this kind are always switched-on together
        self.fixed_cycle = fixed_cycle  #if equal to 1,2 or 3, respectively 1,2 or 3 duty cycles can be modelled, for different periods of the day
        self.occasional_use = occasional_use  #probability that the appliance is always (i.e. everyday) included in the mix of appliances that the user actually switches-on during the day
        self.flat = flat  #allows to model appliances that are not subject to any kind of random variability, such as public lighting
        self.thermal_p_var = (
            thermal_p_var  #allows to randomly variate the App power within a range
        )
        self.pref_index = pref_index  #defines preference index for association with random User daily preference behaviour
        self.wd_we_type = wd_we_type  #defines if the App is associated with weekdays or weekends | 0 is wd 1 is we 2 is all week
        #TODO detect if power is a timeseries or a constant and get rid of P_series altogether
        if (
            p_series is False and isinstance(power, pd.DataFrame) is False
        ):  #check if the user defined P as timeseries
            self.power = power * np.ones(
                365
            )  #treat the power as single value for the entire year
        else:
            self.power = power.values[
                :, 0
            ]  #if a timeseries is given the power is treated as so

        # attributes initialized by self.windows
        self.random_var_w = None
        self.daily_use = None
        self.daily_use_masked = None

        # attributes used for specific fixed and random cycles
        self.p_11 = None
        self.p_12 = None
        self.t_11 = None
        self.t_12 = None
        self.r_c1 = None
        self.p_21 = None
        self.p_22 = None
        self.t_21 = None
        self.t_22 = None
        self.r_c2 = None
        self.p_31 = None
        self.p_32 = None
        self.t_31 = None
        self.t_32 = None
        self.r_c3 = None

        # attribute used for cycle_behaviour
        self.cw11 = np.array([0, 0])
        self.cw12 = np.array([0, 0])
        self.cw21 = np.array([0, 0])
        self.cw22 = np.array([0, 0])
        self.cw31 = np.array([0, 0])
        self.cw32 = np.array([0, 0])

        self.random_cycle1 = np.array([])
        self.random_cycle2 = np.array([])
        self.random_cycle3 = np.array([])

            else:

    def windows(self, window_1 = np.array([0,0]), window_2 = np.array([0,0]),random_var_w = 0, window_3 = np.array([0,0])):
        self.window_1 = window_1 #array of start and ending time for window of use #1
        self.window_2 = window_2 #array of start and ending time for window of use #2
        self.window_3 = window_3 #array of start and ending time for window of use #3
        self.random_var_w = random_var_w #percentage of variability in the start and ending times of the windows
        self.daily_use = np.zeros(1440) #create an empty daily use profile
        self.daily_use[window_1[0]:(window_1[1])] = np.full(np.diff(window_1),0.001) #fills the daily use profile with infinitesimal values that are just used to identify the functioning windows
        self.daily_use[window_2[0]:(window_2[1])] = np.full(np.diff(window_2),0.001) #same as above for window2
        self.daily_use[window_3[0]:(window_3[1])] = np.full(np.diff(window_3),0.001) #same as above for window3
        self.daily_use_masked = np.zeros_like(ma.masked_not_equal(self.daily_use,0.001)) #apply a python mask to the daily_use array to make only functioning windows 'visibile'
        self.random_var_1 = int(random_var_w*np.diff(window_1)) #calculate the random variability of window1, i.e. the maximum range of time they can be enlarged or shortened
        self.random_var_2 = int(random_var_w*np.diff(window_2)) #same as above
        self.random_var_3 = int(random_var_w*np.diff(window_3)) #same as above
        self.user.App_list.append(self) #automatically appends the appliance to the user's appliance list

        if self.fixed_cycle == 1:
            self.cw11 = self.window_1
            self.cw12 = self.window_2

        #if needed, specific duty cycles can be defined for each Appliance, for a maximum of three different ones
    def specific_cycle_1(self, p_11 = 0, t_11 = 0, p_21 = 0, t_21 = 0, r_c1 = 0):
        self.p_11 = p_11 #power absorbed during first part of the duty cycle
        self.t_11 = t_11 #duration of first part of the duty cycle
        self.p_12 = p_21 #power absorbed during second part of the duty cycle
        self.t_12 = t_21 #duration of second part of the duty cycle
        self.r_c1 = r_c1 #random variability of duty cycle segments duration
        # Below is not used
        self.fixed_cycle1 = np.concatenate(((np.ones(t_11)*p_11),(np.ones(t_21)*p_21))) #create numpy array representing the duty cycle

    def specific_cycle_2(self, p_21 = 0, t_21 = 0, p_22 = 0, t_22 = 0, r_c2 = 0):
        self.p_21 = p_21 #same as for cycle1
        self.t_21 = t_21
        self.p_22 = p_22
        self.t_22 = t_22
        self.r_c2 = r_c2
        # Below is not used
        self.fixed_cycle2 = np.concatenate(((np.ones(t_21)*p_21),(np.ones(t_22)*p_22)))

    def specific_cycle_3(self, p_31 = 0, t_31 = 0, p_32 = 0, t_32 = 0, r_c3 = 0):
        self.p_31 = p_31 #same as for cycle1
        self.t_31 = t_31
        self.p_32 = p_32
        self.t_32 = t_32
        self.r_c3 = r_c3
        # Below is not used
        self.fixed_cycle3 = np.concatenate(((np.ones(t_31)*p_31),(np.ones(t_32)*p_32)))

    #different time windows can be associated with different specific duty cycles
    def cycle_behaviour(self, cw11 = np.array([0,0]), cw12 = np.array([0,0]), cw21 = np.array([0,0]), cw22 = np.array([0,0]), cw31 = np.array([0,0]), cw32 = np.array([0,0])):

        # only used around line 223
        self.cw11 = cw11 #first window associated with cycle1
        self.cw12 = cw12 #second window associated with cycle1
        self.cw21 = cw21 #same for cycle2
        self.cw22 = cw22
        self.cw31 = cw31 #same for cycle 3
        self.cw32 = cw32
