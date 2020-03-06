# -*- coding: utf-8 -*-

#%% Definition of the inputs
'''
Input data definition 
'''

from core import User, np, pd, copy
User_list = []

'''Common values used in the input data definition'''

#Define Country
country = 'IT'

#Total number of users to be simulated
tot_users = 50

#Variabilities 
r_w = {}

P_var = 0.1 #random in power
r_d   = 0.3 #random in distance
r_v   = 0.3 #random in velocity

#Variabilites in functioning windows 
r_w['working'] = 0.25
r_w['student'] = 0.33
r_w['inactive'] = 0.1
r_w['free time'] = 0.2

#Occasional use 
occasional_use = {}

occasional_use['weekday'] = 1
occasional_use['saturday'] = 0.6
occasional_use['sunday'] = 0.5
occasional_use['free time'] = {'weekday': 0.1, 'weekend': 0.4}

#%% Files with the inputs to be loaded 

#Composition of the population by percentage share
pop_file =  r"TimeSeries\pop_share.csv" 
pop_data = pd.read_csv(pop_file, header = 0, index_col = 0)

#Share of the type of vehicles in the country
vehicle_file =  r"TimeSeries\vehicle_share.csv" 
vehicle_data = pd.read_csv(vehicle_file, header = 0, index_col = 0)

# Total daily distance 
d_tot_file =  r"TimeSeries\d_tot.csv" 
d_tot_data = pd.read_csv(d_tot_file, header = 0, index_col = 0)

# Distance by trip
d_min_file =  r"TimeSeries\d_min.csv" 
d_min_data = pd.read_csv(d_min_file, header = 0, index_col = [0,1])

# Functioning time by trip [min]
t_func_file =  r"TimeSeries\t_func.csv" 
t_func_data = pd.read_csv(t_func_file, header = 0, index_col = [0,1])

# Functioning windows 
window_file =  r"TimeSeries\windows.csv" 
window_data = pd.read_csv(window_file, header = [0,1], index_col = [0,1,2])
window_data = window_data*60

#Trips distribution by time 
trips = {}
for day in ['weekday', 'saturday', 'sunday']:    
    file =  r"TimeSeries\Trips by time_%s.csv" %day
    trips[day] = pd.read_csv(file, header = 0)
    trips[day] = trips[day][country]/100

#%%

#Composition of the population by percentage share
pop_sh = {}

pop_sh['working']   = pop_data.loc[country, 'Working']
pop_sh['student']   = pop_data.loc[country, 'Student']
pop_sh['inactive']  = pop_data.loc[country, 'Inactive']

#Share of the type of vehicles in the country
vehicle_sh = {}

vehicle_sh['small']  = vehicle_data.loc[country, 'small']
vehicle_sh['medium'] = vehicle_data.loc[country, 'medium']
vehicle_sh['large']  = vehicle_data.loc[country, 'large']

#Maximum power of the vehicle by type [kW]
Pmax_EV = {}

Pmax_EV['small']  = 61
Pmax_EV['medium'] = 150
Pmax_EV['large']  = 350

# Total daily distance 
d_tot = {}

d_tot['weekday']  = d_tot_data.loc[country, 'Weekday']
d_tot['saturday'] = d_tot_data.loc[country, 'Weekend']
d_tot['sunday']   = d_tot_data.loc[country, 'Weekend']

# Distance by trip
d_min = {}

d_min['weekday']  = {'business': d_min_data[country]['Business']['Weekday'], 
                     'personal': d_min_data[country]['Personal']['Weekday']}
d_min['saturday'] = {'business': d_min_data[country]['Business']['Saturday'],
                     'personal': d_min_data[country]['Personal']['Saturday']} 
d_min['sunday']   = {'business': d_min_data[country]['Business']['Sunday'],
                     'personal': d_min_data[country]['Personal']['Sunday']} 

d_min['weekday']['mean']  = int(np.array([d_min['weekday'][k] for k in d_min['weekday']]).mean())
d_min['saturday']['mean'] = int(np.array([d_min['saturday'][k] for k in d_min['saturday']]).mean())
d_min['sunday']['mean']   = int(np.array([d_min['sunday'][k] for k in d_min['sunday']]).mean())

# Functioning time by trip [min]
t_func = {}

t_func['weekday']  = {'business': t_func_data[country]['Business']['Weekday'],  
                      'personal': t_func_data[country]['Personal']['Weekday']}
t_func['saturday'] = {'business': t_func_data[country]['Business']['Saturday'], 
                      'personal': t_func_data[country]['Personal']['Saturday']} 
t_func['sunday']   = {'business': t_func_data[country]['Business']['Sunday'], 
                      'personal': t_func_data[country]['Personal']['Sunday']} 

t_func['weekday']['mean']  = int(np.array([t_func['weekday'][k] for k in t_func['weekday']]).mean())
t_func['saturday']['mean'] = int(np.array([t_func['saturday'][k] for k in t_func['saturday']]).mean())
t_func['sunday']['mean']   = int(np.array([t_func['sunday'][k] for k in t_func['sunday']]).mean())

# Functioning windows 
if country in window_data.columns.get_level_values(0):
    window = {}
    
    window['working']   = {'main':      [[window_data[country]['Start']['Working']['Main'][1],       window_data[country]['End']['Working']['Main'][1]],  
                                         [window_data[country]['Start']['Working']['Main'][2],       window_data[country]['End']['Working']['Main'][2]]], 
                           'free time': [[window_data[country]['Start']['Working']['Free time'][1],  window_data[country]['End']['Working']['Free time'][1]],   
                                         [window_data[country]['Start']['Working']['Free time'][2],  window_data[country]['End']['Working']['Free time'][2]], 
                                         [window_data[country]['Start']['Working']['Free time'][3],  window_data[country]['End']['Working']['Free time'][3]]]}
    window['student']   = {'main':      [[window_data[country]['Start']['Student']['Main'][1],       window_data[country]['End']['Student']['Main'][1]],  
                                         [window_data[country]['Start']['Student']['Main'][2],       window_data[country]['End']['Student']['Main'][2]], 
                                         [window_data[country]['Start']['Student']['Main'][3],       window_data[country]['End']['Student']['Main'][3]]], 
                           'free time': [[window_data[country]['Start']['Student']['Free time'][1],  window_data[country]['End']['Student']['Free time'][1]],    
                                         [window_data[country]['Start']['Student']['Free time'][2],  window_data[country]['End']['Student']['Free time'][2]]]}
    window['inactive']  = {'main':      [[window_data[country]['Start']['Inactive']['Main'][1],      window_data[country]['End']['Inactive']['Main'][1]]], 
                           'free time': [[window_data[country]['Start']['Inactive']['Free time'][1], window_data[country]['End']['Inactive']['Free time'][1]],   
                                         [window_data[country]['Start']['Inactive']['Free time'][2], window_data[country]['End']['Inactive']['Free time'][2]]]}
