# -*- coding: utf-8 -*-

# %% Definition of the inputs
"""
Input data definition
"""

from ramp.core.core import User
import pandas as pd

User_list = []


"""
This example input file represents a single household user whose only load
is the "shower". The example showcases how to model thermal loads by means of
the thermal_P_var attribute.
"""

# Create new user classes
HH = User(user_name="generic households", num_users=1)
User_list.append(HH)

HH_shower_P = pd.read_csv("ramp/example/shower_P.csv")
HH_shower = HH.add_appliance(
    number=1,
    power=HH_shower_P,
    num_windows=2,
    func_time=15,
    time_fraction_random_variability=0.1,
    func_cycle=3,
    thermal_p_var=0.2,
)
HH_shower.windows(window_1=[390, 540], window_2=[1080, 1200], random_var_w=0.2)


if __name__ == "__main__":
    from ramp.core.core import UseCase

    uc = UseCase(
        users=User_list,
        parallel_processing=False,
    )
    uc.initialize(peak_enlarge=0.15)

    Profiles_list = uc.generate_daily_load_profiles(flat=False)

    # post-processing
    from ramp.post_process import post_process as pp

    Profiles_avg, Profiles_list_kW, Profiles_series = pp.Profile_formatting(
        Profiles_list
    )
    pp.Profile_series_plot(
        Profiles_series
    )  # by default, profiles are plotted as a series
    if (
        len(Profiles_list) > 1
    ):  # if more than one daily profile is generated, also cloud plots are shown
        pp.Profile_cloud_plot(Profiles_list, Profiles_avg)

    # this would be a new method using work of @mohammadamint
    # results = uc.export_results()
