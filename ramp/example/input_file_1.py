# -*- coding: utf-8 -*-

# %% Definition of the inputs
"""
Input data definition
"""


from ramp.core.core import User

User_list = []

"""
This example input file represents an whole village-scale community,
adapted from the data used for the Journal publication. It should provide a
complete guidance to most of the possibilities ensured by RAMP for inputs definition,
including specific modular duty cycles and cooking cycles.
For examples related to "thermal loads", see the "input_file_2".
"""

# Create new user classes
HI = User("high income", 11, 3)
User_list.append(HI)

HMI = User("higher middle income", 38, 3)
User_list.append(HMI)

LMI = User("lower middle income", 34, 3)
User_list.append(LMI)

LI = User("low income", 45, 3)
User_list.append(LI)

Hospital = User("hospital", 1)
User_list.append(Hospital)

School = User("school", 1)
User_list.append(School)

Public_lighting = User("public lighting", 1)
User_list.append(Public_lighting)

Church = User("church", 3)
User_list.append(Church)

# Create new appliances

# Church
Ch_indoor_bulb = Church.Appliance(10, 26, 1, 210, 0.2, 60, "yes", flat="yes")
Ch_indoor_bulb.windows([1200, 1440], [0, 0], 0.1)

Ch_outdoor_bulb = Church.Appliance(7, 26, 1, 150, 0.2, 60, "yes", flat="yes")
Ch_outdoor_bulb.windows([1200, 1440], [0, 0], 0.1)

Ch_speaker = Church.Appliance(1, 100, 1, 150, 0.2, 60)
Ch_speaker.windows([1200, 1350], [0, 0], 0.1)

# Public lighting
Pub_lights = Public_lighting.Appliance(12, 40, 2, 310, 0.1, 300, "yes", flat="yes")
Pub_lights.windows([0, 336], [1110, 1440], 0.2)

Pub_lights_2 = Public_lighting.Appliance(25, 150, 2, 310, 0.1, 300, "yes", flat="yes")
Pub_lights_2.windows([0, 336], [1110, 1440], 0.2)


# High-Income
HI_indoor_bulb = HI.Appliance(6, 7, 2, 120, 0.2, 10)
HI_indoor_bulb.windows([1170, 1440], [0, 30], 0.35)

HI_outdoor_bulb = HI.Appliance(2, 13, 2, 600, 0.2, 10)
HI_outdoor_bulb.windows([0, 330], [1170, 1440], 0.35)

HI_TV = HI.Appliance(2, 60, 3, 180, 0.1, 5)
HI_TV.windows([720, 900], [1170, 1440], 0.35, [0, 60])

HI_DVD = HI.Appliance(1, 8, 3, 60, 0.1, 5)
HI_DVD.windows([720, 900], [1170, 1440], 0.35, [0, 60])

HI_Antenna = HI.Appliance(1, 8, 3, 120, 0.1, 5)
HI_Antenna.windows([720, 900], [1170, 1440], 0.35, [0, 60])

HI_Phone_charger = HI.Appliance(5, 2, 2, 300, 0.2, 5)
HI_Phone_charger.windows([1110, 1440], [0, 30], 0.35)

HI_Freezer = HI.Appliance(1, 200, 1, 1440, 0, 30, "yes", 3)
HI_Freezer.windows([0, 1440], [0, 0])
HI_Freezer.specific_cycle_1(200, 20, 5, 10)
HI_Freezer.specific_cycle_2(200, 15, 5, 15)
HI_Freezer.specific_cycle_3(200, 10, 5, 20)
HI_Freezer.cycle_behaviour(
    [480, 1200], [0, 0], [300, 479], [0, 0], [0, 299], [1201, 1440]
)

HI_Freezer2 = HI.Appliance(1, 200, 1, 1440, 0, 30, "yes", 3)
HI_Freezer2.windows([0, 1440], [0, 0])
HI_Freezer2.specific_cycle_1(200, 20, 5, 10)
HI_Freezer2.specific_cycle_2(200, 15, 5, 15)
HI_Freezer2.specific_cycle_3(200, 10, 5, 20)
HI_Freezer2.cycle_behaviour(
    [480, 1200], [0, 0], [300, 479], [0, 0], [0, 299], [1201, 1440]
)

HI_Mixer = HI.Appliance(1, 50, 3, 30, 0.1, 1, occasional_use=0.33)
HI_Mixer.windows([420, 480], [660, 750], 0.35, [1140, 1200])