else: 
    print('\n[WARNING] There are no specific functioning windows defined for the selected country, standard windows will be used. \nEdit the "windows.csv" file to add specific functioning windows')
    
    window = {}
    w_type = 'Standard'
    
    window['working']   = {'main':      [[window_data[w_type]['Start']['Working']['Main'][1],       window_data[w_type]['End']['Working']['Main'][1]],  
                                         [window_data[w_type]['Start']['Working']['Main'][2],       window_data[w_type]['End']['Working']['Main'][2]]], 
                           'free time': [[window_data[w_type]['Start']['Working']['Free time'][1],  window_data[w_type]['End']['Working']['Free time'][1]],   
                                         [window_data[w_type]['Start']['Working']['Free time'][2],  window_data[w_type]['End']['Working']['Free time'][2]], 
                                         [window_data[w_type]['Start']['Working']['Free time'][3],  window_data[w_type]['End']['Working']['Free time'][3]]]}
    window['student']   = {'main':      [[window_data[w_type]['Start']['Student']['Main'][1],       window_data[w_type]['End']['Student']['Main'][1]],  
                                         [window_data[w_type]['Start']['Student']['Main'][2],       window_data[w_type]['End']['Student']['Main'][2]], 
                                         [window_data[w_type]['Start']['Student']['Main'][3],       window_data[w_type]['End']['Student']['Main'][3]]], 
                           'free time': [[window_data[w_type]['Start']['Student']['Free time'][1],  window_data[w_type]['End']['Student']['Free time'][1]],    
                                         [window_data[w_type]['Start']['Student']['Free time'][2],  window_data[w_type]['End']['Student']['Free time'][2]]]}
    window['inactive']  = {'main':      [[window_data[w_type]['Start']['Inactive']['Main'][1],      window_data[w_type]['End']['Inactive']['Main'][1]]], 
                           'free time': [[window_data[w_type]['Start']['Inactive']['Free time'][1], window_data[w_type]['End']['Inactive']['Free time'][1]],   
                                         [window_data[w_type]['Start']['Inactive']['Free time'][2], window_data[w_type]['End']['Inactive']['Free time'][2]]]}

#Re-format functioning windows to calculare the Percentage of travels in functioning windows 
wind_temp = copy.deepcopy(window)
for key in wind_temp.keys():
    for act in ['main', 'free time']:
        wind_temp[key][act] = [item for sublist in window[key][act] for item in sublist]
        wind_temp[key][act] = [int(x / 60) for x in wind_temp[key][act]]

#Percentage of travels in functioning windows 

#main and free time is defined according to the functioning windows
#If the windows are modified, also the perentages should be modified accordingly
perc_usage = {}

perc_usage['weekday']  = {'working' :{'main': trips['weekday'].iloc[np.r_[wind_temp['working']['main'][0]:wind_temp['working']['main'][1], wind_temp['working']['main'][2]:wind_temp['working']['main'][3]]].sum()},
                          'student' :{'main': trips['weekday'].iloc[np.r_[wind_temp['student']['main'][0]:wind_temp['student']['main'][1], wind_temp['student']['main'][2]:wind_temp['student']['main'][3], wind_temp['student']['main'][4]:wind_temp['student']['main'][5]]].sum()}, 
                          'inactive':{'main': trips['weekday'].iloc[np.r_[wind_temp['inactive']['main'][0]:wind_temp['inactive']['main'][1]]].sum()}}
perc_usage['saturday'] = {'working' :{'main': trips['saturday'].iloc[np.r_[wind_temp['working']['main'][0]:wind_temp['working']['main'][1], wind_temp['working']['main'][2]:wind_temp['working']['main'][3]]].sum()},
                          'student' :{'main': trips['saturday'].iloc[np.r_[wind_temp['student']['main'][0]:wind_temp['student']['main'][1], wind_temp['student']['main'][2]:wind_temp['student']['main'][3], wind_temp['student']['main'][4]:wind_temp['student']['main'][5]]].sum()}, 
                          'inactive':{'main': trips['saturday'].iloc[np.r_[wind_temp['inactive']['main'][0]:wind_temp['inactive']['main'][1]]].sum()}}
perc_usage['sunday']   = {'working' :{'main': trips['saturday'].iloc[np.r_[wind_temp['working']['main'][0]:wind_temp['working']['main'][1], wind_temp['working']['main'][2]:wind_temp['working']['main'][3]]].sum()},
                          'student' :{'main': trips['saturday'].iloc[np.r_[wind_temp['student']['main'][0]:wind_temp['student']['main'][1], wind_temp['student']['main'][2]:wind_temp['student']['main'][3], wind_temp['student']['main'][4]:wind_temp['student']['main'][5]]].sum()}, 
                          'inactive':{'main': trips['saturday'].iloc[np.r_[wind_temp['inactive']['main'][0]:wind_temp['inactive']['main'][1]]].sum()}}

#Calulate the Percentage of travels in functioning windows for free time
#as complementary to the main time 
for key in perc_usage.keys():
    for us_type in ['working', 'student', 'inactive']:
        perc_usage[key][us_type]['free time'] = 1 - perc_usage[key][us_type]['main']

#%% Definition of Users 
'''
Users
'''

#Create new user classes

### Working ###

Working_L = User(name = "Working - Large car", us_pref = 0,
                 n_users = int(tot_users*pop_sh['working']*vehicle_sh['large']))
User_list.append(Working_L)

Working_M = User(name = "Working - Medium car", us_pref = 0,
                  n_users = int(tot_users*pop_sh['working']*vehicle_sh['medium']))
User_list.append(Working_M)

Working_S = User(name = "Working - Small car", us_pref = 0,
                  n_users = int(tot_users*pop_sh['working']*vehicle_sh['small']))
User_list.append(Working_S)

### Student ###

Student_L = User(name = "Student - Large car", us_pref = 0,
                  n_users = int(tot_users*pop_sh['student']*vehicle_sh['large']))
User_list.append(Student_L)

Student_M = User(name = "Student - Medium car", us_pref = 0,
                  n_users = int(tot_users*pop_sh['student']*vehicle_sh['medium']))
User_list.append(Student_M)

Student_S = User(name = "Student - Small car", us_pref = 0,
                  n_users = int(tot_users*pop_sh['student']*vehicle_sh['small']))
User_list.append(Student_M)

### Inactive ###

Inactive_L = User(name = "Inactive - Large car", us_pref = 0,
                  n_users = int(tot_users*pop_sh['inactive']*vehicle_sh['large']))
