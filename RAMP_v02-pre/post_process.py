# -*- coding: utf-8 -*-

#%% Import required libraries
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pytz
import copy
import matplotlib.ticker as mtick
from pathlib import Path
import pickle
from initialise import tot_users_calc, tot_battery_cap_calc
import datetime as dt
#import enlopy as el

#%% Post-processing
'''
Just some additional code lines to calculate useful indicators and generate plots
'''
def Profile_formatting(stoch_profiles):
    Profile_avg = np.zeros(1440)
    for pr in stoch_profiles:
        Profile_avg = Profile_avg + pr
    Profile_avg = Profile_avg/len(stoch_profiles)
    
    Profile_kW = []
    for kW in stoch_profiles: 
        Profile_kW.append(kW/1000)
    
    # Profile_series = np.array([])
    # for iii in stoch_profiles:
    #     Profile_series = np.append(Profile_series,iii)
    Profile_series = np.array([])
    Profile_series = np.hstack(stoch_profiles)

    return (Profile_avg, Profile_kW, Profile_series)

def Profiles_user_formatting(stoch_profiles):
    Profiles_user_format = {}
    for us_type in stoch_profiles[0]:
        Profiles_user_format[us_type] = []
        for day in range(len(stoch_profiles)):
            try:
                temp = np.stack(stoch_profiles[day][us_type], axis=-1)
            except:
                temp = np.zeros((1440,1))
            Profiles_user_format[us_type].append(temp)
        Profiles_user_format[us_type] = np.vstack(Profiles_user_format[us_type])
    return Profiles_user_format

def Usage_formatting(stoch_profiles):
    Usage_avg = np.zeros(1440)
    for pr in stoch_profiles:
        Usage_avg = Usage_avg + pr
    Usage_avg = Usage_avg/len(stoch_profiles)
      
    # Usage_series = np.array([])
    # for iii in stoch_profiles:
    #     Usage_series = np.append(Usage_series,iii)
    
    Usage_series = np.array([])
    Usage_series = np.hstack(stoch_profiles)

    return (Usage_avg, Usage_series)

def Profile_cloud_plot(stoch_profiles,stoch_profiles_avg):
    #x = np.arange(0,1440,5)
    plt.figure(figsize=(10,5))
    for n in stoch_profiles:
        plt.plot(np.arange(1440),n,'#b0c4de')
        plt.xlabel('Time [h])')
        plt.ylabel('Power [W]')
        plt.ylim(ymin=0)
        #plt.ylim(ymax=5000)
        plt.margins(x=0)
        plt.margins(y=0)
    plt.plot(np.arange(1440),stoch_profiles_avg,'#4169e1')
    plt.xticks([0,240,480,(60*12),(60*16),(60*20),(60*24)],[0,4,8,12,16,20,24])
    #plt.savefig('profiles.eps', format='eps', dpi=1000)
    plt.show()

def Profile_series_plot(stoch_profiles_series):
    #x = np.arange(0,1440,5)
    plt.figure(figsize=(10,5))
    plt.plot(np.arange(len(stoch_profiles_series)),stoch_profiles_series, '#4169e1')    #plt.xlabel('Time (hours)')
    plt.ylabel('Power (W)')
    plt.ylim(ymin=0)
    #plt.ylim(ymax=5000)
    plt.margins(x=0)
    plt.margins(y=0)
    #plt.xticks([0,240,480,(60*12),(60*16),(60*20),(60*24)],[0,4,8,12,16,20,24])
    #plt.savefig('profiles.eps', format='eps', dpi=1000)
    plt.show()

def Usage_series_plot(stoch_profiles_series):
    #x = np.arange(0,1440,5)
    plt.figure(figsize=(10,5))
    plt.plot(np.arange(len(stoch_profiles_series)),stoch_profiles_series)    #plt.xlabel('Time (hours)')
    plt.ylabel('Usage ')
    plt.ylim(ymin=0)
    #plt.ylim(ymax=5000)
    plt.margins(x=0)
    plt.margins(y=0)
    #plt.xticks([0,240,480,(60*12),(60*16),(60*20),(60*24)],[0,4,8,12,16,20,24])
    #plt.savefig('profiles.eps', format='eps', dpi=1000)
    plt.show()

