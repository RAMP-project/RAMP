# -*- coding: utf-8 -*-

# %% Import required libraries
import numpy as np
import random
import math
from ramp.core.initialise import initialise_inputs
from ramp.core.core import UseCase

# %% Core model stochastic script


def stochastic_process(
    j=None, fname=None, num_profiles=None, day_type=None, parallel=False
):
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

    peak_enlarge, user_list, num_profiles = initialise_inputs(j, fname, num_profiles)

    # Calculation of the peak time range, which is used to discriminate between off-peak
    # and on-peak coincident switch-on probability, corresponds to step 1. of [1], p.6
    peak_time_range = calc_peak_time_range(user_list, peak_enlarge)

    uc = UseCase(users=user_list)

    if parallel is True:
        profiles = uc.generate_daily_load_profiles_parallel(
            num_profiles, peak_time_range, day_type
        )
    else:
        profiles = uc.generate_daily_load_profiles(
            num_profiles, peak_time_range, day_type
        )

    return profiles