# Higher-Middle Income
HMI_indoor_bulb = HMI.Appliance(5, 7, 2, 120, 0.2, 10)
HMI_indoor_bulb.windows([1170, 1440], [0, 30], 0.35)

HMI_outdoor_bulb = HMI.Appliance(2, 13, 2, 600, 0.2, 10)
HMI_outdoor_bulb.windows([0, 330], [1170, 1440], 0.35)

HMI_TV = HMI.Appliance(1, 60, 2, 120, 0.1, 5)
HMI_TV.windows([1170, 1440], [0, 60], 0.35)

HMI_DVD = HMI.Appliance(1, 8, 2, 40, 0.1, 5)
HMI_DVD.windows([1170, 1440], [0, 60], 0.35)

HMI_Antenna = HMI.Appliance(1, 8, 2, 80, 0.1, 5)
HMI_Antenna.windows([1170, 1440], [0, 60], 0.35)

HMI_Radio = HMI.Appliance(1, 36, 2, 60, 0.1, 5)
HMI_Radio.windows([390, 450], [1140, 1260], 0.35)

HMI_Phone_charger = HMI.Appliance(4, 2, 2, 300, 0.2, 5)
HMI_Phone_charger.windows([1110, 1440], [0, 30], 0.35)

HMI_Freezer = HMI.Appliance(1, 200, 1, 1440, 0, 30, "yes", 3)
HMI_Freezer.windows([0, 1440], [0, 0])
HMI_Freezer.specific_cycle_1(200, 20, 5, 10)
HMI_Freezer.specific_cycle_2(200, 15, 5, 15)
HMI_Freezer.specific_cycle_3(200, 10, 5, 20)
HMI_Freezer.cycle_behaviour(
    [480, 1200], [0, 0], [300, 479], [0, 0], [0, 299], [1201, 1440]
)

HMI_Mixer = HMI.Appliance(1, 50, 3, 30, 0.1, 1, occasional_use=0.33)
HMI_Mixer.windows([420, 450], [660, 750], 0.35, [1020, 1170])

# Lower-Midlle Income
LMI_indoor_bulb = LMI.Appliance(3, 7, 2, 120, 0.2, 10)
LMI_indoor_bulb.windows([1170, 1440], [0, 30], 0.35)

LMI_outdoor_bulb = LMI.Appliance(2, 13, 2, 600, 0.2, 10)
LMI_outdoor_bulb.windows([0, 330], [1170, 1440], 0.35)

LMI_TV = LMI.Appliance(1, 60, 3, 90, 0.1, 5)
LMI_TV.windows([450, 660], [720, 840], 0.35, [1170, 1440])

LMI_DVD = LMI.Appliance(1, 8, 3, 30, 0.1, 5)
LMI_DVD.windows([450, 660], [720, 840], 0.35, [1170, 1440])

LMI_Antenna = LMI.Appliance(1, 8, 3, 60, 0.1, 5)
LMI_Antenna.windows([450, 660], [720, 840], 0.35, [1170, 1440])

LMI_Phone_charger = LMI.Appliance(4, 2, 1, 300, 0.2, 5)
LMI_Phone_charger.windows([1020, 1440], [0, 0], 0.35)

LMI_Mixer = LMI.Appliance(1, 50, 2, 30, 0.1, 1, occasional_use=0.33)
LMI_Mixer.windows([660, 750], [1110, 1200], 0.35)

# Low Income
LI_indoor_bulb = LI.Appliance(2, 7, 2, 120, 0.2, 10)
LI_indoor_bulb.windows([1170, 1440], [0, 30], 0.35)

LI_outdoor_bulb = LI.Appliance(1, 13, 2, 600, 0.2, 10)
LI_outdoor_bulb.windows([0, 330], [1170, 1440], 0.35)

LI_TV = LI.Appliance(1, 60, 3, 90, 0.1, 5)
LI_TV.windows([750, 840], [1170, 1440], 0.35, [0, 30])

LI_DVD = LI.Appliance(1, 8, 3, 30, 0.1, 5)
LI_DVD.windows([750, 840], [1170, 1440], 0.35, [0, 30])

LI_Antenna = LI.Appliance(1, 8, 3, 60, 0.1, 5)
LI_Antenna.windows([750, 840], [1170, 1440], 0.35, [0, 30])

LI_Phone_charger = LI.Appliance(2, 2, 1, 300, 0.2, 5)
LI_Phone_charger.windows([1080, 1440], [0, 0], 0.35)

