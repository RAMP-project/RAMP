# -*- coding: utf-8 -*-

#%% Definition of the inputs
'''
Input data definition (this is planned to be externalised in a yaml or similar file)
'''

from core import User, np
from initialise import User_list

#%% Inputs definition

#Yearly behaviour pattern
Year_behaviour = np.zeros(365)
Year_behaviour[0:7] = [0,0,0,0,0,1,1]

#User classes definition
MONOU1 = User("Single-family house, User 1",100)
User_list.append(MONOU1)

#Appliances definition

#Single Family House, User 1
MONOU1_shower_P = np.ones(365)
#MONOU1_shower_P[0:7] = [11300,10000,5000,2000,20000,11300,3000]
MONOU1_shower_P = MONOU1_shower_P*11300

MONOU1_shower1 = MONOU1.Appliance(MONOU1,1,MONOU1_shower_P,2,10,0.5,2, wd_we_type = 0)
MONOU1_shower1.windows([7*60,10*60],[18*60,21*60],0.33)

MONOU1_shower2 = MONOU1.Appliance(MONOU1,1,MONOU1_shower_P,2,10,0.5,2, wd_we_type = 1)
MONOU1_shower2.windows([12*60,16*60],[0,0],0.33)

#MONOU1_bathbasin = MONOU1.Appliance(MONOU1,1,np.ones(365)*2750,1,6,0.5,1)
#MONOU1_bathbasin.windows([7*60,23*60],[0,0],0.05)
#
#MONOU1_kitchenbasin = MONOU1.Appliance(MONOU1,1,np.ones(365)*2750,1,6.5,0.5,1)
#MONOU1_kitchenbasin.windows([7*60,23*60],[0,0],0.05)