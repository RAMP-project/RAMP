# -*- coding: utf-8 -*-
"""
Created on Fri Oct 26 14:59:08 2018

@author: stevo
"""

#%% Definition of the inputs
'''
Data from Field Campaign Pistolese-Stevanato 2017
'''



from core import User, np
User_list = []


#Create new user classes
HI = User("high income",130,3)
User_list.append(HI)



#Create new appliances


#High-Income 

HI_indoor_bulb = HI.Appliance(HI,7,60,2,360,0.2,2)
HI_indoor_bulb.windows([1080,1440],[0,30],0.35)


