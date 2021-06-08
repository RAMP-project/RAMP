# -*- coding: utf-8 -*-

#%% Definition of the inputs
'''
Input data definition 
'''

from ramp.core.core import User, np, pd
User_list = []


'''
This example input file represents a single household user whose only load
is the "shower". The example showcases how to model thermal loads by means of 
the thermal_P_var attribute.
'''

#Create new user classes
HH = User("generic households",1)
User_list.append(HH)

HH_shower_P = pd.read_csv('input_files/time_series/shower_P.csv')

#High-Income
HH_shower = HH.Appliance(HH,1,HH_shower_P,2,15,0.1,3, thermal_P_var = 0.2, P_series=True)
HH_shower.windows([390,540],[1080,1200],0.2)