User_list.append(Inactive_L)

Inactive_M = User(name = "Inactive - Medium car", us_pref = 0,
                  n_users = int(tot_users*pop_sh['inactive']*vehicle_sh['medium']))
User_list.append(Inactive_M)

Inactive_S = User(name = "Inactive - Small car", us_pref = 0,
                  n_users = int(tot_users*pop_sh['inactive']*vehicle_sh['small']))
User_list.append(Inactive_S)

#%% Definition of Appliances
'''
Appliances
'''

#%% Working 

### Large Car ###

# Working - Large Car - Weekday
Working_EV_large_wd = Working_L.Appliance(Working_L, n = 1, P_max = Pmax_EV['large'], P_var = P_var, w = 2, d_tot = d_tot['weekday']*perc_usage['weekday']['working']['main'], r_d = r_d, t_func = t_func['weekday']['business'], r_v = r_v, d_min = d_min['weekday']['business'], fixed = 'no', fixed_cycle = 0, occasional_use = occasional_use['weekday'], flat = 'no', pref_index = 0, wd_we_type = 0, P_series = False)
Working_EV_large_wd.windows(w1 = window['working']['main'][0], w2 = window['working']['main'][1], r_w = r_w['working'])

# Working - Large Car - Weekday - Free Time
Working_EV_large_wd_ft = Working_L.Appliance(Working_L, n = 1, P_max = Pmax_EV['large'], P_var = P_var, w = 3, d_tot = d_tot['weekday']*perc_usage['weekday']['working']['free time'], r_d = r_d, t_func = t_func['weekday']['personal'], r_v = r_v, d_min = d_min['weekday']['personal'], fixed = 'no', fixed_cycle = 0, occasional_use = occasional_use['free time']['weekday'], flat = 'no', pref_index = 0, wd_we_type = 0, P_series = False)
Working_EV_large_wd_ft.windows(w1 = window['working']['free time'][0], w2 = window['working']['free time'][1], w3 = window['working']['free time'][2], r_w = r_w['free time'])

# Working - Large Car - Saturday
Working_EV_large_sat = Working_L.Appliance(Working_L, n = 1, P_max = Pmax_EV['large'], P_var = P_var, w = 1, d_tot = d_tot['saturday']*perc_usage['saturday']['inactive']['main'], r_d = r_d, t_func = t_func['saturday']['business'], r_v = r_v, d_min = d_min['saturday']['business'], fixed = 'no', fixed_cycle = 0, occasional_use = occasional_use['saturday'], flat = 'no', pref_index = 0, wd_we_type = 1, P_series = False)
Working_EV_large_sat.windows(w1 = window['inactive']['main'][0],  r_w = r_w['inactive'])

# Working - Large Car - Saturday - Free Time
Working_EV_large_sat_ft = Working_L.Appliance(Working_L, n = 1, P_max = Pmax_EV['large'], P_var = P_var, w = 2, d_tot = d_tot['saturday']*perc_usage['saturday']['inactive']['free time'], r_d = r_d, t_func = t_func['saturday']['personal'], r_v = r_v, d_min = d_min['saturday']['personal'], fixed = 'no', fixed_cycle = 0, occasional_use = occasional_use['free time']['weekend'], flat = 'no', pref_index = 0, wd_we_type = 1, P_series = False)
Working_EV_large_sat_ft.windows(w1 = window['inactive']['free time'][0], w2 = window['inactive']['free time'][1], r_w = r_w['free time'])

# Working - Large Car - Sunday
Working_EV_large_sun = Working_L.Appliance(Working_L, n = 1, P_max = Pmax_EV['large'], P_var = P_var, w = 1, d_tot = d_tot['sunday']*perc_usage['sunday']['inactive']['main'], r_d = r_d, t_func = t_func['sunday']['business'], r_v = r_v, d_min = d_min['sunday']['business'], fixed = 'no', fixed_cycle = 0, occasional_use = occasional_use['sunday'], flat = 'no', pref_index = 0, wd_we_type = 2, P_series = False)
Working_EV_large_sun.windows(w1 = window['inactive']['main'][0], r_w = r_w['inactive'])

# Working - Large Car - Sunday - Free Time
Working_EV_large_sun_ft = Working_L.Appliance(Working_L, n = 1, P_max = Pmax_EV['large'], P_var = P_var, w = 2, d_tot = d_tot['sunday']*perc_usage['sunday']['inactive']['free time'], r_d = r_d, t_func = t_func['sunday']['personal'], r_v = r_v, d_min = d_min['sunday']['personal'], fixed = 'no', fixed_cycle = 0, occasional_use = occasional_use['free time']['weekend'], flat = 'no', pref_index = 0, wd_we_type = 2, P_series = False)
Working_EV_large_sun_ft.windows(w1 = window['inactive']['free time'][0], w2 = window['inactive']['free time'][1], r_w = r_w['free time'])

### Medium Car ###

# Working - Medium Car - Weekday
Working_EV_medium_wd = Working_M.Appliance(Working_M, n = 1, P_max = Pmax_EV['medium'], P_var = P_var, w = 2, d_tot = d_tot['weekday']*perc_usage['weekday']['working']['main'], r_d = r_d, t_func = t_func['weekday']['business'], r_v = r_v, d_min = d_min['weekday']['business'], fixed = 'no', fixed_cycle = 0, occasional_use = occasional_use['weekday'], flat = 'no', pref_index = 0, wd_we_type = 0, P_series = False)
Working_EV_medium_wd.windows(w1 = window['working']['main'][0], w2 = window['working']['main'][1], r_w = r_w['working'])

# Working - Medium Car - Weekday - Free Time
Working_EV_medium_wd_ft = Working_M.Appliance(Working_M, n = 1, P_max = Pmax_EV['medium'], P_var = P_var, w = 3, d_tot = d_tot['weekday']*perc_usage['weekday']['working']['free time'], r_d = r_d, t_func = t_func['weekday']['personal'], r_v = r_v, d_min = d_min['weekday']['personal'], fixed = 'no', fixed_cycle = 0, occasional_use = occasional_use['free time']['weekday'], flat = 'no', pref_index = 0, wd_we_type = 0, P_series = False)
Working_EV_medium_wd_ft.windows(w1 = window['working']['free time'][0], w2 = window['working']['free time'][1], w3 = window['working']['free time'][2], r_w = r_w['free time'])

