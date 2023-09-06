#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  5 10:47:58 2023

@author: claudia
"""

from ramp.core.core import Appliance


import pytest

class TestRandSwitchOnWindow:

    # Tests that the method returns a list of indexes within the available functioning windows when there are multiple available functioning windows and the random time is larger than the duration of the appliance's function cycle.
    def test_happy_path(self):
        appliance = Appliance(user=None, func_cycle=2)
        appliance.free_spots = [slice(0, 5), slice(10, 15)]
        indexes = appliance.rand_switch_on_window(rand_time=6)
        assert all(index in range(0, 5) or index in range(10, 15) for index in indexes)

    # Tests that the method returns None when there are no available functioning windows.
    def test_edge_case_no_windows(self):
        appliance = Appliance(user=None, func_cycle=2)
        appliance.free_spots = []
        indexes = appliance.rand_switch_on_window(rand_time=6)
        assert indexes is None

    # Tests that the method returns None when the available functioning window is smaller than the duration of the appliance's function cycle.
    def test_edge_case_small_window(self):
        appliance = Appliance(user=None, func_cycle=5)
        appliance.free_spots = [slice(0, 3)]
        indexes = appliance.rand_switch_on_window(rand_time=6)
        assert indexes is None

    # Tests that the method returns a list of indexes within the available functioning window when the available functioning window is equal to the duration of the appliance's function cycle.
    def test_edge_case_equal_window(self):
        appliance = Appliance(user=None, func_cycle=5)
        appliance.free_spots = [slice(0, 5)]
        indexes = appliance.rand_switch_on_window(rand_time=6)
        assert all(index in range(0, 5) for index in indexes)

    # Tests that the method returns a list of indexes within the available functioning window when the available functioning window is larger than the duration of the appliance's function cycle.
    def test_edge_case_large_window(self):
        appliance = Appliance(user=None, func_cycle=2)
        appliance.free_spots = [slice(0, 10)]
        indexes = appliance.rand_switch_on_window(rand_time=6)
        assert all(index in range(0, 10) for index in indexes)

    # Tests that the method returns a list of indexes within the available functioning windows when the appliance has multiple free spots.
    def test_edge_case_multiple_free_spots(self):
        appliance = Appliance(user=None, func_cycle=2)
        appliance.free_spots = [slice(0, 5), slice(10, 15), slice(20, 25)]
        indexes = appliance.rand_switch_on_window(rand_time=6)
        assert all(index in range(0, 5) or index in range(10, 15) or index in range(20, 25) for index in indexes)