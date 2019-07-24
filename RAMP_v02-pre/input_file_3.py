# -*- coding: utf-8 -*-

#%% Definition of the inputs
'''
Input data definition
'''

from core import User, np, pd
User_list = []


'''
This example input file represents a single household user whose only load
is the "hairdryer". The example showcases how to model multi-year loads,
appliances that appear only after a certain minimum time threshold.
'''

#Create new user classes
HH = User("generic households",10)
User_list.append(HH)

#High-Income
HH_hairdryer = HH.Appliance(HH,1,1000,2,20,0.1,3, year_min = 0, initial_share=0.4)
HH_hairdryer.windows([390,540],[1080,1200],0.2)




