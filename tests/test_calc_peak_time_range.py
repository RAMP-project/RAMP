#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  5 16:21:32 2023

@author: claudia
"""

import numpy as np
import scipy.stats as stats

# TODO fix this in regard to issue https://github.com/RAMP-project/RAMP/issues/99
# def test_peak_time_range_values():
#     """
#     Perform a statistical analysis on the peak time range values obtained from the calc_peak_time_range function.
#
#     Inputs:
#     - user_list: A list containing all the user types.
#     - num_repetitions: The desired number of repetitions for the statistical analysis.
#
#     Outputs:
#     - None (The function performs an assertion to check the normality of the mean values).
#     """
#
#     user_list = user_defined_inputs(j=1, fname=None)
#
#     num_repetitions = 100  # Set the desired number of repetitions
#     results = []
#
#     for _ in range(num_repetitions):
#         peak_time_range = calc_peak_time_range(user_list, peak_enlarge=0.15)
#         results.append(peak_time_range)
#
#     statistics_dict = {}
#
#     # Performing statistical analysis on the results
#     for i, arr in enumerate(results):
#         statistics_dict[i] = {"mean": np.mean(arr)}
#
#     # Extract the mean values
#     mean_sample = [inner_dict["mean"] for inner_dict in statistics_dict.values()]
#     # Perform the normality test (Shapiro-Wilk in this sample)
#     _, p_value = stats.shapiro(mean_sample)
#     assert p_value > 0.05