# Working - Medium Car - Saturday
Working_EV_medium_sat = Working_M.Appliance(Working_M, n = 1, P_max = Pmax_EV['medium'], P_var = P_var, w = 1, d_tot = d_tot['saturday']*perc_usage['saturday']['inactive']['main'], r_d = r_d, t_func = t_func['saturday']['business'], r_v = r_v, d_min = d_min['saturday']['business'], fixed = 'no', fixed_cycle = 0, occasional_use = occasional_use['saturday'], flat = 'no', pref_index = 0, wd_we_type = 1, P_series = False)
Working_EV_medium_sat.windows(w1 = window['inactive']['main'][0], r_w = r_w['inactive'])

# Working - Medium Car - Saturday - Free Time
Working_EV_medium_sat_ft = Working_M.Appliance(Working_M, n = 1, P_max = Pmax_EV['medium'], P_var = P_var, w = 2, d_tot = d_tot['saturday']*perc_usage['saturday']['inactive']['free time'], r_d = r_d, t_func = t_func['saturday']['personal'], r_v = r_v, d_min = d_min['saturday']['personal'], fixed = 'no', fixed_cycle = 0, occasional_use = occasional_use['free time']['weekend'], flat = 'no', pref_index = 0, wd_we_type = 1, P_series = False)
Working_EV_medium_sat_ft.windows(w1 = window['inactive']['free time'][0], w2 = window['inactive']['free time'][1], r_w = r_w['free time'])

# Working - Medium Car - Sunday
Working_EV_medium_sun = Working_M.Appliance(Working_M, n = 1, P_max = Pmax_EV['medium'], P_var = P_var, w = 1, d_tot = d_tot['sunday']*perc_usage['sunday']['inactive']['main'], r_d = r_d, t_func = t_func['sunday']['business'], r_v = r_v, d_min = d_min['sunday']['business'], fixed = 'no', fixed_cycle = 0, occasional_use = occasional_use['sunday'], flat = 'no', pref_index = 0, wd_we_type = 2, P_series = False)
Working_EV_medium_sun.windows(w1 = window['inactive']['main'][0], r_w = r_w['inactive'])

# Working - Medium Car - Sunday - Free Time
Working_EV_medium_sun_ft = Working_M.Appliance(Working_M, n = 1, P_max = Pmax_EV['medium'], P_var = P_var, w = 2, d_tot = d_tot['sunday']*perc_usage['sunday']['inactive']['free time'], r_d = r_d, t_func = t_func['sunday']['personal'], r_v = r_v, d_min = d_min['sunday']['personal'], fixed = 'no', fixed_cycle = 0, occasional_use = occasional_use['free time']['weekend'], flat = 'no', pref_index = 0, wd_we_type = 2, P_series = False)
Working_EV_medium_sun_ft.windows(w1 = window['inactive']['free time'][0], w2 = window['inactive']['free time'][1], r_w = r_w['free time'])

### Small Car ###

# Working - Small Car - Weekday
Working_EV_small_wd = Working_S.Appliance(Working_S, n = 1, P_max = Pmax_EV['small'], P_var = P_var, w = 2, d_tot = d_tot['weekday']*perc_usage['weekday']['working']['main'], r_d = r_d, t_func = t_func['weekday']['business'], r_v = r_v, d_min = d_min['weekday']['business'], fixed = 'no', fixed_cycle = 0, occasional_use = occasional_use['weekday'], flat = 'no', pref_index = 0, wd_we_type = 0, P_series = False)
Working_EV_small_wd.windows(w1 = window['working']['main'][0], w2 = window['working']['main'][1], r_w = r_w['working'])

# Working - Small Car - Weekday - Free Time
Working_EV_small_wd_ft = Working_S.Appliance(Working_S, n = 1, P_max = Pmax_EV['small'], P_var = P_var, w = 3, d_tot = d_tot['weekday']*perc_usage['weekday']['working']['free time'], r_d = r_d, t_func = t_func['weekday']['personal'], r_v = r_v, d_min = d_min['weekday']['personal'], fixed = 'no', fixed_cycle = 0, occasional_use = occasional_use['free time']['weekday'], flat = 'no', pref_index = 0, wd_we_type = 0, P_series = False)
Working_EV_small_wd_ft.windows(w1 = window['working']['free time'][0], w2 = window['working']['free time'][1], w3 = window['working']['free time'][2], r_w = r_w['free time'])

# Working - Small Car - Saturday
Working_EV_small_sat = Working_S.Appliance(Working_S, n = 1, P_max = Pmax_EV['small'], P_var = P_var, w = 1, d_tot = d_tot['saturday']*perc_usage['saturday']['inactive']['main'], r_d = r_d, t_func = t_func['saturday']['business'], r_v = r_v, d_min = d_min['saturday']['business'], fixed = 'no', fixed_cycle = 0, occasional_use = occasional_use['saturday'], flat = 'no', pref_index = 0, wd_we_type = 1, P_series = False)
Working_EV_small_sat.windows(w1 = window['inactive']['main'][0], r_w = r_w['inactive'])

# Working - Small Car - Saturday - Free Time
Working_EV_small_sat_ft = Working_S.Appliance(Working_S, n = 1, P_max = Pmax_EV['small'], P_var = P_var, w = 2, d_tot = d_tot['saturday']*perc_usage['saturday']['inactive']['free time'], r_d = r_d, t_func = t_func['saturday']['personal'], r_v = r_v, d_min = d_min['saturday']['personal'], fixed = 'no', fixed_cycle = 0, occasional_use = occasional_use['free time']['weekend'], flat = 'no', pref_index = 0, wd_we_type = 1, P_series = False)
Working_EV_small_sat_ft.windows(w1 = window['inactive']['free time'][0], w2 = window['inactive']['free time'][1], r_w = r_w['free time'])

# Working - Small Car - Sunday
Working_EV_small_sun = Working_S.Appliance(Working_S, n = 1, P_max = Pmax_EV['small'], P_var = P_var, w = 1, d_tot = d_tot['sunday']*perc_usage['sunday']['inactive']['main'], r_d = r_d, t_func = t_func['sunday']['business'], r_v = r_v, d_min = d_min['sunday']['business'], fixed = 'no', fixed_cycle = 0, occasional_use = occasional_use['sunday'], flat = 'no', pref_index = 0, wd_we_type = 2, P_series = False)
Working_EV_small_sun.windows(w1 = window['inactive']['main'][0], r_w = r_w['inactive'])

# Working - Small Car - Sunday - Free Time
Working_EV_small_sun_ft = Working_S.Appliance(Working_S, n = 1, P_max = Pmax_EV['small'], P_var = P_var, w = 2, d_tot = d_tot['sunday']*perc_usage['sunday']['inactive']['free time'], r_d = r_d, t_func = t_func['sunday']['personal'], r_v = r_v, d_min = d_min['sunday']['personal'], fixed = 'no', fixed_cycle = 0, occasional_use = occasional_use['free time']['weekend'], flat = 'no', pref_index = 0, wd_we_type = 2, P_series = False)
Working_EV_small_sun_ft.windows(w1 = window['inactive']['free time'][0], w2 = window['inactive']['free time'][1], r_w = r_w['free time'])

