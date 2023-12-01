#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  5 10:47:58 2023

@author: claudia
"""

from ramp import User
from scipy import stats


class TestRandSwitchOnWindow:
    def setup_method(self):
        self.user = User(user_name="Test User", num_users=1)

    # Test when self.fixed = yes, all the apps are switched on together (should return the total number of apps)

    def test_all_appliances_switched_on_together(self):
        appliance = self.user.add_appliance(number=5, fixed="yes")
        coincidence = appliance.calc_coincident_switch_on()
        assert isinstance(coincidence, int)
        assert coincidence == appliance.number

    # Test when self.fixed= no and the index value lies in peak_time_range (test whether the coincidence values are normally distributed or not)
    def test_coincidence_normality_on_peak(self):
        # Create an instance of the Appliance class with the desired parameters

        appliance = self.user.add_appliance(number=10, fixed="no")

        # Generate a sample of 'coincidence' values
        sample_size = 30
        coincidence_sample = []
        for _ in range(sample_size):
            coincidence = appliance.calc_coincident_switch_on(inside_peak_window=True)
            coincidence_sample.append(coincidence)

        # Perform the Shapiro-Wilk test for normality
        _, p_value = stats.shapiro(coincidence_sample)

        # Assert that the p-value is greater than a chosen significance level
        assert p_value > 0.05, "The 'coincidence' values are not normally distributed."

    # Tests that the method returns a list of indexes within the available functioning windows when there are multiple available functioning windows and the random time is larger than the duration of the appliance's function cycle.

    def test_happy_path(self):
        appliance = self.user.add_appliance(func_cycle=2)
        appliance.free_spots = [slice(0, 5), slice(10, 15)]
        indexes = appliance.rand_switch_on_window(rand_time=6)
        assert all(index in range(0, 5) or index in range(10, 15) for index in indexes)

    # Tests that the method returns None when there are no available functioning windows.
    def test_edge_case_no_windows(self):
        appliance = self.user.add_appliance(func_cycle=2)
        appliance.free_spots = []
        indexes = appliance.rand_switch_on_window(rand_time=6)
        assert indexes is None

    # Tests that the method returns None when the available functioning window is smaller than the duration of the appliance's function cycle.
    def test_edge_case_small_window(self):
        appliance = self.user.add_appliance(func_cycle=5)
        appliance.free_spots = [slice(0, 3)]
        indexes = appliance.rand_switch_on_window(rand_time=6)
        assert indexes is None

    # Tests that the method returns a list of indexes within the available functioning window when the available functioning window is equal to the duration of the appliance's function cycle.
    def test_edge_case_equal_window(self):
        appliance = self.user.add_appliance(func_cycle=5)
        appliance.free_spots = [slice(0, 5)]
        indexes = appliance.rand_switch_on_window(rand_time=6)
        assert all(index in range(0, 5) for index in indexes)

    # Tests that the method returns a list of indexes within the available functioning window when the available functioning window is larger than the duration of the appliance's function cycle.
    def test_edge_case_large_window(self):
        appliance = self.user.add_appliance(func_cycle=2)
        appliance.free_spots = [slice(0, 10)]
        indexes = appliance.rand_switch_on_window(rand_time=6)
        assert all(index in range(0, 10) for index in indexes)

    # Tests that the method returns a list of indexes within the available functioning windows when the appliance has multiple free spots.
    def test_edge_case_multiple_free_spots(self):
        appliance = self.user.add_appliance(func_cycle=2)
        appliance.free_spots = [slice(0, 5), slice(10, 15), slice(20, 25)]
        indexes = appliance.rand_switch_on_window(rand_time=6)
        assert all(
            index in range(0, 5) or index in range(10, 15) or index in range(20, 25)
            for index in indexes
        )
