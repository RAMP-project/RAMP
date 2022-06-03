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


def switch_on_parameters():
    """
    Calibration parameters. These can be changed in case the user has some real data against which the model can be calibrated
    They regulate the probability of coincident switch-on within the peak window

    mu_peak corresponds to \mu_{%} in [1], p.8
    s_peak corresponds to \sigma_{%} in [1], p.8

    Notes
    -----
    [1] F. Lombardi, S. Balderrama, S. Quoilin, E. Colombo,
        Generating high-resolution multi-energy load profiles for remote areas with an open-source stochastic model,
        Energy, 2019, https://doi.org/10.1016/j.energy.2019.04.097.
    """

    mu_peak = 0.5  # median value of gaussian distribution [0,1] by which the number of coincident switch_ons is randomly selected
    s_peak = 0.5  # standard deviation (as percentage of the median value) of the gaussian distribution [0,1] above mentioned
    op_factor = 0.5  # off-peak coincidence calculation parameter

    return mu_peak, s_peak, op_factor


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

