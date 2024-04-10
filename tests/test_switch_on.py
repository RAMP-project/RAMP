#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  5 10:47:58 2023

@author: claudia
"""

from ramp import User
import numpy as np
import scipy.optimize as opt

from ramp.core.constants import switch_on_parameters


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

        N = 100
        appliance = self.user.add_appliance(number=N, fixed="no")

        # Generate a sample of 'coincidence' values
        sample_size = N * 10
        coincidence_sample = []
        for _ in range(sample_size):
            coincidence = appliance.calc_coincident_switch_on(inside_peak_window=True)
            coincidence_sample.append(coincidence)

        def normed_dist(bins, mu, sigma):
            return (
                1
                / (sigma * np.sqrt(2 * np.pi))
                * np.exp(-((bins - mu) ** 2) / (2 * sigma**2))
            )

        # exclude the tail values i.e. only one appliance is switched on or all of them are, see https://github.com/RAMP-project/RAMP/issues/99 for illustrations
        coincidence_sample = np.array(coincidence_sample)
        max_val = np.max(coincidence_sample)
        coincidence_sample_reduced = coincidence_sample[
            np.where(coincidence_sample != 1)
        ]
        coincidence_sample_reduced = coincidence_sample_reduced[
            np.where(coincidence_sample_reduced != max_val)
        ]

        # compute the experimental probability density function for appliance numbers from 2 to N-1
        exp_pdf, bins = np.histogram(
            coincidence_sample_reduced,
            bins=[i for i in range(2, N + 1, 1)],
            density=True,
        )

        s_peak, mu_peak, op_factor = switch_on_parameters()
        mu = mu_peak * N
        sigma = s_peak * N * mu_peak

        p0 = [mu, sigma]  # Inital guess of mean and std
        errfunc = (
            lambda p, x, y: normed_dist(x, *p) - y
        )  # Distance to the target function
        p1, success = opt.leastsq(errfunc, p0[:], args=(bins[:-1], exp_pdf))

        # if not then the fit did not succeed
        assert success in [1, 2, 3, 4]

        fit_mu, fit_stdev = p1
        tolerance_mu = 0.05  # arbitrary
        tolerance_sigma = 0.1  # arbitrary
        err_mu = np.abs(mu - fit_mu) / mu
        err_sigma = np.abs(sigma - fit_stdev) / sigma
        assert (
            err_mu < tolerance_mu
        ), f"The mean value of a normal fit onto the sampled coincidence histogram ({fit_mu}) divert more than {tolerance_mu*100} % of the provided gaussian mean ({mu})"
        assert (
            err_sigma < tolerance_sigma
        ), f"The std value of a normal fit onto the sampled coincidence histogram ({fit_stdev}) divert more than {tolerance_sigma*100} % of the provided gaussian std ({sigma})"

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