#%% Student 

### Large Car ###

# Student - Large Car - Weekday
Student_EV_large_wd = Student_L.Appliance(Student_L, n = 1, P_max = Pmax_EV['large'], P_var = P_var, w = 3, d_tot = d_tot['weekday']*perc_usage['weekday']['student']['main'], r_d = r_d, t_func = t_func['weekday']['mean'], r_v = r_v, d_min = d_min['weekday']['mean'], fixed = 'no', fixed_cycle = 0, occasional_use = occasional_use['weekday'], flat = 'no', pref_index = 0, wd_we_type = 0, P_series = False)
Student_EV_large_wd.windows(w1 = window['student']['main'][0], w2 = window['student']['main'][1], w3 = window['student']['main'][2], r_w = r_w['student'])

# Student - Large Car - Weekday - Free Time
Student_EV_large_wd_ft = Student_L.Appliance(Student_L, n = 1, P_max = Pmax_EV['large'], P_var = P_var, w = 2, d_tot = d_tot['weekday']*perc_usage['weekday']['student']['free time'], r_d = r_d, t_func = t_func['weekday']['personal'], r_v = r_v, d_min = d_min['weekday']['personal'], fixed = 'no', fixed_cycle = 0, occasional_use = occasional_use['free time']['weekday'], flat = 'no', pref_index = 0, wd_we_type = 0, P_series = False)
Student_EV_large_wd_ft.windows(w1 = window['student']['free time'][0], w2 = window['student']['free time'][1], r_w = r_w['free time'])

# Student - Large Car - Saturday
Student_EV_large_sat = Student_L.Appliance(Student_L, n = 1, P_max = Pmax_EV['large'], P_var = P_var, w = 1, d_tot = d_tot['saturday']*perc_usage['saturday']['inactive']['main'], r_d = r_d, t_func = t_func['saturday']['mean'], r_v = r_v, d_min = d_min['saturday']['mean'], fixed = 'no', fixed_cycle = 0, occasional_use = occasional_use['saturday'], flat = 'no', pref_index = 0, wd_we_type = 1, P_series = False)
Student_EV_large_sat.windows(w1 = window['inactive']['main'][0], r_w = r_w['inactive'])

# Student - Large Car - Saturday - Free Time
Student_EV_large_sat_ft = Student_L.Appliance(Student_L, n = 1, P_max = Pmax_EV['large'], P_var = P_var, w = 2, d_tot = d_tot['saturday']*perc_usage['saturday']['inactive']['free time'], r_d = r_d, t_func = t_func['saturday']['personal'], r_v = r_v, d_min = d_min['saturday']['personal'], fixed = 'no', fixed_cycle = 0, occasional_use = occasional_use['free time']['weekend'], flat = 'no', pref_index = 0, wd_we_type = 1, P_series = False)
Student_EV_large_sat_ft.windows(w1 = window['inactive']['free time'][0], w2 = window['inactive']['free time'][1], r_w = r_w['free time'])

# Student - Large Car - Sunday
Student_EV_large_sun = Student_L.Appliance(Student_L, n = 1, P_max = Pmax_EV['large'], P_var = P_var, w = 1, d_tot = d_tot['sunday']*perc_usage['sunday']['inactive']['main'], r_d = r_d, t_func = t_func['sunday']['mean'], r_v = r_v, d_min = d_min['sunday']['mean'], fixed = 'no', fixed_cycle = 0, occasional_use = occasional_use['sunday'], flat = 'no', pref_index = 0, wd_we_type = 2, P_series = False)
Student_EV_large_sun.windows(w1 = window['inactive']['main'][0], r_w = r_w['inactive'])

# Student - Large Car - Sunday - Free Time
Student_EV_large_sun_ft = Student_L.Appliance(Student_L, n = 1, P_max = Pmax_EV['large'], P_var = P_var, w = 2, d_tot = d_tot['sunday']*perc_usage['sunday']['inactive']['free time'], r_d = r_d, t_func = t_func['sunday']['personal'], r_v = r_v, d_min = d_min['sunday']['personal'], fixed = 'no', fixed_cycle = 0, occasional_use = occasional_use['free time']['weekend'], flat = 'no', pref_index = 0, wd_we_type = 2, P_series = False)
Student_EV_large_sun_ft.windows(w1 = window['inactive']['free time'][0], w2 = window['inactive']['free time'][1], r_w = r_w['free time'])

### Medium Car ###

# Student - Medium Car - Weekday
Student_EV_medium_wd = Student_M.Appliance(Student_M, n = 1, P_max = Pmax_EV['medium'], P_var = P_var, w = 3, d_tot = d_tot['weekday']*perc_usage['weekday']['student']['main'], r_d = r_d, t_func = t_func['weekday']['mean'], r_v = r_v, d_min = d_min['weekday']['mean'], fixed = 'no', fixed_cycle = 0, occasional_use = occasional_use['weekday'], flat = 'no', pref_index = 0, wd_we_type = 0, P_series = False)
Student_EV_medium_wd.windows(w1 = window['student']['main'][0], w2 = window['student']['main'][1], w3 = window['student']['main'][2], r_w = r_w['student'])

# Student - Medium Car - Weekday - Free Time
Student_EV_medium_wd_ft = Student_M.Appliance(Student_M, n = 1, P_max = Pmax_EV['medium'], P_var = P_var, w = 2, d_tot = d_tot['weekday']*perc_usage['weekday']['student']['free time'], r_d = r_d, t_func = t_func['weekday']['personal'], r_v = r_v, d_min = d_min['weekday']['personal'], fixed = 'no', fixed_cycle = 0, occasional_use = occasional_use['free time']['weekday'], flat = 'no', pref_index = 0, wd_we_type = 0, P_series = False)
Student_EV_medium_wd_ft.windows(w1 = window['student']['free time'][0], w2 = window['student']['free time'][1], r_w = r_w['free time'])

# Student - Medium Car - Saturday
Student_EV_medium_sat = Student_M.Appliance(Student_M, n = 1, P_max = Pmax_EV['medium'], P_var = P_var, w = 1, d_tot = d_tot['saturday']*perc_usage['saturday']['inactive']['main'], r_d = r_d, t_func = t_func['saturday']['mean'], r_v = r_v, d_min = d_min['saturday']['mean'], fixed = 'no', fixed_cycle = 0, occasional_use = occasional_use['saturday'], flat = 'no', pref_index = 0, wd_we_type = 1, P_series = False)
Student_EV_medium_sat.windows(w1 = window['inactive']['main'][0], r_w = r_w['inactive'])

