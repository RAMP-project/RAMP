import os
import pytest
import numpy as np

from ramp import User, UseCase
import pandas as pd

pd.options.plotting.backend = "plotly"
import plotly.io as pio

pio.renderers.default = "browser"


@pytest.fixture
def test_use_case():
    # Create an instance of UseCase to test fix for the duty cycle repetition issue 78

    # %% Create test user
    test_user = User(user_name="test_user", num_users=1)

    # Create test appliance
    test_appliance = test_user.add_appliance(
        name="test_appliance_with_duty_cycles",
        func_time=4 * 60,  # runs for 2 hours per day
        window_1=[6 * 60, 20 * 60],  # usage timeframe from 10:00 to 17:00
        num_windows=1,
        fixed_cycle=1,  # appliance uses duty cycles
        # Duty cycle 1
        p_11=8000,  # power of the first cycle
        t_11=2,  # time needed for the first cycle
        p_12=2000,  # power of the second cycle
        t_12=18,  # time needed for the second cycle
        continuous_duty_cycle=0,
    )
    # Create and initialize UseCase
    duty_cycle_test_uc = UseCase(name="duty_cycle_test", users=[test_user])
    duty_cycle_test_uc.initialize(num_days=3)

    return duty_cycle_test_uc


class TestUseCase:
    @pytest.mark.usefixtures("test_use_case")
    def test_daily_load_profile(self, test_use_case):
        # Generate load profiles
        daily_load_profile = pd.DataFrame(
            test_use_case.generate_daily_load_profiles(),
            index=test_use_case.datetimeindex,
        )

        # Count separate switch-on events -> whenever there is a jump in the load profile from smaller or equal 0.001
        # to a value larger 0.001 (0.001 is used in the RAMP algorithm to "mark" available switch-on events, therefore
        # load profiles are often not actually 0 even though there is no appliance use scheduled

        # create a boolean mask for the condition
        mask = (daily_load_profile[0] <= 0.001) & (
            daily_load_profile[0].shift(-1) > 0.001
        )
        # Sum the number of switch on events
        switch_on_count = mask.sum()

        # Get the duration of the test duty cycle
        test_duty_cycle_duration = (
            test_use_case.appliances[0].t_11 + test_use_case.appliances[0].t_12
        )

        # Calculate how many switch-on events are expected
        expected_switch_on_count = (
            test_use_case.appliances[0].func_time / test_duty_cycle_duration
        )

        # In rare cases, it might happen that switch-on events are scheduled in direct succession
        # Therefore, the test should not fail if the number of expected switch-on events is not fully reached.
        # For the defined test, I allow 2 switch-on events less than expected

        # The test fails, if there are 2 switch-on events less than expected

        assert switch_on_count >= expected_switch_on_count - 2
