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
        corresponds to \delta_{peak} in [1], p.7

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
    peak_enlarge, Year_behaviour, User_list = Initialise_inputs(j, fname)
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
                    App.daily_use = np.zeros(1440)

                    # skip this appliance in any of the following applies
                    if (
                        # evaluates if occasional use happens or not
                        (random.uniform(0, 1) > App.occasional_use
                            # evaluates if daily preference coincides with the randomised daily preference number
                            or (App.pref_index != 0 and rand_daily_pref != App.pref_index)
                            # checks if the app is allowed in the given yearly behaviour pattern
                            or App.wd_we_type not in [Year_behaviour[prof_i], 2])
                    ):
                        continue

                    # recalculate windows start and ending times randomly, based on the inputs
                    rand_window_1 = App.calc_rand_window(window_idx=1)
                    rand_window_2 = App.calc_rand_window(window_idx=2)
                    rand_window_3 = App.calc_rand_window(window_idx=3)
                    rand_windows = [rand_window_1, rand_window_2, rand_window_3]

                    # random variability is applied to the total functioning time and to the duration
                    # of the duty cycles provided they have been specified
                    # step 2a of [1]
                    rand_time = App.rand_total_time_of_use(*rand_windows)

                    # redefines functioning windows based on the previous randomisation of the boundaries
                    # step 2b of [1]
                    if App.flat == 'yes':
                        # for "flat" appliances the algorithm stops right after filling the newly
                        # created windows without applying any further stochasticity
                        total_power_value = App.power[prof_i] * App.number
                        for rand_window in rand_windows:
                            App.daily_use[rand_window[0]:rand_window[1]] = np.full(np.diff(rand_window), total_power_value)
                        Us.load = Us.load + App.daily_use
                        continue
                    else:
                        # "non-flat" appliances a mask is applied on the newly defined windows and
                        # the algorithm goes further on
                        for rand_window in rand_windows:
                            App.daily_use[rand_window[0]:rand_window[1]] = np.full(np.diff(rand_window), 0.001)
                    App.daily_use_masked = np.zeros_like(ma.masked_not_equal(App.daily_use,0.001))

                    # calculates randomised cycles taking the random variability in the duty cycle duration
                    App.assign_random_cycles()

                    # steps 2c-2e repeated until the sum of the durations of all the switch-on events equals rand_time
                    App.generate_load_profile(rand_time, peak_time_range, *rand_windows, power=App.power[prof_i])

                    Us.load = Us.load + App.daily_use #adds the App profile to the User load
            Tot_Classes = Tot_Classes + Us.load #adds the User load to the total load of all User classes
        Profile.append(Tot_Classes) #appends the total load to the list that will contain all the generated profiles
        print('Profile',prof_i+1,'/',num_profiles,'completed') #screen update about progress of computation
    return(Profile)
