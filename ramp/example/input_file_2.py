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
HH = User("generic households", 1)
User_list.append(HH)

HH_shower_P = pd.read_csv("ramp/example/shower_P.csv")

# High-Income
HH_shower = HH.Appliance(1, HH_shower_P, 2, 15, 0.1, 3, thermal_P_var=0.2)
HH_shower.windows([390, 540], [1080, 1200], 0.2)


if __name__ == "__main__":
    from ramp.core.core import UseCase

    uc = UseCase(
        users=User_list,
        parallel_processing=False,
    )
    uc.initialize(peak_enlarge=0.15)

    Profiles_list = uc.generate_daily_load_profiles()

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
