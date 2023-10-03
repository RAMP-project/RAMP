#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 31 10:04:56 2023

@author: claudia
"""

import os
import pytest
import numpy as np
import random
import math
from scipy.stats import norm

from ramp.core.core import User, Appliance
from ramp.core.core import UseCase
from ramp.core.initialise import initialise_inputs
from ramp.core.stochastic_process import calc_peak_time_range

def load_usecase(j=None, fname=None):
    peak_enlarge, user_list, num_profiles = initialise_inputs(
        j, fname, num_profiles=1
    )
    return user_list

class TestPeakTime:
    def test_calc_peak_time_range(self):
            j=1
            peak_enlarge=0.15
            user_list=load_usecase(j)
            #call the function onder test
            peak_time_range = calc_peak_time_range(user_list, peak_enlarge)
            #perform assertions to validate the output
            assert isinstance(peak_time_range, np.ndarray)  # Check if the result is a NumPy array
            assert peak_time_range.shape[0] > 0  # Check if the result array is not empty
            assert peak_time_range.dtype == int  # Check if the array contains integers
            assert np.all(peak_time_range >= 0)  # Check if all values are non-negative
        