# -*- coding: utf-8 -*-

# %% Definition of the inputs
"""
Input data definition
"""

from ramp.core.core import User

User_list = []


"""
This example input file represents a single household user whose only loads
are the "cooking" activities. The example showcases how to model electric cooking loads by means of
the Prefence Index and User Preference attributes.
"""

# Create new user classes
HH = User(user_name="generic household", num_users=1, user_preference=3)
User_list.append(HH)

# Create new appliances

# Create Cooking appliances

HH_lunch1_soup = HH.add_appliance(
    number=1,
    power=1800,
    num_windows=2,
    func_time=70,
    time_fraction_random_variability=0.15,
    func_cycle=60,
    thermal_p_var=0.2,
    pref_index=1,
    fixed_cycle=1,
)
HH_lunch1_soup.windows(window_1=[12 * 60, 15 * 60], window_2=[0, 0], random_var_w=0.15)
HH_lunch1_soup.specific_cycle_1(p_11=1800, t_11=10, p_12=750, t_12=60, r_c1=0.15)
HH_lunch1_soup.cycle_behaviour(cw11=[12 * 60, 15 * 60], cw12=[0, 0])

HH_lunch2_rice = HH.add_appliance(
    1, 1800, 2, 25, 0.15, 20, thermal_p_var=0.2, pref_index=2, fixed_cycle=1
)
HH_lunch2_rice.windows([12 * 60, 15 * 60], [0, 0], 0.15)
HH_lunch2_rice.specific_cycle_1(1800, 10, 750, 15, 0.15)
HH_lunch2_rice.cycle_behaviour([12 * 60, 15 * 60], [0, 0])

HH_lunch2_egg = HH.add_appliance(1, 1200, 2, 3, 0.2, 3, thermal_p_var=0.2, pref_index=2)
HH_lunch2_egg.windows([12 * 60, 15 * 60], [0, 0], 0.15)

HH_lunch2_platano = HH.add_appliance(
    1, 1800, 2, 10, 0.15, 5, thermal_p_var=0.2, pref_index=2, fixed_cycle=1
)
HH_lunch2_platano.windows([12 * 60, 15 * 60], [0, 0], 0.15)
HH_lunch2_platano.specific_cycle_1(1800, 5, 1200, 5, 0.15)
HH_lunch2_platano.cycle_behaviour([12 * 60, 15 * 60], [0, 0])

HH_lunch2_meat = HH.add_appliance(
    1, 1200, 2, 7, 0.15, 3, thermal_p_var=0.2, pref_index=2
)
HH_lunch2_meat.windows([12 * 60, 15 * 60], [0, 0], 0.15)

HH_lunch3_beansnrice = HH.add_appliance(
    1, 1800, 2, 45, 0.2, 30, thermal_p_var=0.2, pref_index=3, fixed_cycle=1
)
HH_lunch3_beansnrice.windows([12 * 60, 15 * 60], [0, 0], 0.15)
HH_lunch3_beansnrice.specific_cycle_1(1800, 10, 750, 35, 0.2)
HH_lunch3_beansnrice.cycle_behaviour([12 * 60, 15 * 60], [0, 0])

HH_lunch3_meat = HH.add_appliance(
    1, 1200, 2, 10, 0.2, 5, thermal_p_var=0.2, pref_index=3
)
HH_lunch3_meat.windows([12 * 60, 15 * 60], [0, 0], 0.15)

HH_lunch_yuca = HH.add_appliance(
    1, 1800, 1, 25, 0.15, 10, thermal_p_var=0.2, pref_index=0, fixed_cycle=1
)
HH_lunch_yuca.windows([13 * 60, 14 * 60], [0, 0], 0.15)
HH_lunch_yuca.specific_cycle_1(1800, 10, 750, 15, 0.15)
HH_lunch_yuca.cycle_behaviour([12 * 60, 15 * 60], [0, 0])

HH_breakfast_huminta = HH.add_appliance(
    1, 1800, 1, 65, 0.15, 50, thermal_p_var=0.2, pref_index=0, fixed_cycle=1
)
HH_breakfast_huminta.windows([6 * 60, 9 * 60], [0, 0], 0.15)
HH_breakfast_huminta.specific_cycle_1(1800, 5, 750, 60, 0.15)
HH_breakfast_huminta.cycle_behaviour([6 * 60, 9 * 60], [0, 0])

HH_breakfast_bread = HH.add_appliance(
    1, 1800, 1, 15, 0.15, 10, thermal_p_var=0.2, pref_index=0, fixed_cycle=1
)
HH_breakfast_bread.windows([6 * 60, 9 * 60], [0, 0], 0.15)
HH_breakfast_bread.specific_cycle_1(1800, 10, 1200, 5, 0.15)
HH_breakfast_bread.cycle_behaviour([6 * 60, 9 * 60], [0, 0])

HH_breakfast_coffee = HH.add_appliance(
    1, 1800, 1, 5, 0.15, 2, thermal_p_var=0.2, pref_index=0
)
HH_breakfast_coffee.windows([6 * 60, 9 * 60], [0, 0], 0.15)

HH_mate = HH.add_appliance(1, 1800, 1, 30, 0.3, 2, thermal_p_var=0.2, pref_index=0)
HH_mate.windows([7 * 60, 20 * 60], [0, 0], 0.15)


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
