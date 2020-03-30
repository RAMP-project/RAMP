# -*- coding: utf-8 -*-

#%% Initialisation of a model instance

from core import np, pd
import importlib
import datetime
import calendar

# Import holidays package including Latvia and Romania (edited version)
import sys,os
sys.path.append(os.path.abspath(r'C:\Users\Andrea\GitHub\python-holidays'))
import holidays 

def yearly_pattern(country, year):
    '''
    Definition of a yearly pattern of weekends and weekdays, in case some appliances have specific wd/we behaviour
    ''' 
    #Yearly behaviour pattern
    first_day = datetime.date(year, 1, 1).strftime("%A")
    
    if calendar.isleap(year):
        year_len = 366
    else: 
        year_len = 365
        
    Year_behaviour = np.zeros(year_len)
    
    dict_year = {'Monday'   : [5, 6], 
                 'Tuesday'  : [4, 5], 
                 'Wednesday': [3, 4],
                 'Thursday' : [2, 3], 
                 'Friday'   : [1, 2], 
                 'Saturday' : [0, 1], 
                 'Sunday'   : [0, 6]}
      
    for d in dict_year.keys():
        if first_day == d:
            Year_behaviour[dict_year[d][0]:year_len:7] = 1
            Year_behaviour[dict_year[d][1]:year_len:7] = 2
    
    # Adding Vacation days to the Yearly pattern
            
    if country == 'EL': 
        country = 'GR'
    elif country == 'FR':
        country = 'FRA'
        
    holidays_country = list(holidays.CountryHoliday(country, years = year).keys())
    
    for i in range(len(holidays_country)):
        day_of_year = list(holidays.IT(years = year).keys())[i].timetuple().tm_yday
        Year_behaviour[day_of_year-1] = 2
    
    dummy_days = 7 # Number of days to add at the beginning and the end of the simulation to avoid special cases at the beginning and at the end
    dummy_days_array = np.zeros(dummy_days) 
    
    Year_behaviour = np.hstack((dummy_days_array, Year_behaviour, dummy_days_array))
    
    return(Year_behaviour, dummy_days)

def user_defined_inputs(country):
    '''
    Imports an input file and returns a processed User_list
    '''
    User_list = getattr((importlib.import_module('%s' %country)), 'User_list')
    return(User_list)

def Initialise_model(dummy_days):
    '''
    The model is ready to be initialised
    '''
    # Simulating n days before and after the wished number of profiles
    num_profiles_user = int(input("Please indicate the number of profiles to be generated: ")) #asks the user how many profiles (i.e. code runs) he wants
    num_profiles_sim = num_profiles_user + (2 * dummy_days)
    
    if num_profiles_user > 366:
        print('[CRITICAL] Number of profiles higher than days in the year, please provide a number lower than 366') 
        sys.exit()
    print('Please wait...') 
    
    Profile = [] #creates empty lists to store the results of each code run, i.e. each stochastically generated profile
    Usage = []
    Profile_user = []

    return (Profile, Usage, Profile_user, num_profiles_user, num_profiles_sim)
    
def Initialise_inputs(country, year):
    Year_behaviour, dummy_days = yearly_pattern(country, year)
    User_list = user_defined_inputs(country)
    (Profile, Usage, Profile_user, num_profiles_user, 
     num_profiles_sim) = Initialise_model(dummy_days)
    
    # Calibration parameters
    '''
    Calibration parameters. These can be changed in case the user has some real data against which the model can be calibrated
    They regulate the probabilities defining the largeness of the peak window and the probability of coincident switch-on within the peak window
    '''
    peak_enlarg = 0 #percentage random enlargement or reduction of peak time range length
    mu_peak = 0.5 #median value of gaussian distribution [0,1] by which the number of coincident switch_ons is randomly selected
    s_peak = 1 #standard deviation (as percentage of the median value) of the gaussian distribution [0,1] above mentioned
    
    return (peak_enlarg, mu_peak, s_peak, Year_behaviour, User_list, Profile, 
            Usage, Profile_user, num_profiles_user, num_profiles_sim, dummy_days)

def charge_prob(SOC):
    
    k = 15
    per_SOC = 0.5
    
    p = 1-1/(1+np.exp(-k*(SOC-per_SOC)))
       
    return p

def charge_prob_const(SOC):        
    
    p = 1       
    
    return p

def infrastructure_prob(minutes, t_park, infr_prob):
    
    window_1 = minutes.indexer_between_time('0:00', '6:00', include_start=True, include_end=False)
    window_2 = minutes.indexer_between_time('6:00', '19:00', include_start=True, include_end=False)
    window_3 = minutes.indexer_between_time('19:00', '0:00', include_start=True, include_end=False)
    
    p = np.piecewise(t_park, [t_park in  window_1, t_park in window_2, t_park in window_3], [90, 40, 90])
    p = p/100   
    
    return p

def infrastructure_prob_const(minutes, t_park, infr_prob):
    
    p = infr_prob   
    
    return p

def SOC_initial_f(SOC_max, SOC_min, SOC_initial):
    
    SOC_i = np.random.rand()*(SOC_max-SOC_min) + SOC_min
    
    return SOC_i

def SOC_initial_f_const(SOC_max, SOC_min, SOC_initial):
    
    SOC_i = SOC_initial
        
    return SOC_i

