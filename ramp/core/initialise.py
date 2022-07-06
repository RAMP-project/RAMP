# -*- coding: utf-8 -*-

#%% Initialisation of a model instance

import numpy as np 
import importlib
from ramp.core.core import UseCase


def yearly_pattern():
    '''
    Definition of a yearly pattern of weekends and weekdays, in case some appliances have specific wd/we behaviour
    '''
    #Yearly behaviour pattern
    Year_behaviour = np.zeros(365)
    Year_behaviour[5:365:7] = 1
    Year_behaviour[6:365:7] = 1
    
    return(Year_behaviour)


def user_defined_inputs(j=None, fname=None):
    '''
    Imports an input file and returns a processed User_list
    '''
    # Back compatibility with old code
    if j is not None:
        file_module = importlib.import_module(f'ramp.input_files.input_file_{j}')
        User_list = file_module.User_list

    if fname is not None:
        usecase = UseCase()
        usecase.load(fname)
        User_list = usecase.users

    return(User_list)


def Initialise_model(num_profiles):
    '''
    The model is ready to be initialised
    '''

    if num_profiles is None:
        num_profiles = int(input("please indicate the number of profiles to be generated: ")) #asks the user how many profiles (i.e. code runs) he wants
    print('Please wait...') 
    Profile = [] #creates an empty list to store the results of each code run, i.e. each stochastically generated profile
    
    return (Profile, num_profiles)
    
def Initialise_inputs(j=None, fname=None):
    Year_behaviour = yearly_pattern()
    user_list = user_defined_inputs(j, fname)

    peak_enlarge = 0.15  # percentage random enlargement or reduction of peak time range length, corresponds to \delta_{peak} in [1], p.7
    return (peak_enlarge, Year_behaviour, user_list)