# Hospital
Ho_indoor_bulb = Hospital.Appliance(12, 7, 2, 690, 0.2, 10)
Ho_indoor_bulb.windows([480, 720], [870, 1440], 0.35)

Ho_outdoor_bulb = Hospital.Appliance(1, 13, 2, 690, 0.2, 10)
Ho_outdoor_bulb.windows([0, 330], [1050, 1440], 0.35)

Ho_Phone_charger = Hospital.Appliance(8, 2, 2, 300, 0.2, 5)
Ho_Phone_charger.windows([480, 720], [900, 1440], 0.35)

Ho_Fridge = Hospital.Appliance(1, 150, 1, 1440, 0, 30, "yes", 3)
Ho_Fridge.windows([0, 1440], [0, 0])
Ho_Fridge.specific_cycle_1(150, 20, 5, 10)
Ho_Fridge.specific_cycle_2(150, 15, 5, 15)
Ho_Fridge.specific_cycle_3(150, 10, 5, 20)
Ho_Fridge.cycle_behaviour(
    [580, 1200], [0, 0], [420, 579], [0, 0], [0, 419], [1201, 1440]
)

Ho_Fridge2 = Hospital.Appliance(1, 150, 1, 1440, 0, 30, "yes", 3)
Ho_Fridge2.windows([0, 1440], [0, 0])
Ho_Fridge2.specific_cycle_1(150, 20, 5, 10)
Ho_Fridge2.specific_cycle_2(150, 15, 5, 15)
Ho_Fridge2.specific_cycle_3(150, 10, 5, 20)
Ho_Fridge2.cycle_behaviour(
    [580, 1200], [0, 0], [420, 579], [0, 0], [0, 299], [1201, 1440]
)

Ho_Fridge3 = Hospital.Appliance(1, 150, 1, 1440, 0.1, 30, "yes", 3)
Ho_Fridge3.windows([0, 1440], [0, 0])
Ho_Fridge3.specific_cycle_1(150, 20, 5, 10)
Ho_Fridge3.specific_cycle_2(150, 15, 5, 15)
Ho_Fridge3.specific_cycle_3(150, 10, 5, 20)
Ho_Fridge3.cycle_behaviour(
    [580, 1200], [0, 0], [420, 479], [0, 0], [0, 419], [1201, 1440]
)

Ho_PC = Hospital.Appliance(2, 50, 2, 300, 0.1, 10)
Ho_PC.windows([480, 720], [1050, 1440], 0.35)

Ho_Mixer = Hospital.Appliance(1, 50, 2, 60, 0.1, 1, occasional_use=0.33)
Ho_Mixer.windows([480, 720], [1050, 1440], 0.35)

# School
S_indoor_bulb = School.Appliance(8, 7, 1, 60, 0.2, 10)
S_indoor_bulb.windows([1020, 1080], [0, 0], 0.35)

S_outdoor_bulb = School.Appliance(6, 13, 1, 60, 0.2, 10)
S_outdoor_bulb.windows([1020, 1080], [0, 0], 0.35)

S_Phone_charger = School.Appliance(5, 2, 2, 180, 0.2, 5)
S_Phone_charger.windows([510, 750], [810, 1080], 0.35)

S_PC = School.Appliance(18, 50, 2, 210, 0.1, 10)
S_PC.windows([510, 750], [810, 1080], 0.35)

S_Printer = School.Appliance(1, 20, 2, 30, 0.1, 5)
S_Printer.windows([510, 750], [810, 1080], 0.35)

S_Freezer = School.Appliance(1, 200, 1, 1440, 0, 30, "yes", 3)
S_Freezer.windows([0, 1440])
S_Freezer.specific_cycle_1(200, 20, 5, 10)
S_Freezer.specific_cycle_2(200, 15, 5, 15)
S_Freezer.specific_cycle_3(200, 10, 5, 20)
S_Freezer.cycle_behaviour(
    [580, 1200], [0, 0], [510, 579], [0, 0], [0, 509], [1201, 1440]
)

S_TV = School.Appliance(1, 60, 2, 120, 0.1, 5, occasional_use=0.5)
S_TV.windows([510, 750], [810, 1080], 0.35)

S_DVD = School.Appliance(1, 8, 2, 120, 0.1, 5, occasional_use=0.5)
S_DVD.windows([510, 750], [810, 1080], 0.35)

S_Stereo = School.Appliance(1, 150, 2, 90, 0.1, 5, occasional_use=0.33)
S_Stereo.windows([510, 750], [810, 1080], 0.35)

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
