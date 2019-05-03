# -*- coding: utf-8 -*-

#%% Definition of the inputs
'''
Input data definition (this is planned to be externalised in a yaml or similar file)
'''

from core import User, User_list, np
import pandas as pd

#%% Inputs definition

def yearly_pattern():
    #Yearly behaviour pattern
    Year_behaviour = np.zeros(365)
    Year_behaviour[5:365:7] = 1
    Year_behaviour[6:365:7] = 1
    return (Year_behaviour)


def user_defined_inputs():
    #User classes definition
    MONOU1 = User("Single-family house, User 1",10)
    User_list.append(MONOU1)
    
    #Appliances definition
    
    #Single Family House, User 1
    MONOU1_shower_P = np.ones(365)*11300
    
    MONOU1_shower1 = MONOU1.Appliance(MONOU1,1,11300,2,10,0.5,2, wd_we_type = 0, thermal_P_var = 0.1)
    MONOU1_shower1.windows([7*60,10*60],[18*60,21*60],0.33)
    
    MONOU1_shower2 = MONOU1.Appliance(MONOU1,1,MONOU1_shower_P,2,10,0.5,2, wd_we_type = 1, thermal_P_var = 0.1)
    MONOU1_shower2.windows([12*60,16*60],[0,0],0.33)
    