def Profile_df_plot(Profile_df, year, country, start = '01-01 00:00:00', end = '12-31 23:59:00'):
    
    start_plot = str(year) + ' ' + start
    end_plot = str(year) + ' ' + end

    Profiles_df_plot = Profile_df[start_plot : end_plot]/1000   #Convert to kW
    
    figsize = (10,5)
    ax = Profiles_df_plot.plot(kind='line', color='blue', rot=0, fontsize=15, legend=False, figsize = figsize)
    ax.set_ylabel('Power [kW]', fontsize = 15)
    ax.set_title("Transport Demand Profile - " + country, fontsize = 15) 
    
    return ax

def Charging_Profile_df_plot(Profile_df, year, country, color = 'blue', start = '01-01 00:00:00', end = '12-31 23:59:00'):
    
    start_plot = str(year) + ' ' + start
    end_plot = str(year) + ' ' + end

    Profiles_df_plot = Profile_df[start_plot : end_plot]   
    
    figsize = (10,5)
    ax = Profiles_df_plot.plot(kind='line', color=color, rot=0, fontsize=15, legend=False, figsize = figsize)
    ax.set_ylabel('Power [kW]', fontsize = 15)
    ax.set_title("Charging Demand Profile - " + country, fontsize = 15) 
    
    return ax

def Comparison_plot(Profile_df, Charging_Profile_df, year, country, start = '01-01 00:00:00', end = '12-31 23:59:00'):
    
    start_plot = str(year) + ' ' + start
    end_plot = str(year) + ' ' + end

    Profiles_df_plot = Profile_df[start_plot : end_plot]/1000
    Charging_Profiles_df_plot = Charging_Profile_df[start_plot : end_plot]   

    figsize = (10,5)
    
    ax = Profiles_df_plot.plot(kind='line', color='royalblue', rot=0, fontsize=15, alpha = 0.7, legend=True, figsize = figsize)
    ax = Charging_Profiles_df_plot.plot(kind='line', color='orange', ax = ax, rot=0, fontsize=15, alpha = 0.7, legend=True, figsize = figsize)
    
    ax.set_ylabel('Power [kW]', fontsize = 15)
    ax.set_title("Comparison of Charging and Transport Profiles - " + country, fontsize = 15) 

    return ax

def Usage_df_plot(Usage_df, year, country, User_list, start = '01-01 00:00:00', end = '12-31 23:59:00'):
    
    tot_users = tot_users_calc(User_list)
    
    start_plot = str(year) + ' ' + start
    end_plot = str(year) + ' ' + end

    # Plot of the Usage in percentage of the total population
    Usage_df_plot = Usage_df[start_plot : end_plot]/10  #Divide by 10 because a value of 10 is assigned for each user to avoid the filter 

    figsize = (10,5)
    ax = ((Usage_df_plot/tot_users)*100).plot(kind='line', color= 'orange', rot=0, fontsize=15, legend=False, figsize = figsize)
    ax.set_ylabel('Usage [% of Total Users]', fontsize = 15)
    ax.set_title("Usage Profile - " + country, fontsize = 15)     
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))

    return ax

def Profile_dataframe(Profiles_series, year):
    
    minutes = pd.date_range(start=str(year) + '-01-01', periods = len(Profiles_series), freq='T')
    
    if Profiles_series.ndim == 1:
        Profiles_df = pd.DataFrame(Profiles_series, columns = ['Mobility Profile'])
    else: 
        Profiles_df = pd.DataFrame(Profiles_series)   
    
    Profiles_df.set_index(minutes, inplace = True)
   
    return Profiles_df

