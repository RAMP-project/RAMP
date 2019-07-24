# -*- coding: utf-8 -*-

#%% Initialisation of a model instance

from core import np
import importlib


def yearly_pattern():
    '''
    Definition of a yearly pattern of weekends and weekdays, in case some appliances have specific wd/we behaviour
    '''
    #Yearly behaviour pattern
    Year_behaviour = np.zeros(365)
    Year_behaviour[5:365:7] = 1
    Year_behaviour[6:365:7] = 1

    return(Year_behaviour)


def user_defined_inputs(j):
    '''
    Imports an input file and returns a processed User_list
    '''
    User_list = getattr((importlib.import_module('input_file_%d' %j)), 'User_list')
    return(User_list)


def Initialise_model():
    '''
    The model is ready to be initialised
    '''
    num_years = int(input("please indicate the number of years to be considered: ")) #asks the user how many years of daily profiles (s)he wants
    if num_years == 1:
        num_profiles = int(input("please indicate the number of profiles to be generated: ")) #asks the user how many profiles (i.e. code runs) (s)he wants
        Profile = [] #creates an empty list to store the results of each code run, i.e. each stochastically generated profile
    else:
        num_profiles = 365
        Profile = [] #creates an empty list to store the results of each yearly run of 365 daily profiles
    print('Please wait...')
    return (Profile, num_profiles, num_years)

def Initialise_inputs(j):
    Year_behaviour = yearly_pattern()
    user_defined_inputs(j)
    user_list = user_defined_inputs(j)

    # Calibration parameters
    '''
    Calibration parameters. These can be changed in case the user has some real data against which the model can be calibrated
    They regulate the probabilities defining the largeness of the peak window and the probability of coincident switch-on within the peak window
    '''
    peak_enlarg = 0 #percentage random enlargement or reduction of peak time range length
    mu_peak = 0.5 #median value of gaussian distribution [0,1] by which the number of coincident switch_ons is randomly selected
    s_peak = 1 #standard deviation (as percentage of the median value) of the gaussian distribution [0,1] above mentioned

    return (peak_enlarg, mu_peak, s_peak, Year_behaviour, user_list)

