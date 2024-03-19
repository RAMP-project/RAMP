import numpy as np
import pytest
from ramp import UseCase, User


def test_skip_when_func_time_zero():
    # Generate test user and appliance
    user = User(user_name="Test User", num_users=1)
    appliance = user.add_appliance(
        name="Test Appliance",
        func_time=0,  # Set func_time to be 0
        func_cycle=20,
        time_fraction_random_variability=0.1,
    )

    # Add to use_case
    use_case = UseCase(name="test_use_case", users=[user])

    # Calculate peak time range for this use_case
    peak_time_range = use_case.calc_peak_time_range()

    # Generated one load profile of this appliance
    power = 1000
    appliance.generate_load_profile(
        prof_i=0, peak_time_range=peak_time_range, day_type=0, power=power
    )

    # Check that no use of this appliance is simulated -> the appliances load profile is always smaller than it's power
    # (Checking for the load_profile to always be 0 might be unreliable, since the RAMP core "marks" potential usage
    # windows with small power values larger 0)
    assert np.max(appliance.daily_use) < power


def test_warning_when_func_time_zero():
    user = User(user_name="Test User", num_users=1)
    with pytest.warns():
        appliance = user.add_appliance(
            name="Test Appliance",
            func_time=0,  # Set func_time to be 0
            func_cycle=20,
            time_fraction_random_variability=0.1,
        )
