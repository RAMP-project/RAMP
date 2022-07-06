# -*- coding: utf-8 -*-

#%% Import required libraries
import numpy as np
import random 
import math
from ramp.core.initialise import initialise_inputs

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
    for user in user_list:
        tot_max_profile = tot_max_profile + user.maximum_profile
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


def stochastic_process(j=None, fname=None, num_profiles=None, day_type=0):
    """Generate num_profiles load profile for the usecase

        Covers steps 1. and 2. of the algorithm described in [1], p.6-7

    day_type: int
        0 for a week day or 1 for a weekend day

    Notes
    -----
    [1] F. Lombardi, S. Balderrama, S. Quoilin, E. Colombo,
        Generating high-resolution multi-energy load profiles for remote areas with an open-source stochastic model,
        Energy, 2019, https://doi.org/10.1016/j.energy.2019.04.097.
    """
    # creates an empty list to store the results of each code run, i.e. each stochastically generated profile
    profiles = []

    peak_enlarge, user_list, num_profiles = initialise_inputs(j, fname, num_profiles)

    # Calculation of the peak time range, which is used to discriminate between off-peak
    # and on-peak coincident switch-on probability, corresponds to step 1. of [1], p.6
    peak_time_range = calc_peak_time_range(user_list, peak_enlarge)

    for prof_i in range(num_profiles):
        # initialise an empty daily profile (or profile load)
        # that will be filled with the sum of the daily profiles of each User instance
        usecase_load = np.zeros(1440)
        # for each User instance generate a load profile, iterating through all user of this instance and
        # all appliances they own, corresponds to step 2. of [1], p.7
        for user in user_list:
            user.generate_aggregated_load_profile(prof_i, peak_time_range, day_type)
            # aggregate the user load to the usecase load
            usecase_load = usecase_load + user.load
        profiles.append(usecase_load)
        # screen update about progress of computation
        print('Profile', prof_i+1, '/', num_profiles, 'completed')
    return profiles

