# -*- coding: utf-8 -*-
"""
Created on Fri Oct 26 14:59:08 2018

@author: stevo
"""

#%% Definition of the inputs
'''
Input data definition (this is planned to be externalised in a separate script)
'''
def input_file(k):
    from core import User
    User_list = []
            
    
    #Create new user classes
    HI = User("high income",11*k,3)
    User_list.append(HI)
    
    HMI = User("higher middle income",38*k,3)
    User_list.append(HMI)
    
        
    #Create new appliances
    
    #High-Income
    HI_indoor_bulb = HI.Appliance(HI,6,7,2,120,0.2,10)
    HI_indoor_bulb.windows([1170,1440],[0,30],0.35)
    
    HI_outdoor_bulb = HI.Appliance(HI,2,13,2,600,0.2,10)
    HI_outdoor_bulb.windows([0,330],[1170,1440],0.35)
    
    HI_TV = HI.Appliance(HI,2,60,3,180,0.1,5)
    HI_TV.windows([720,900],[1170,1440],0.35,[0,60])
    
    HI_DVD = HI.Appliance(HI,1,8,3,60,0.1,5)
    HI_DVD.windows([720,900],[1170,1440],0.35,[0,60])
    
    HI_Antenna = HI.Appliance(HI,1,8,3,120,0.1,5)
    HI_Antenna.windows([720,900],[1170,1440],0.35,[0,60])
    
    HI_Phone_charger = HI.Appliance(HI,5,2,2,300,0.2,5)
    HI_Phone_charger.windows([1110,1440],[0,30],0.35)
    
    HI_Freezer = HI.Appliance(HI,1,200,1,1440,0,30,'yes',3)
    HI_Freezer.windows([0,1440],[0,0])
    HI_Freezer.specific_cycle_1(200,20,5,10)
    HI_Freezer.specific_cycle_2(200,15,5,15)
    HI_Freezer.specific_cycle_3(200,10,5,20)
    HI_Freezer.cycle_behaviour([480,1200],[0,0],[300,479],[0,0],[0,299],[1201,1440])
    
    HI_Freezer2 = HI.Appliance(HI,1,200,1,1440,0,30,'yes',3)
    HI_Freezer2.windows([0,1440],[0,0])
    HI_Freezer2.specific_cycle_1(200,20,5,10)
    HI_Freezer2.specific_cycle_2(200,15,5,15)
    HI_Freezer2.specific_cycle_3(200,10,5,20)
    HI_Freezer2.cycle_behaviour([480,1200],[0,0],[300,479],[0,0],[0,299],[1201,1440])
    
    HI_Mixer = HI.Appliance(HI,1,50,3,30,0.1,1,occasional_use = 0.33)
    HI_Mixer.windows([420,480],[660,750],0.35,[1140,1200])
    
    #Higher-Middle Income
    HMI_indoor_bulb = HMI.Appliance(HMI,5,7,2,120,0.2,10)
    HMI_indoor_bulb.windows([1170,1440],[0,30],0.35)
    
    HMI_outdoor_bulb = HMI.Appliance(HMI,2,13,2,600,0.2,10)
    HMI_outdoor_bulb.windows([0,330],[1170,1440],0.35)
    
    HMI_TV = HMI.Appliance(HMI,1,60,2,120,0.1,5)
    HMI_TV.windows([1170,1440],[0,60],0.35)
    
    HMI_DVD = HMI.Appliance(HMI,1,8,2,40,0.1,5)
    HMI_DVD.windows([1170,1440],[0,60],0.35)
    
    HMI_Antenna = HMI.Appliance(HMI,1,8,2,80,0.1,5)
    HMI_Antenna.windows([1170,1440],[0,60],0.35)
    
    HMI_Radio = HMI.Appliance(HMI,1,36,2,60,0.1,5)
    HMI_Radio.windows([390,450],[1140,1260],0.35)
    
    HMI_Phone_charger = HMI.Appliance(HMI,4,2,2,300,0.2,5)
    HMI_Phone_charger.windows([1110,1440],[0,30],0.35)
    
    HMI_Freezer = HMI.Appliance(HMI,1,200,1,1440,0,30, 'yes',3)
    HMI_Freezer.windows([0,1440],[0,0])
    HMI_Freezer.specific_cycle_1(200,20,5,10)
    HMI_Freezer.specific_cycle_2(200,15,5,15)
    HMI_Freezer.specific_cycle_3(200,10,5,20)
    HMI_Freezer.cycle_behaviour([480,1200],[0,0],[300,479],[0,0],[0,299],[1201,1440])
    
    HMI_Mixer = HMI.Appliance(HMI,1,50,3,30,0.1,1, occasional_use = 0.33)
    HMI_Mixer.windows([420,450],[660,750],0.35,[1020,1170])
    
    return(User_list)


