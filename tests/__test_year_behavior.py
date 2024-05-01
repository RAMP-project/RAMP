import os
import pytest
import numpy as np

from ramp.core.core import User


class TestApplianceClass:
    def setup_method(self):
        HI = User("high income", 1)
        self.HI_Freezer = HI.add_appliance(1, 200, 1, 1440, 0, 30, "yes", 3)
        self.HI_Freezer.windows([0, 1440], [0, 0])
        self.HI_Freezer.specific_cycle_1(200, 20, 5, 10)
        self.HI_Freezer.specific_cycle_2(200, 15, 5, 15)
        self.HI_Freezer.specific_cycle_3(200, 10, 5, 20)
        self.HI_Freezer.cycle_behaviour(
            [480, 1200], [0, 0], [300, 479], [0, 0], [0, 299], [1201, 1440]
        )
        self.HI_Freezer.assign_random_cycles()

        self.HI_Freezer_fixed = HI.add_appliance(1, 200, 1, 1440, 0, 30, "yes", 3)
        self.HI_Freezer_fixed.windows([0, 1440], [0, 0])

        self.HI_Freezer_var = HI.add_appliance(
            1, 200, 1, 1440, 0, 30, "yes", 3, thermal_p_var=0.1
        )
        self.HI_Freezer_var.windows([0, 1440], [0, 0])

    def teardown_method(self):
        pass

    def test_first_cycle_correctly_updated(self):
        """Convert the 3 example .py input files to xlsx and compare each appliance of each user"""

        with pytest.raises(ValueError):
            print(self.HI_Freezer.daily_use)
            self.HI_Freezer.update_daily_use(
                coincidence=1, power=1, indexes=np.array([1])
            )
            print(self.HI_Freezer.daily_use)
        # print(self.HI_Freezer.random_cycle1)

        # pytest.fail()

        # test that the daily use is updated by the value (random_cycle_1 * coincidence)

    def test_first_cycle_correctly_updated(self):
        pass

    def test_second_cycle_correctly_updated(self):
        """Convert the 3 example .py input files to xlsx and compare each appliance of each user"""

        self.HI_Freezer.update_daily_use(coincidence=4, power=1, indexes=np.array([1]))

        # test that the daily use is updated by the value (random_cycle_1 * coincidence)

    def test_coincidence_number(self):
        """Convert the 3 example .py input files to xlsx and compare each appliance of each user"""

        self.HI_Freezer.update_daily_use(coincidence=2, power=1, indexes=np.array([1]))
        print(self.HI_Freezer.random_cycle1)
        print(self.HI_Freezer.daily_use)
        assert self.HI_Freezer.daily_use[9] == 400.0
        # test that the daily use is updated by the value (random_cycle_1 * coincidence)

    def test_third_cycle_correctly_updated(self):
        """Convert the 3 example .py input files to xlsx and compare each appliance of each user"""

        self.HI_Freezer.update_daily_use(coincidence=1, power=1, indexes=np.array([1]))

        # test that the daily use is updated by the value (random_cycle_1 * coincidence)

    def test_daily_use_without_duty_cycle_correctly_updated(self):
        """Convert the 3 example .py input files to xlsx and compare each appliance of each user"""

        self.HI_Freezer_fixed.update_daily_use(
            coincidence=1, power=1, indexes=np.array([1])
        )

    def test_daily_use_without_duty_cycle_but_thermal_var_correctly_updated(self):
        """Convert the 3 example .py input files to xlsx and compare each appliance of each user"""

        self.HI_Freezer_var.update_daily_use(
            coincidence=1, power=1, indexes=np.array([1])
        )

        # test that the daily use is updated by the value (random_cycle_1 * coincidence)


def test_something():
    """Convert the 3 example .py input files to xlsx and compare each appliance of each user"""
    HI = User("high income", 1)
    HI_Freezer = HI.add_appliance(1, 200, 1, 1440, 0, 30, "yes", 3)
    HI_Freezer.windows([0, 1440], [0, 0])
    HI_Freezer.specific_cycle_1(200, 20, 5, 10)
    HI_Freezer.specific_cycle_2(200, 15, 5, 15)
    HI_Freezer.specific_cycle_3(200, 10, 5, 20)
    HI_Freezer.cycle_behaviour(
        [480, 1200], [0, 0], [300, 479], [0, 0], [0, 299], [1201, 1440]
    )
    HI_Freezer.assign_random_cycles()
    # do somthing here for this particular usecase

    # test that the daily use is updated by the value (random_cycle_1 * coincidence)