# Student - Medium Car - Saturday - Free Time
Student_EV_medium_sat_ft = Student_M.Appliance(Student_M, n = 1, P_max = Pmax_EV['medium'], P_var = P_var, w = 2, d_tot = d_tot['saturday']*perc_usage['saturday']['inactive']['free time'], r_d = r_d, t_func = t_func['saturday']['personal'], r_v = r_v, d_min = d_min['saturday']['personal'], fixed = 'no', fixed_cycle = 0, occasional_use = occasional_use['free time']['weekend'], flat = 'no', pref_index = 0, wd_we_type = 1, P_series = False)
Student_EV_medium_sat_ft.windows(w1 = window['inactive']['free time'][0], w2 = window['inactive']['free time'][1], r_w = r_w['free time'])

# Student - Medium Car - Sunday
Student_EV_medium_sun = Student_M.Appliance(Student_M, n = 1, P_max = Pmax_EV['medium'], P_var = P_var, w = 1, d_tot = d_tot['sunday']*perc_usage['sunday']['inactive']['main'], r_d = r_d, t_func = t_func['sunday']['mean'], r_v = r_v, d_min = d_min['sunday']['mean'], fixed = 'no', fixed_cycle = 0, occasional_use = occasional_use['sunday'], flat = 'no', pref_index = 0, wd_we_type = 2, P_series = False)
Student_EV_medium_sun.windows(w1 = window['inactive']['main'][0], r_w = r_w['inactive'])

# Student - Medium Car - Sunday - Free Time
Student_EV_medium_sun_ft = Student_M.Appliance(Student_M, n = 1, P_max = Pmax_EV['medium'], P_var = P_var, w = 2, d_tot = d_tot['sunday']*perc_usage['sunday']['inactive']['free time'], r_d = r_d, t_func = t_func['sunday']['personal'], r_v = r_v, d_min = d_min['sunday']['personal'], fixed = 'no', fixed_cycle = 0, occasional_use = occasional_use['free time']['weekend'], flat = 'no', pref_index = 0, wd_we_type = 2, P_series = False)
Student_EV_medium_sun_ft.windows(w1 = window['inactive']['free time'][0], w2 = window['inactive']['free time'][1], r_w = r_w['free time'])

### Small Car ###

# Student - Small Car - Weekday
Student_EV_small_wd = Student_S.Appliance(Student_S, n = 1, P_max = Pmax_EV['small'], P_var = P_var, w = 3, d_tot = d_tot['weekday']*perc_usage['weekday']['student']['main'], r_d = r_d, t_func = t_func['weekday']['mean'], r_v = r_v, d_min = d_min['weekday']['mean'], fixed = 'no', fixed_cycle = 0, occasional_use = occasional_use['weekday'], flat = 'no', pref_index = 0, wd_we_type = 0, P_series = False)
Student_EV_small_wd.windows(w1 = window['student']['main'][0], w2 = window['student']['main'][1], w3 = window['student']['main'][2], r_w = r_w['student'])

# Student - Small Car - Weekday - Free Time
Student_EV_small_wd_ft = Student_S.Appliance(Student_S, n = 1, P_max = Pmax_EV['small'], P_var = P_var, w = 2, d_tot = d_tot['weekday']*perc_usage['weekday']['student']['free time'], r_d = r_d, t_func = t_func['weekday']['personal'], r_v = r_v, d_min = d_min['weekday']['personal'], fixed = 'no', fixed_cycle = 0, occasional_use = occasional_use['free time']['weekday'], flat = 'no', pref_index = 0, wd_we_type = 0, P_series = False)
Student_EV_small_wd_ft.windows(w1 = window['student']['free time'][0], w2 = window['student']['free time'][1], r_w = r_w['free time'])

# Student - Small Car - Saturday
Student_EV_small_sat = Student_S.Appliance(Student_S, n = 1, P_max = Pmax_EV['small'], P_var = P_var, w = 1, d_tot = d_tot['saturday']*perc_usage['saturday']['inactive']['main'], r_d = r_d, t_func = t_func['saturday']['mean'], r_v = r_v, d_min = d_min['saturday']['mean'], fixed = 'no', fixed_cycle = 0, occasional_use = occasional_use['saturday'], flat = 'no', pref_index = 0, wd_we_type = 1, P_series = False)
Student_EV_small_sat.windows(w1 = window['inactive']['main'][0], r_w = r_w['inactive'])

# Student - Small Car - Saturday - Free Time
Student_EV_small_sat_ft = Student_S.Appliance(Student_S, n = 1, P_max = Pmax_EV['small'], P_var = P_var, w = 2, d_tot = d_tot['saturday']*perc_usage['saturday']['inactive']['free time'], r_d = r_d, t_func = t_func['saturday']['personal'], r_v = r_v, d_min = d_min['saturday']['personal'], fixed = 'no', fixed_cycle = 0, occasional_use = occasional_use['free time']['weekend'], flat = 'no', pref_index = 0, wd_we_type = 1, P_series = False)
Student_EV_small_sat_ft.windows(w1 = window['inactive']['free time'][0], w2 = window['inactive']['free time'][1], r_w = r_w['free time'])

# Student - Small Car - Sunday
Student_EV_small_sun = Student_S.Appliance(Student_S, n = 1, P_max = Pmax_EV['small'], P_var = P_var, w = 1, d_tot = d_tot['sunday']*perc_usage['sunday']['inactive']['main'], r_d = r_d, t_func = t_func['sunday']['mean'], r_v = r_v, d_min = d_min['sunday']['mean'], fixed = 'no', fixed_cycle = 0, occasional_use = occasional_use['sunday'], flat = 'no', pref_index = 0, wd_we_type = 2, P_series = False)
Student_EV_small_sun.windows(w1 = window['inactive']['main'][0], r_w = r_w['inactive'])

# Student - Medium Car - Sunday - Free Time
Student_EV_small_sun_ft = Student_S.Appliance(Student_S, n = 1, P_max = Pmax_EV['small'], P_var = P_var, w = 2, d_tot = d_tot['sunday']*perc_usage['sunday']['inactive']['free time'], r_d = r_d, t_func = t_func['sunday']['personal'], r_v = r_v, d_min = d_min['sunday']['personal'], fixed = 'no', fixed_cycle = 0, occasional_use = occasional_use['free time']['weekend'], flat = 'no', pref_index = 0, wd_we_type = 2, P_series = False)
Student_EV_small_sun_ft.windows(w1 = window['inactive']['free time'][0], w2 = window['inactive']['free time'][1], r_w = r_w['free time'])

#%% Inactive 

### Large Car ###
 
