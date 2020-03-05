# -*- coding: utf-8 -*-

#%% Initialisation of a model instance

from core import np
import importlib
import datetime

import pandas as pd

# Import holidays package including Latvia and Romania (edited version)
import sys,os
sys.path.append(os.path.abspath(r'C:\Users\Andrea\GitHub\python-holidays'))
import holidays 

def yearly_pattern(country, year, vacation = False):
    '''
    Definition of a yearly pattern of weekends and weekdays, in case some appliances have specific wd/we behaviour
    '''
    #Yearly behaviour pattern
    first_day = datetime.date(year, 1, 1).strftime("%A")
    Year_behaviour = np.zeros(365)
    
    dict_year = {'Monday'   : [5, 6], 
                 'Tuesday'  : [4, 5], 
                 'Wednesday': [3, 4],
                 'Thursday' : [2, 3], 
                 'Friday'   : [1, 2], 
                 'Saturday' : [0, 1], 
                 'Sunday'   : [0, 6]}
      
    for d in dict_year.keys():
        if first_day == d:
            Year_behaviour[dict_year[d][0]:365:7] = 1
            Year_behaviour[dict_year[d][1]:365:7] = 2
    
        # Adding Vacation days to the Yearly pattern
            
    if country == 'EL': 
        country = 'GR'
    elif country == 'FR':
        country = 'FRA'
        
    holidays_country = list(holidays.CountryHoliday(country, years = year).keys())
    
    for i in range(len(holidays_country)):
        day_of_year = list(holidays.IT(years = 2014).keys())[i].timetuple().tm_yday
        Year_behaviour[day_of_year-1] = 2
        
    return(Year_behaviour)

def user_defined_inputs(country):
    '''
    Imports an input file and returns a processed User_list
    '''
    User_list = getattr((importlib.import_module('%s' %country)), 'User_list')
    return(User_list)


def Initialise_model():
    '''
    The model is ready to be initialised
    '''
    num_profiles = int(input("please indicate the number of profiles to be generated: ")) #asks the user how many profiles (i.e. code runs) he wants
    if num_profiles > 366:
        print('[CRITICAL] Number of profiles higher than days in the year, please provide a number <= 366') 
        sys.exit()
    print('Please wait...') 
    Profile = [] #creates an empty list to store the results of each code run, i.e. each stochastically generated profile
    Usage = []
    
    return (Profile, Usage, num_profiles)
    
def Initialise_inputs(country, year):
    Year_behaviour = yearly_pattern(country, year)
    user_defined_inputs(country)
    user_list = user_defined_inputs(country)
    
    # Calibration parameters
    '''
    Calibration parameters. These can be changed in case the user has some real data against which the model can be calibrated
    They regulate the probabilities defining the largeness of the peak window and the probability of coincident switch-on within the peak window
    '''
    peak_enlarg = 0 #percentage random enlargement or reduction of peak time range length
    mu_peak = 0.5 #median value of gaussian distribution [0,1] by which the number of coincident switch_ons is randomly selected
    s_peak = 1 #standard deviation (as percentage of the median value) of the gaussian distribution [0,1] above mentioned
    
    return (peak_enlarg, mu_peak, s_peak, Year_behaviour, user_list)