def Charging_Profile_dataframe(Profiles_series, year):
    
    minutes = pd.date_range(start=str(year) + '-01-01', periods = len(Profiles_series), freq='T')
    
    if Profiles_series.ndim == 1:
        Profiles_df = pd.DataFrame(Profiles_series, columns = ['Charging Profile'])
    else: 
        Profiles_df = pd.DataFrame(Profiles_series)   
    
    Profiles_df.set_index(minutes, inplace = True)
   
    return Profiles_df

def AF_dataframe(Profiles_series, year):
    
    minutes = pd.date_range(start=str(year) + '-01-01', periods = len(Profiles_series), freq='T')
    
    if Profiles_series.ndim == 1:
        Profiles_df = pd.DataFrame(Profiles_series, columns = ['Availability Factor'])
    else: 
        Profiles_df = pd.DataFrame(Profiles_series)   
    
    Profiles_df.set_index(minutes, inplace = True)
   
    return Profiles_df

def Profile_user_dataframe(Profiles_user, year):
    
    minutes = pd.date_range(start=str(year) + '-01-01', periods = len(Profiles_user[list(Profiles_user.keys())[0]]), freq='T')
    
    Profiles_user_df = {}
    
    for us_type in Profiles_user.keys():
        Profiles_user_df[us_type] = pd.DataFrame(Profiles_user[us_type])
        Profiles_user_df[us_type].set_index(minutes, inplace = True)
       
    return Profiles_user_df

def Usage_dataframe(Profiles_series, year):
    
    minutes = pd.date_range(start=str(year) + '-01-01', periods = len(Profiles_series), freq='min')
    
    Profiles_df = pd.DataFrame(Profiles_series, columns = ['Usage'])
    Profiles_df.set_index(minutes, inplace = True)
   
    return Profiles_df

def temp_import(country, year, inputfile_temp = r"Input_data\temp.csv"):
      
    temp_profile = pd.read_csv(inputfile_temp, index_col = 0)
    temp_profile = pd.DataFrame(temp_profile[country]) 
    temp_profile = temp_profile.loc[temp_profile.index.str.contains(str(year)+ '|' + str(year-1)+ '|' + str(year+1))]

    hours = pd.period_range(start=str(year-1) + '-01-01', end=str(year+1) + '-12-31 23:00', freq='H')
    temp_profile.set_index(hours, inplace = True)
    
    temp_profile = temp_profile.resample('T', closed='right').pad()
    
    return temp_profile

def Profile_temp(Profiles_df, temp_profile,  year = 2016):

    Profiles_df_c = copy.deepcopy(Profiles_df)

    minutes = pd.date_range(start=str(year-1) + '-01-01', end=str(year+1) + '-12-31 23:59:00', freq='T', tz = 'UTC')
    temp_profile.set_index(minutes, inplace = True)
            
    temp_profile = temp_profile.loc[Profiles_df_c.index]
    
    temp_coeff = pd.DataFrame(1, index = Profiles_df_c.index, columns = temp_profile.columns)
    
    temp_coeff[temp_profile < 15] = 1.12 - 0.01*temp_profile[temp_profile < 15]
    temp_coeff[temp_profile > 20] = 0.63 + 0.02*temp_profile[temp_profile > 20]
    
    Profiles_temp = Profiles_df_c * temp_coeff.values
    
    return Profiles_temp

def Profile_temp_users(Profiles_user, temp_profile,  year = 2016, dummy_days = 1):

    start_day = dt.datetime(year, 1, 1) - dt.timedelta(days=dummy_days)
    n_periods = len(Profiles_user['Working - Large car'])
    
    minutes_sim = pd.date_range(start=start_day, periods = n_periods, freq='T')
        
    minutes = pd.date_range(start=str(year-1) + '-01-01', end=str(year+1) + '-12-31 23:59:00', freq='T')

    temp_profile.set_index(minutes, inplace = True)
            
    temp_profile = temp_profile.loc[minutes_sim]
    
    temp_coeff = pd.DataFrame(1, index = temp_profile.index, columns = temp_profile.columns)
    
    temp_coeff[temp_profile < 15] = 1.12 - 0.01*temp_profile[temp_profile < 15]
    temp_coeff[temp_profile > 20] = 0.63 + 0.02*temp_profile[temp_profile > 20]
    
    Profiles_user_temp = {}
    
    for user in Profiles_user: 
        Profiles_user_temp[user] = Profiles_user[user] * temp_coeff.values
            
    return Profiles_user_temp