# Inactive - Large Car - Weekday
Inactive_EV_large_wd = Inactive_L.Appliance(Inactive_L, n = 1, P_max = Pmax_EV['large'], P_var = P_var, w = 1, d_tot = d_tot['weekday']*perc_usage['weekday']['inactive']['main'], r_d = r_d, t_func = t_func['weekday']['personal'], r_v = r_v, d_min = d_min['weekday']['personal'], fixed = 'no', fixed_cycle = 0, occasional_use = occasional_use['weekday'], flat = 'no', pref_index = 0, wd_we_type = 0, P_series = False)
Inactive_EV_large_wd.windows(w1 = window['inactive']['main'][0], r_w = r_w['inactive'])

# Inactive - Large Car - Weekday - Free Time
Inactive_EV_large_wd_ft = Inactive_L.Appliance(Inactive_L, n = 1, P_max = Pmax_EV['large'], P_var = P_var, w = 2, d_tot = d_tot['weekday']*perc_usage['weekday']['inactive']['free time'], r_d = r_d, t_func = t_func['weekday']['personal'], r_v = r_v, d_min = d_min['weekday']['personal'], fixed = 'no', fixed_cycle = 0, occasional_use = occasional_use['free time']['weekday'], flat = 'no', pref_index = 0, wd_we_type = 0, P_series = False)
Inactive_EV_large_wd_ft.windows(w1 = window['inactive']['free time'][0], w2 = window['inactive']['free time'][1], r_w = r_w['free time'])

# Inactive - Large Car - Saturday
Inactive_EV_large_sat = Inactive_L.Appliance(Inactive_L, n = 1, P_max = Pmax_EV['large'], P_var = P_var, w = 1, d_tot = d_tot['saturday']*perc_usage['saturday']['inactive']['main'], r_d = r_d, t_func = t_func['saturday']['personal'], r_v = r_v, d_min = d_min['saturday']['personal'], fixed = 'no', fixed_cycle = 0, occasional_use = occasional_use['saturday'], flat = 'no', pref_index = 0, wd_we_type = 1, P_series = False)
Inactive_EV_large_sat.windows(w1 = window['inactive']['main'][0], r_w = r_w['inactive'])

# Inactive - Large Car - Saturday - Free Time
Inactive_EV_large_sat_ft = Inactive_L.Appliance(Inactive_L, n = 1, P_max = Pmax_EV['large'], P_var = P_var, w = 2, d_tot = d_tot['saturday']*perc_usage['saturday']['inactive']['free time'], r_d = r_d, t_func = t_func['saturday']['personal'], r_v = r_v, d_min = d_min['saturday']['personal'], fixed = 'no', fixed_cycle = 0, occasional_use = occasional_use['free time']['weekend'], flat = 'no', pref_index = 0, wd_we_type = 1, P_series = False)
Inactive_EV_large_sat_ft.windows(w1 = window['inactive']['free time'][0], w2 = window['inactive']['free time'][1], r_w = r_w['free time'])

# Inactive - Large Car - Sunday
Inactive_EV_large_sun = Inactive_L.Appliance(Inactive_L, n = 1, P_max = Pmax_EV['large'], P_var = P_var, w = 1, d_tot = d_tot['sunday']*perc_usage['sunday']['inactive']['main'], r_d = r_d, t_func = t_func['sunday']['personal'], r_v = r_v, d_min = d_min['sunday']['personal'], fixed = 'no', fixed_cycle = 0, occasional_use = occasional_use['sunday'], flat = 'no', pref_index = 0, wd_we_type = 2, P_series = False)
Inactive_EV_large_sun.windows(w1 = window['inactive']['main'][0], r_w = r_w['inactive'])

# Inactive - Large Car - Sunday - Free Time
Inactive_EV_large_sun_ft = Inactive_L.Appliance(Inactive_L, n = 1, P_max = Pmax_EV['large'], P_var = P_var, w = 2, d_tot = d_tot['sunday']*perc_usage['sunday']['inactive']['free time'], r_d = r_d, t_func = t_func['sunday']['personal'], r_v = r_v, d_min = d_min['sunday']['personal'], fixed = 'no', fixed_cycle = 0, occasional_use = occasional_use['free time']['weekend'], flat = 'no', pref_index = 0, wd_we_type = 2, P_series = False)
Inactive_EV_large_sun_ft.windows(w1 = window['inactive']['free time'][0], w2 = window['inactive']['free time'][1], r_w = r_w['free time'])

### Medium Car ###

# Inactive - Medium Car - Weekday
Inactive_EV_medium_wd = Inactive_M.Appliance(Inactive_M, n = 1, P_max = Pmax_EV['medium'], P_var = P_var, w = 1, d_tot = d_tot['weekday']*perc_usage['weekday']['inactive']['main'], r_d = r_d, t_func = t_func['weekday']['personal'], r_v = r_v, d_min = d_min['weekday']['personal'], fixed = 'no', fixed_cycle = 0, occasional_use = occasional_use['weekday'], flat = 'no', pref_index = 0, wd_we_type = 0, P_series = False)
Inactive_EV_medium_wd.windows(w1 = window['inactive']['main'][0], r_w = r_w['inactive'])

# Inactive - Medium Car - Weekday - Free Time
Inactive_EV_medium_wd_ft = Inactive_M.Appliance(Inactive_M, n = 1, P_max = Pmax_EV['medium'], P_var = P_var, w = 2, d_tot = d_tot['weekday']*perc_usage['weekday']['inactive']['free time'], r_d = r_d, t_func = t_func['weekday']['personal'], r_v = r_v, d_min = d_min['weekday']['personal'], fixed = 'no', fixed_cycle = 0, occasional_use = occasional_use['free time']['weekday'], flat = 'no', pref_index = 0, wd_we_type = 0, P_series = False)
Inactive_EV_medium_wd_ft.windows(w1 = window['inactive']['free time'][0], w2 = window['inactive']['free time'][1], r_w = r_w['free time'])

# Inactive - Medium Car - Saturday
Inactive_EV_medium_sat = Inactive_M.Appliance(Inactive_M, n = 1, P_max = Pmax_EV['medium'], P_var = P_var, w = 1, d_tot = d_tot['saturday']*perc_usage['saturday']['inactive']['main'], r_d = r_d, t_func = t_func['saturday']['personal'], r_v = r_v, d_min = d_min['saturday']['personal'], fixed = 'no', fixed_cycle = 0, occasional_use = occasional_use['saturday'], flat = 'no', pref_index = 0, wd_we_type = 1, P_series = False)
Inactive_EV_medium_sat.windows(w1 = window['inactive']['main'][0], r_w = r_w['inactive'])

