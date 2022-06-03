# -*- coding: utf-8 -*-

#%% Definition of the inputs
'''
Input data definition
'''

from ramp.core.core import User, np, pd
User_list = []


'''
This example input file represents a single household user whose only loads
are the "cooking" activities. The example showcases how to model electric cooking loads by means of
the Prefence Index and User Preference attributes.
'''

#Create new user classes
HH = User("generic household",1,3)
User_list.append(HH)

#Create new appliances

#Create Cooking appliances

HH_lunch1_soup = HH.Appliance(HH,1,1800,2,70,0.15,60, thermal_P_var = 0.2, pref_index =1, fixed_cycle=1)
HH_lunch1_soup.windows([12*60,15*60],[0,0],0.15)
HH_lunch1_soup.specific_cycle_1(1800,10,750,60,0.15)
HH_lunch1_soup.cycle_behaviour([12*60,15*60],[0,0])

HH_lunch2_rice = HH.Appliance(HH,1,1800,2,25,0.15,20, thermal_P_var = 0.2, pref_index = 2, fixed_cycle=1)
HH_lunch2_rice.windows([12*60,15*60],[0,0],0.15)
HH_lunch2_rice.specific_cycle_1(1800,10,750,15,0.15)
HH_lunch2_rice.cycle_behaviour([12*60,15*60],[0,0])

HH_lunch2_egg = HH.Appliance(HH,1,1200,2,3,0.2,3, thermal_P_var = 0.2 , pref_index = 2)
HH_lunch2_egg.windows([12*60,15*60],[0,0],0.15)

HH_lunch2_platano = HH.Appliance(HH,1,1800,2,10,0.15,5, thermal_P_var = 0.2, pref_index = 2, fixed_cycle=1)
HH_lunch2_platano.windows([12*60,15*60],[0,0],0.15)
HH_lunch2_platano.specific_cycle_1(1800,5,1200,5,0.15)
HH_lunch2_platano.cycle_behaviour([12*60,15*60],[0,0])

HH_lunch2_meat = HH.Appliance(HH,1,1200,2,7,0.15,3, thermal_P_var = 0.2, pref_index = 2)
HH_lunch2_meat.windows([12*60,15*60],[0,0],0.15)

HH_lunch3_beansnrice = HH.Appliance(HH,1,1800,2,45,0.2,30, thermal_P_var =0.2 , pref_index = 3, fixed_cycle=1)
HH_lunch3_beansnrice.windows([12*60,15*60],[0,0],0.15)
HH_lunch3_beansnrice.specific_cycle_1(1800,10,750,35,0.2)
HH_lunch3_beansnrice.cycle_behaviour([12*60,15*60],[0,0])

HH_lunch3_meat = HH.Appliance(HH,1,1200,2,10,0.2,5, thermal_P_var = 0.2, pref_index = 3)
HH_lunch3_meat.windows([12*60,15*60],[0,0],0.15)

HH_lunch_yuca = HH.Appliance(HH,1,1800,1,25,0.15,10, thermal_P_var = 0.2, pref_index =0, fixed_cycle=1)
HH_lunch_yuca.windows([13*60,14*60],[0,0],0.15)
HH_lunch_yuca.specific_cycle_1(1800,10,750,15,0.15)
HH_lunch_yuca.cycle_behaviour([12*60,15*60],[0,0])

HH_breakfast_huminta = HH.Appliance(HH,1,1800,1,65,0.15,50, thermal_P_var = 0.2, pref_index =0, fixed_cycle=1)
HH_breakfast_huminta.windows([6*60,9*60],[0,0],0.15)
HH_breakfast_huminta.specific_cycle_1(1800,5,750,60,0.15)
HH_breakfast_huminta.cycle_behaviour([6*60,9*60],[0,0])

HH_breakfast_bread = HH.Appliance(HH,1,1800,1,15,0.15,10, thermal_P_var = 0.2, pref_index =0, fixed_cycle=1)
HH_breakfast_bread.windows([6*60,9*60],[0,0],0.15)
HH_breakfast_bread.specific_cycle_1(1800,10,1200,5,0.15)
HH_breakfast_bread.cycle_behaviour([6*60,9*60],[0,0])

HH_breakfast_coffee = HH.Appliance(HH,1,1800,1,5,0.15,2, thermal_P_var = 0.2, pref_index =0)
HH_breakfast_coffee.windows([6*60,9*60],[0,0],0.15)

HH_mate = HH.Appliance(HH,1,1800,1,30,0.3,2, thermal_P_var = 0.2, pref_index =0)
HH_mate.windows([7*60,20*60],[0,0],0.15)
