# -*- coding: utf-8 -*-

#%% Definition of the inputs
'''
Input data definition 
'''


from core import User, np
User_list = []

'''
This example input file represents an whole village-scale community,
adapted from the data used for the Journal publication. It should provide a 
complete guidance to most of the possibilities ensured by RAMP for inputs definition,
including specific modular duty cycles and cooking cycles. 
For examples related to "thermal loads", see the "input_file_2".
'''

#Create new user classes
HI = User("high income",3,3)
User_list.append(HI)

LI = User("low income",6,3)
User_list.append(LI)

#Create new appliances

#High-Income
HI_indoor_bulb = HI.Appliance(HI,5,7,2,120,0.2,10)
HI_indoor_bulb.windows([1170,1440],[0,30],0.35)


#Low-income
LI_indoor_bulb = LI.Appliance(LI,6,7,2,120,0.2,10, year_min=2, initial_share=0.5)
LI_indoor_bulb.windows([1170,1440],[0,30],0.35)