# Inactive - Medium Car - Saturday - Free Time
Inactive_EV_medium_sat_ft = Inactive_M.Appliance(Inactive_M, n = 1, P_max = Pmax_EV['medium'], P_var = P_var, w = 2, d_tot = d_tot['saturday']*perc_usage['saturday']['inactive']['free time'], r_d = r_d, t_func = t_func['saturday']['personal'], r_v = r_v, d_min = d_min['saturday']['personal'], fixed = 'no', fixed_cycle = 0, occasional_use = occasional_use['free time']['weekend'], flat = 'no', pref_index = 0, wd_we_type = 1, P_series = False)
Inactive_EV_medium_sat_ft.windows(w1 = window['inactive']['free time'][0], w2 = window['inactive']['free time'][1], r_w = r_w['free time'])

# Inactive - Medium Car - Sunday
Inactive_EV_medium_sun = Inactive_M.Appliance(Inactive_M, n = 1, P_max = Pmax_EV['medium'], P_var = P_var, w = 1, d_tot = d_tot['sunday']*perc_usage['sunday']['inactive']['main'], r_d = r_d, t_func = t_func['sunday']['personal'], r_v = r_v, d_min = d_min['sunday']['personal'], fixed = 'no', fixed_cycle = 0, occasional_use = occasional_use['sunday'], flat = 'no', pref_index = 0, wd_we_type = 2, P_series = False)
Inactive_EV_medium_sun.windows(w1 = window['inactive']['main'][0], r_w = r_w['inactive'])

# Inactive - Medium Car - Sunday - Free Time
Inactive_EV_medium_sun_ft = Inactive_M.Appliance(Inactive_M, n = 1, P_max = Pmax_EV['medium'], P_var = P_var, w = 2, d_tot = d_tot['sunday']*perc_usage['sunday']['inactive']['free time'], r_d = r_d, t_func = t_func['sunday']['personal'], r_v = r_v, d_min = d_min['sunday']['personal'], fixed = 'no', fixed_cycle = 0, occasional_use = occasional_use['free time']['weekend'], flat = 'no', pref_index = 0, wd_we_type = 2, P_series = False)
Inactive_EV_medium_sun_ft.windows(w1 = window['inactive']['free time'][0], w2 = window['inactive']['free time'][1], r_w = r_w['free time'])

### Small Car ###

# Inactive - Small Car - Weekday
Inactive_EV_small_wd = Inactive_S.Appliance(Inactive_S, n = 1, P_max = Pmax_EV['small'], P_var = P_var, w = 1, d_tot = d_tot['weekday']*perc_usage['weekday']['inactive']['main'], r_d = r_d, t_func = t_func['weekday']['personal'], r_v = r_v, d_min = d_min['weekday']['personal'], fixed = 'no', fixed_cycle = 0, occasional_use = occasional_use['weekday'], flat = 'no', pref_index = 0, wd_we_type = 0, P_series = False)
Inactive_EV_small_wd.windows(w1 = window['inactive']['main'][0], r_w = r_w['inactive'])

# Inactive - Small Car - Weekday - Free Time
Inactive_EV_small_wd_ft = Inactive_S.Appliance(Inactive_S, n = 1, P_max = Pmax_EV['small'], P_var = P_var, w = 2, d_tot = d_tot['weekday']*perc_usage['weekday']['inactive']['free time'], r_d = r_d, t_func = t_func['weekday']['personal'], r_v = r_v, d_min = d_min['weekday']['personal'], fixed = 'no', fixed_cycle = 0, occasional_use = occasional_use['free time']['weekday'], flat = 'no', pref_index = 0, wd_we_type = 0, P_series = False)
Inactive_EV_small_wd_ft.windows(w1 = window['inactive']['free time'][0], w2 = window['inactive']['free time'][1], r_w = r_w['free time'])

# Inactive - Small Car - Saturday
Inactive_EV_small_sat = Inactive_S.Appliance(Inactive_S, n = 1, P_max = Pmax_EV['small'], P_var = P_var, w = 1, d_tot = d_tot['saturday']*perc_usage['saturday']['inactive']['main'], r_d = r_d, t_func = t_func['saturday']['personal'], r_v = r_v, d_min = d_min['saturday']['personal'], fixed = 'no', fixed_cycle = 0, occasional_use = occasional_use['saturday'], flat = 'no', pref_index = 0, wd_we_type = 1, P_series = False)
Inactive_EV_small_sat.windows(w1 = window['inactive']['main'][0], r_w = r_w['inactive'])

# Inactive - Small Car - Weekday - Free Time
Inactive_EV_small_sat_ft = Inactive_S.Appliance(Inactive_S, n = 1, P_max = Pmax_EV['small'], P_var = P_var, w = 2, d_tot = d_tot['weekday']*perc_usage['saturday']['inactive']['free time'], r_d = r_d, t_func = t_func['weekday']['personal'], r_v = r_v, d_min = d_min['weekday']['personal'], fixed = 'no', fixed_cycle = 0, occasional_use = occasional_use['free time']['weekend'], flat = 'no', pref_index = 0, wd_we_type = 0, P_series = False)
Inactive_EV_small_sat_ft.windows(w1 = window['inactive']['free time'][0], w2 = window['inactive']['free time'][1], r_w = r_w['free time'])

# Inactive - Small Car - Sunday
Inactive_EV_small_sun = Inactive_S.Appliance(Inactive_S, n = 1, P_max = Pmax_EV['small'], P_var = P_var, w = 1, d_tot = d_tot['sunday']*perc_usage['sunday']['inactive']['main'], r_d = r_d, t_func = t_func['sunday']['personal'], r_v = r_v, d_min = d_min['sunday']['personal'], fixed = 'no', fixed_cycle = 0, occasional_use = occasional_use['sunday'], flat = 'no', pref_index = 0, wd_we_type = 2, P_series = False)
Inactive_EV_small_sun.windows(w1 = window['inactive']['main'][0], r_w = r_w['inactive'])

# Inactive - Small Car - Sunday - Free Time
Inactive_EV_small_sun_ft = Inactive_S.Appliance(Inactive_S, n = 1, P_max = Pmax_EV['small'], P_var = P_var, w = 2, d_tot = d_tot['sunday']*perc_usage['sunday']['inactive']['free time'], r_d = r_d, t_func = t_func['sunday']['personal'], r_v = r_v, d_min = d_min['sunday']['personal'], fixed = 'no', fixed_cycle = 0, occasional_use = occasional_use['free time']['weekend'], flat = 'no', pref_index = 0, wd_we_type = 2, P_series = False)
Inactive_EV_small_sun_ft.windows(w1 = window['inactive']['free time'][0], w2 = window['inactive']['free time'][1], r_w = r_w['free time'])