#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 28 13:27:24 2023

@author: claudia
"""

import numpy as np
from ramp.core.stochastic_process import calc_peak_time_range
from ramp.core.core import User
from ramp.core.initialise import initialise_inputs
import pytest


def load_usecase(j=None, fname=None):
    peak_enlarge, user_list, num_profiles = initialise_inputs(
        j, fname, num_profiles=1
    )
    return user_list

class TestCalcPeakTimeRange:

    # Tests that the peak time range is calculated correctly for a single user class with the default peak_enlarge value
    def test_single_user_class_default_peak_enlarge(self):
        user_list = [User(maximum_profile=np.array([1, 2, 3, 4, 5]))]
        peak_time_range = calc_peak_time_range(user_list)
        assert isinstance(peak_time_range, np.ndarray)
        assert peak_time_range.shape[0] > 0
        assert peak_time_range.dtype == int
        assert np.all(peak_time_range >= 0)

    # Tests that the peak time range is calculated correctly for multiple user classes with the default peak_enlarge value
    def test_multiple_user_classes_default_peak_enlarge(self):
        user_list = [User(maximum_profile=np.array([1, 2, 3, 4, 5])),
                     User(maximum_profile=np.array([2, 3, 4, 5, 6]))]
        peak_time_range = calc_peak_time_range(user_list)
        assert isinstance(peak_time_range, np.ndarray)
        assert peak_time_range.shape[0] > 0
        assert peak_time_range.dtype == int
        assert np.all(peak_time_range >= 0)

    # Tests that the peak time range is calculated correctly for a single user class with a non-default peak_enlarge value
    def test_single_user_class_non_default_peak_enlarge(self):
        user_list = [User(maximum_profile=np.array([1, 2, 3, 4, 5]))]
        peak_time_range = calc_peak_time_range(user_list, peak_enlarge=0.2)
        assert isinstance(peak_time_range, np.ndarray)
        assert peak_time_range.shape[0] > 0
        assert peak_time_range.dtype == int
        assert np.all(peak_time_range >= 0)

    # Tests that the peak time range is calculated correctly for multiple user classes with a non-default peak_enlarge value
    def test_multiple_user_classes_non_default_peak_enlarge(self):
        user_list = [User(maximum_profile=np.array([1, 2, 3, 4, 5])),
                     User(maximum_profile=np.array([2, 3, 4, 5, 6]))]
        peak_time_range = calc_peak_time_range(user_list, peak_enlarge=0.2)
        assert isinstance(peak_time_range, np.ndarray)
        assert peak_time_range.shape[0] > 0
        assert peak_time_range.dtype == int
        assert np.all(peak_time_range >= 0)

    # Tests that the peak time range is calculated correctly for a single user class with peak_enlarge=0
    def test_single_user_class_peak_enlarge_0(self):
        user_list = [User(maximum_profile=np.array([1, 2, 3, 4, 5]))]
        peak_time_range = calc_peak_time_range(user_list, peak_enlarge=0)
        assert isinstance(peak_time_range, np.ndarray)
        assert peak_time_range.shape[0] > 0
        assert peak_time_range.dtype == int
        assert np.all(peak_time_range >= 0)

    # Tests that the peak time range is calculated correctly for multiple user classes with peak_enlarge=0
    def test_multiple_user_classes_peak_enlarge_0(self):
        user_list = [User(maximum_profile=np.array([1, 2, 3, 4, 5])),
                     User(maximum_profile=np.array([2, 3, 4, 5, 6]))]
        peak_time_range = calc_peak_time_range(user_list, peak_enlarge=0)
        assert isinstance(peak_time_range, np.ndarray)
        assert peak_time_range.shape[0] > 0
        assert peak_time_range.dtype == int
        assert np.all(peak_time_range >= 0)

    def test_calc_peak_time_range_with_inputs(self):
            j=1
            peak_enlarge=0.15
            user_list=load_usecase(j,peak_enlarge )
            #call the function onder test
            peak_time_range = calc_peak_time_range(user_list, peak_enlarge)
            #perform assertions to validate the output
            assert isinstance(peak_time_range, np.ndarray)  # Check if the result is a NumPy array
            assert peak_time_range.shape[0] > 0  # Check if the result array is not empty
            assert peak_time_range.dtype == int  # Check if the array contains integers
            assert np.all(peak_time_range >= 0)  # Check if all values are non-negative