def Time_correction(df, country, year):
    
    df_c = copy.deepcopy(df)   
    
    ind = df_c.index.tz_localize(pytz.country_timezones[country][0], nonexistent = 'NaT', ambiguous='NaT')
    ind_filter = ind[~ ind.isnull()]
        
    idx = pd.date_range(start=min(ind_filter), end=max(ind_filter), freq = ind.to_series().diff().min())
    df_c = df_c.set_index(idx)
    
    ind_utc = ind.tz_convert('utc')
    temp_utc = df_c.set_index(ind_utc)
    
    ind_year = pd.date_range(start=str(year) + '-01-01', end=str(max(temp_utc.index).date()) + ' 23:59:00', freq = ind.to_series().diff().min(), tz = 'utc')
    temp_year = pd.DataFrame([np.nan] * len(ind_year), index = ind_year)
    
    df_utc_final = temp_utc.join(temp_year, how='outer')
    df_utc_final = df_utc_final.dropna(axis=1, how='all')
    df_utc_final = df_utc_final.loc[df_utc_final.index.notnull()]
    df_utc_final = df_utc_final.ffill()
    df_utc_final = df_utc_final[df_utc_final.index >= str(year) + '-01-01']
    
    df_utc_final = pd.DataFrame(df_utc_final)
    
    return df_utc_final

def Resample(df):
    
    df = df.resample('H').mean()
    
    return df

def Charging_user_formatting(Ch_dict, dummy_days):
    
    Charging_dict = {}
    dummy_minutes = dummy_days * 1440
    
    for key in Ch_dict:
        Charging_dict[key] = np.transpose(np.vstack(Ch_dict[key]))
        Charging_dict[key] = Charging_dict[key][dummy_minutes:-dummy_minutes, :]
    
    return Charging_dict
    
def Availability_factors(en_system, User_list, security_margin = 0.5):
    
    tot_Battery_cap_min = tot_battery_cap_calc(User_list) * 60 
    
    AF = (en_system * security_margin) / tot_Battery_cap_min
    
    return AF

#%% Export individual profiles
'''
for i in range (len(Profile)):
    np.save('p0%d.npy' % (i), Profile[i])
'''

# Export Profiles

def export_csv(filename, variable, inputfile, simulation_name):
    
    if simulation_name:
        simulation = f'/{simulation_name}/'
    else:
        simulation = '/'
        
    folder = f'results/{inputfile}' + simulation 
    Path(folder).mkdir(parents=True, exist_ok=True) 
    variable.to_csv(f'{folder}{filename}.csv')
    
def export_pickle(filename, variable, inputfile, simulation_name):
    
    if simulation_name:
        simulation = f'/{simulation_name}/'
    else:
        simulation = '/'

    folder = f'results/{inputfile}' + simulation  
    Path(folder).mkdir(parents=True, exist_ok=True) 

    file = open(f'{folder}{filename}.pkl','wb')
    pickle.dump(variable, file, protocol=4)
    file.close()
    
 
# Read pkl Variable 
# file = open(r"C:\Users\Andrea\OneDrive - Politecnico di Milano\Università\Tesi (OneDrive)\Article PROres1 coupling\Simulations and results\TIMES_ProRes_2050_EVFLEX_new\EVFLEX_new.pkl", 'rb')
# inputs_EV = pickle.load(file)
# results_EV = pickle.load(file)
# file.close()
