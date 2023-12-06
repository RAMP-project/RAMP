#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 28 15:40:12 2023

@author: claudia
"""

from ramp import User


import pytest


@pytest.fixture
def appliance_instance():
    # Create a User instance (you may need to provide the required arguments for User)
    user = User(user_name="Test User", num_users=1)
    appliance = user.add_appliance(
        name="Test Appliance",
        func_time=100,  # Set an appropriate func_time
        func_cycle=20,
        time_fraction_random_variability=0.1,
    )
    return appliance


# Define the test class for the Appliance class
class TestAppliance:
    # Test that the method returns an integer
    @pytest.mark.usefixtures("appliance_instance")
    def test_returns_integer_value(self, appliance_instance):
        result = appliance_instance.rand_total_time_of_use(
            [0, 480], [600, 1080], [1200, 1440]
        )
        assert isinstance(result, int)

    # Tests that the method returns a value greater than func_cycle
    @pytest.mark.usefixtures("appliance_instance")
    def test_rand_time_equal_or_greater_than_func_cycle(self, appliance_instance):
        # Define windows with total available time
        rand_window_1 = [0, 100]
        rand_window_2 = [200, 300]
        rand_window_3 = [400, 500]
        appliance_instance.func_cycle = 50
        # Generate a sample of 'rand_time' values
        sample_size = 100
        rand_time_sample = []
        for _ in range(sample_size):
            rand_time = appliance_instance.rand_total_time_of_use(
                rand_window_1, rand_window_2, rand_window_3
            )
            rand_time_sample.append(rand_time)
        assert all(
            rand_time >= appliance_instance.func_cycle for rand_time in rand_time_sample
        )

    # Tests that the method returns a value less than or equal to 0.99 * total_time
    @pytest.mark.usefixtures("appliance_instance")
    def test_rand_time_less_than_99_percent_total_time(self, appliance_instance):
        rand_window_1 = [0, 100]
        rand_window_2 = [200, 300]
        rand_window_3 = [400, 500]
        appliance_instance.func_time = 200
        appliance_instance.time_fraction_random_variability = 0.5
        # Call the method from the class
        rand_time = appliance_instance.rand_total_time_of_use(
            rand_window_1, rand_window_2, rand_window_3
        )
        total_time = (
            (rand_window_1[1] - rand_window_1[0])
            + (rand_window_2[1] - rand_window_2[0])
            + (rand_window_3[1] - rand_window_3[0])
        )
        assert rand_time <= 0.99 * total_time
