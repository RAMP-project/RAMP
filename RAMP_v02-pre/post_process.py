# -*- coding: utf-8 -*-

#%% Import required libraries
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pytz
import copy

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
    
    Profile_series = np.array([])
    for iii in stoch_profiles:
        Profile_series = np.append(Profile_series,iii)
    
    return (Profile_avg, Profile_kW, Profile_series)

def Usage_formatting(stoch_profiles):
    Usage_avg = np.zeros(1440)
    for pr in stoch_profiles:
        Usage_avg = Usage_avg + pr
    Usage_avg = Usage_avg/len(stoch_profiles)
      
    Usage_series = np.array([])
    for iii in stoch_profiles:
        Usage_series = np.append(Usage_series,iii)
    
    return (Usage_avg, Usage_series)

def Profile_cloud_plot(stoch_profiles,stoch_profiles_avg):
    #x = np.arange(0,1440,5)
    plt.figure(figsize=(10,5))
    for n in stoch_profiles:
        plt.plot(np.arange(1440),n,'#b0c4de')
        plt.xlabel('Time (hours)')
        plt.ylabel('Power (W)')
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

def Profile_usage_plot(stoch_profiles_series):
    #x = np.arange(0,1440,5)
    plt.figure(figsize=(10,5))
    plt.plot(np.arange(len(stoch_profiles_series)),stoch_profiles_series)    #plt.xlabel('Time (hours)')
    plt.ylabel('Usage')
    plt.ylim(ymin=0)
    #plt.ylim(ymax=5000)
    plt.margins(x=0)
    plt.margins(y=0)
    #plt.xticks([0,240,480,(60*12),(60*16),(60*20),(60*24)],[0,4,8,12,16,20,24])
    #plt.savefig('profiles.eps', format='eps', dpi=1000)
    plt.show()

def Profile_dataframe(Profiles_series, year):
    
    minutes = pd.DataFrame(pd.date_range(start=str(year) + '-01-01', periods = len(Profiles_series), freq='min'))
    
    Profiles_df = pd.DataFrame(Profiles_series, columns = ['Load Profile'])
    Profiles_df.set_index(minutes.iloc[:,0], inplace = True)
   
    return Profiles_df

def Usage_dataframe(Profiles_series, year):
    
    minutes = pd.DataFrame(pd.date_range(start=str(year) + '-01-01', periods = len(Profiles_series), freq='min'))
    
    Profiles_df = pd.DataFrame(Profiles_series, columns = ['Usage'])
    Profiles_df.set_index(minutes.iloc[:,0], inplace = True)
   
    return Profiles_df

def temp_import(country, year, inputfile = r"TimeSeries\temp.csv"):
      
    temp_profile = pd.read_csv(inputfile, index_col = 0)
    temp_profile = pd.DataFrame(temp_profile[country]) 
    temp_profile = temp_profile.loc[temp_profile.index.str.contains(str(year))]

    return temp_profile

def Profile_temp(Profiles_df, temp_profile,  year = 2016):
    
    hours = pd.date_range(start=str(year) + '-01-01', end=str(year) + '-12-31 23:00:00', freq='H')
    temp_profile.set_index(hours, inplace = True)
    
    Profiles_df_c = copy.deepcopy(Profiles_df)
    
    Profiles_df_hour = Profiles_df_c.resample('H').sum()
    
    temp_profile = temp_profile.loc[Profiles_df_hour.index]
    
    temp_coeff = pd.DataFrame(1, index = Profiles_df_hour.index, columns = temp_profile.columns)
    
    temp_coeff[temp_profile < 15] = 1.12 - 0.01*temp_profile[temp_profile < 15]
    temp_coeff[temp_profile > 20] = 0.63 + 0.02*temp_profile[temp_profile > 20]
    
    Profiles_temp = Profiles_df_hour * temp_coeff.values
    
    return Profiles_temp

# def localize(df, country, ambiguous=None):

#     # The exceptions below correct for daylight saving time
#     try:
#         df.index = df.index.tz_localize(pytz.country_timezones[country][0], ambiguous=ambiguous)
#         return df

#     # Delete values that do not exist because of daylight saving time
#     except pytz.NonExistentTimeError as err:
#         return localize(df.loc[df.index != err.args[0], ], country)

#     # Duplicate values that exist twice because of daylight saving time
#     except pytz.AmbiguousTimeError as err:
#         b = err
#         return b
#         # idx = pd.Timestamp(err.args[0].split("'")[1])
#         # unambiguous_df = localize(df.loc[df.index != idx, ], country)
#         # ambiguous_df = localize(df.loc[[idx, idx], ], country, ambiguous=[True, False])
#         # return unambiguous_df.append(ambiguous_df).sort_index()

def Time_correction(df, country, year):

    df_c = copy.deepcopy(df)   
    
    ind = df_c.index.tz_localize(pytz.country_timezones[country][0], nonexistent = 'NaT', ambiguous='NaT')
    ind_filter = ind[~ ind.isnull()]
        
    idx = pd.date_range(start=min(ind_filter), end=max(ind_filter), freq='H')
    df_c = df_c.set_index(idx)
    
    ind_utc = ind.tz_convert('utc')
    temp_utc = df_c.set_index(ind_utc)
    
    ind_year = pd.date_range(start=str(year) + '-01-01', end=str(max(temp_utc.index).date()) + ' 23:00:00', freq='H', tz = 'utc')
    temp_year = pd.DataFrame([np.nan] * len(ind_year), index = ind_year)
    
    df_utc_final = pd.concat([temp_utc, temp_year], axis=1, sort=False)
    df_utc_final = df_utc_final.iloc[:,0]
    df_utc_final = df_utc_final.loc[df_utc_final.index.notnull()]
    df_utc_final = df_utc_final.ffill()
    df_utc_final = df_utc_final[df_utc_final.index >= str(year) + '-01-01']
    
    df_utc_final = pd.DataFrame(df_utc_final)
    
    return df_utc_final

#%% Export individual profiles
'''
for i in range (len(Profile)):
    np.save('p0%d.npy' % (i), Profile[i])
'''

# Export Profiles

def export_series(filename, variable, country):
    variable.to_csv('results/%s_%s.csv' % (filename, country))