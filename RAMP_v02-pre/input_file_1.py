# -*- coding: utf-8 -*-
"""
Created on Fri Oct 26 14:59:08 2018

@author: stevo
"""

#%% Definition of the inputs
'''
Input data definition (this is planned to be externalised in a separate script)
'''


from core import User, np
User_list = []

#Create new user classes
HH = User("household",14,3)
User_list.append(HH)


#Households
HH_indoor_bulb = HH.Appliance(HH,6,7,2,120,0.2,10)
HH_indoor_bulb.windows([1170,1440],[0,30],0.35)

HH_outdoor_bulb = HH.Appliance(HH,2,13,2,600,0.2,10)
HH_outdoor_bulb.windows([0,330],[1170,1440],0.35)

HH_TV = HH.Appliance(HH,2,60,3,180,0.1,5)
HH_TV.windows([720,900],[1170,1440],0.35,[0,60])

HH_DVD = HH.Appliance(HH,1,8,3,60,0.1,5)
HH_DVD.windows([720,900],[1170,1440],0.35,[0,60])

HH_Antenna = HH.Appliance(HH,1,8,3,120,0.1,5)
HH_Antenna.windows([720,900],[1170,1440],0.35,[0,60])

HH_Phone_charger = HH.Appliance(HH,5,2,2,300,0.2,5)
HH_Phone_charger.windows([1110,1440],[0,30],0.35)

HH_Freezer = HH.Appliance(HH,1,200,1,1440,0,30,'yes',3)
HH_Freezer.windows([0,1440],[0,0])
HH_Freezer.specific_cycle_1(200,20,5,10)
HH_Freezer.specific_cycle_2(200,15,5,15)
HH_Freezer.specific_cycle_3(200,10,5,20)
HH_Freezer.cycle_behaviour([480,1200],[0,0],[300,479],[0,0],[0,299],[1201,1440])

HH_Freezer2 = HH.Appliance(HH,1,200,1,1440,0,30,'yes',3)
HH_Freezer2.windows([0,1440],[0,0])
HH_Freezer2.specific_cycle_1(200,20,5,10)
HH_Freezer2.specific_cycle_2(200,15,5,15)
HH_Freezer2.specific_cycle_3(200,10,5,20)
HH_Freezer2.cycle_behaviour([480,1200],[0,0],[300,479],[0,0],[0,299],[1201,1440])

HH_Mixer = HH.Appliance(HH,1,50,3,30,0.1,1,occasional_use = 0.33)
HH_Mixer.windows([420,480],[660,750],0.35,[1140,1200])

HH_fans = HH.Appliance(HH,1,75,1,300,0.3,10)
HH_fans.windows([480,1320],[0,0],0.2)


