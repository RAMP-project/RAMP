# -*- coding: utf-8 -*-

#%% Definition of the inputs
'''
Input data definition 
'''

from core import User, np, pd
User_list = []

'''Common values used in the input data definition'''

#Total number of users to be simulated
tot_users = 1000

#Composition of the population by percentage share
pop_sh = {}

pop_sh['working'] = 0.572
pop_sh['student'] = 0.047
pop_sh['inactive'] = 0.381

#Share of the type of vehicles in the country
vehicle_sh = {}

vehicle_sh['small'] = 0.24
vehicle_sh['medium'] = 0.69
vehicle_sh['large'] = 0.07

#Maximum power of the vehicle by type [kW]
Pmax_EV = {}

Pmax_EV['small'] = 61
Pmax_EV['medium'] = 150
Pmax_EV['large'] = 350

# Functioning windows 
window = {}

window['working'] = [[420,540],[960, 1140]]
window['student'] = [[420,540],[720, 900],[960, 1140]]
window['inactive'] = [[420,1140]]

# Total daily distance 
d_tot = {}

d_tot['weekday'] = 50
d_tot['weekend'] = 55

# Distance by trip
d_min = {}

d_min['weekday'] = {'business': 19, 'personal': 16}
d_min['weekend'] = {'business': 21, 'personal': 20} 
d_min['weekday']['mean'] = int(np.array([d_min['weekday'][k] for k in d_min['weekday']]).mean())
d_min['weekend']['mean'] = int(np.array([d_min['weekend'][k] for k in d_min['weekend']]).mean())

# Functioning time by trip
t_func = {}

t_func['weekday'] = {'business': 26, 'personal': 21}
t_func['weekend'] = {'business': 28, 'personal': 31} 
t_func['weekday']['mean'] = int(np.array([t_func['weekday'][k] for k in t_func['weekday']]).mean())
t_func['weekend']['mean'] = int(np.array([t_func['weekend'][k] for k in t_func['weekend']]).mean())

#Variabilities 

P_var = 0.1 #random in power
r_d = 0.3 #random in distance
r_v = 0.3 #random in velocity

'''Users'''

#Create new user classes
Working_L = User(name = "Working - Large car", us_pref = 0,
                 n_users = int(tot_users*pop_sh['working']*vehicle_sh['large']))
User_list.append(Working_L)

Working_M = User(name = "Working - Medium car", us_pref = 0,
                 n_users = int(tot_users*pop_sh['working']*vehicle_sh['medium']))
User_list.append(Working_M)

Working_S = User(name = "Working - Small car", us_pref = 0,
                  n_users = int(tot_users*pop_sh['working']*vehicle_sh['small']))
User_list.append(Working_S)

Student_L = User(name = "Student - Large car", us_pref = 0,
                  n_users = int(tot_users*pop_sh['student']*vehicle_sh['large']))
User_list.append(Student_L)

Student_M = User(name = "Student - Medium car", us_pref = 0,
                 n_users = int(tot_users*pop_sh['student']*vehicle_sh['medium']))
User_list.append(Student_M)

Student_S = User(name = "Student - Small car", us_pref = 0,
                 n_users = int(tot_users*pop_sh['student']*vehicle_sh['small']))
User_list.append(Student_M)

Inactive_L = User(name = "Inactive - Large car", us_pref = 0,
                  n_users = int(tot_users*pop_sh['inactive']*vehicle_sh['large']))
User_list.append(Inactive_L)

Inactive_M = User(name = "Inactive - Medium car", us_pref = 0,
                  n_users = int(tot_users*pop_sh['inactive']*vehicle_sh['medium']))
User_list.append(Inactive_M)

Inactive_S = User(name = "Inactive - Small car", us_pref = 0,
                  n_users = int(tot_users*pop_sh['inactive']*vehicle_sh['small']))
User_list.append(Inactive_S)

'''Appliances'''

# Working 
Working_EV_large_wd = Working_L.Appliance(Working_L, n = 1, P_max = Pmax_EV['large'], P_var = P_var, w = 2, d_tot = d_tot['weekday'], r_d = r_d, t_func = t_func['weekday']['business'], r_v = r_v, d_min = d_min['weekday']['business'], fixed = 'no', fixed_cycle = 0, occasional_use = 1, flat = 'no', pref_index = 0, wd_we_type = 0, P_series = False)
Working_EV_large_wd.windows(w1 = window['working'][0], w2 = window['working'][1], r_w = 0.3)

# Working_EV_large_we = Working_EV_large_wd
# Working_EV_large_we.wd_we_type = 1
# Working_EV_large_we.d_tot = d_tot['weekend']

Working_EV_large_we = Working_L.Appliance(Working_L, n = 1, P_max = Pmax_EV['large'], P_var = P_var, w = 2, d_tot = d_tot['weekend'], r_d = r_d, t_func = t_func['weekend']['business'], r_v = r_v, d_min = d_min['weekend']['business'], fixed = 'no', fixed_cycle = 0, occasional_use = 1, flat = 'no', pref_index = 0, wd_we_type = 1, P_series = False)
Working_EV_large_we.windows(w1 = window['working'][0], w2 = window['working'][1], r_w = 0.3)

Working_EV_medium_wd = Working_M.Appliance(Working_M, n = 1, P_max = Pmax_EV['medium'], P_var = P_var, w = 2, d_tot = d_tot['weekday'], r_d = r_d, t_func = t_func['weekday']['business'], r_v = r_v, d_min = d_min['weekday']['business'], fixed = 'no', fixed_cycle = 0, occasional_use = 1, flat = 'no', pref_index = 0, wd_we_type = 0, P_series = False)
Working_EV_medium_wd.windows(w1 = window['working'][0], w2 = window['working'][1], r_w = 0.3)

Working_EV_medium_we = Working_M.Appliance(Working_M, n = 1, P_max = Pmax_EV['medium'], P_var = P_var, w = 2, d_tot = d_tot['weekend'], r_d = r_d, t_func = t_func['weekend']['business'], r_v = r_v, d_min = d_min['weekend']['business'], fixed = 'no', fixed_cycle = 0, occasional_use = 1, flat = 'no', pref_index = 0, wd_we_type = 1, P_series = False)
Working_EV_medium_we.windows(w1 = window['working'][0], w2 = window['working'][1], r_w = 0.3)

Working_EV_small_wd = Working_S.Appliance(Working_S, n = 1, P_max = Pmax_EV['small'], P_var = P_var, w = 2, d_tot = d_tot['weekday'], r_d = r_d, t_func = t_func['weekday']['business'], r_v = r_v, d_min = d_min['weekday']['business'], fixed = 'no', fixed_cycle = 0, occasional_use = 1, flat = 'no', pref_index = 0, wd_we_type = 0, P_series = False)
Working_EV_small_wd.windows(w1 = window['working'][0], w2 = window['working'][1], r_w = 0.3)

Working_EV_small_we = Working_S.Appliance(Working_S, n = 1, P_max = Pmax_EV['small'], P_var = P_var, w = 2, d_tot = d_tot['weekend'], r_d = r_d, t_func = t_func['weekend']['business'], r_v = r_v, d_min = d_min['weekend']['business'], fixed = 'no', fixed_cycle = 0, occasional_use = 1, flat = 'no', pref_index = 0, wd_we_type = 1, P_series = False)
Working_EV_small_we.windows(w1 = window['working'][0], w2 = window['working'][1], r_w = 0.3)

# Student
Student_EV_large_wd = Student_L.Appliance(Student_L, n = 1, P_max = Pmax_EV['large'], P_var = P_var, w = 3, d_tot = d_tot['weekday'], r_d = r_d, t_func = t_func['weekday']['mean'], r_v = r_v, d_min = d_min['weekday']['mean'], fixed = 'no', fixed_cycle = 0, occasional_use = 1, flat = 'no', pref_index = 0, wd_we_type = 0, P_series = False)
Student_EV_large_wd.windows(w1 = window['student'][0], w2 = window['student'][1], w3 = window['student'][2], r_w = 0.3)

Student_EV_large_we = Student_L.Appliance(Student_L, n = 1, P_max = Pmax_EV['large'], P_var = P_var, w = 3, d_tot = d_tot['weekend'], r_d = r_d, t_func = t_func['weekend']['mean'], r_v = r_v, d_min = d_min['weekend']['mean'], fixed = 'no', fixed_cycle = 0, occasional_use = 1, flat = 'no', pref_index = 0, wd_we_type = 1, P_series = False)
Student_EV_large_we.windows(w1 = window['student'][0], w2 = window['student'][1], w3 = window['student'][2], r_w = 0.3)

Student_EV_medium_wd = Student_M.Appliance(Student_M, n = 1, P_max = Pmax_EV['medium'], P_var = P_var, w = 3, d_tot = d_tot['weekday'], r_d = r_d, t_func = t_func['weekday']['mean'], r_v = r_v, d_min = d_min['weekday']['mean'], fixed = 'no', fixed_cycle = 0, occasional_use = 1, flat = 'no', pref_index = 0, wd_we_type = 0, P_series = False)
Student_EV_medium_wd.windows(w1 = window['student'][0], w2 = window['student'][1], w3 = window['student'][2], r_w = 0.3)

Student_EV_medium_we = Student_M.Appliance(Student_M, n = 1, P_max = Pmax_EV['medium'], P_var = P_var, w = 3, d_tot = d_tot['weekend'], r_d = r_d, t_func = t_func['weekend']['mean'], r_v = r_v, d_min = d_min['weekend']['mean'], fixed = 'no', fixed_cycle = 0, occasional_use = 1, flat = 'no', pref_index = 0, wd_we_type = 1, P_series = False)
Student_EV_medium_we.windows(w1 = window['student'][0], w2 = window['student'][1], w3 = window['student'][2], r_w = 0.3)

Student_EV_small_wd = Student_S.Appliance(Student_S, n = 1, P_max = Pmax_EV['small'], P_var = P_var, w = 3, d_tot = d_tot['weekday'], r_d = r_d, t_func = t_func['weekday']['mean'], r_v = r_v, d_min = d_min['weekday']['mean'], fixed = 'no', fixed_cycle = 0, occasional_use = 1, flat = 'no', pref_index = 0, wd_we_type = 0, P_series = False)
Student_EV_small_wd.windows(w1 = window['student'][0], w2 = window['student'][1], w3 = window['student'][2], r_w = 0.3)

Student_EV_small_we = Student_S.Appliance(Student_S, n = 1, P_max = Pmax_EV['small'], P_var = P_var, w = 3, d_tot = d_tot['weekend'], r_d = r_d, t_func = t_func['weekend']['mean'], r_v = r_v, d_min = d_min['weekend']['mean'], fixed = 'no', fixed_cycle = 0, occasional_use = 1, flat = 'no', pref_index = 0, wd_we_type = 1, P_series = False)
Student_EV_small_we.windows(w1 = window['student'][0], w2 = window['student'][1], w3 = window['student'][2], r_w = 0.3)

# Inactive
Inactive_EV_large_wd = Inactive_L.Appliance(Inactive_L, n = 1, P_max = Pmax_EV['large'], P_var = P_var, w = 1, d_tot = d_tot['weekday'], r_d = r_d, t_func = t_func['weekday']['personal'], r_v = r_v, d_min = d_min['weekday']['personal'], fixed = 'no', fixed_cycle = 0, occasional_use = 1, flat = 'no', pref_index = 0, wd_we_type = 0, P_series = False)
Inactive_EV_large_wd.windows(w1 = window['inactive'][0], r_w = 0.1)

Inactive_EV_large_we = Inactive_L.Appliance(Inactive_L, n = 1, P_max = Pmax_EV['large'], P_var = P_var, w = 1, d_tot = d_tot['weekend'], r_d = r_d, t_func = t_func['weekend']['personal'], r_v = r_v, d_min = d_min['weekend']['personal'], fixed = 'no', fixed_cycle = 0, occasional_use = 1, flat = 'no', pref_index = 0, wd_we_type = 1, P_series = False)
Inactive_EV_large_we.windows(w1 = window['inactive'][0], r_w = 0.1)

Inactive_EV_medium_wd = Inactive_M.Appliance(Inactive_M, n = 1, P_max = Pmax_EV['medium'], P_var = P_var, w = 1, d_tot = d_tot['weekday'], r_d = r_d, t_func = t_func['weekday']['personal'], r_v = r_v, d_min = d_min['weekday']['personal'], fixed = 'no', fixed_cycle = 0, occasional_use = 1, flat = 'no', pref_index = 0, wd_we_type = 0, P_series = False)
Inactive_EV_medium_wd.windows(w1 = window['inactive'][0], r_w = 0.1)

Inactive_EV_medium_we = Inactive_M.Appliance(Inactive_M, n = 1, P_max = Pmax_EV['medium'], P_var = P_var, w = 1, d_tot = d_tot['weekend'], r_d = r_d, t_func = t_func['weekend']['personal'], r_v = r_v, d_min = d_min['weekend']['personal'], fixed = 'no', fixed_cycle = 0, occasional_use = 1, flat = 'no', pref_index = 0, wd_we_type = 1, P_series = False)
Inactive_EV_medium_we.windows(w1 = window['inactive'][0], r_w = 0.1)

Inactive_EV_small_wd = Inactive_S.Appliance(Inactive_S, n = 1, P_max = Pmax_EV['small'], P_var = P_var, w = 1, d_tot = d_tot['weekday'], r_d = r_d, t_func = t_func['weekday']['personal'], r_v = r_v, d_min = d_min['weekday']['personal'], fixed = 'no', fixed_cycle = 0, occasional_use = 1, flat = 'no', pref_index = 0, wd_we_type = 0, P_series = False)
Inactive_EV_small_wd.windows(w1 = window['inactive'][0], r_w = 0.1)

Inactive_EV_small_we = Inactive_S.Appliance(Inactive_S, n = 1, P_max = Pmax_EV['small'], P_var = P_var, w = 1, d_tot = d_tot['weekend'], r_d = r_d, t_func = t_func['weekend']['personal'], r_v = r_v, d_min = d_min['weekend']['personal'], fixed = 'no', fixed_cycle = 0, occasional_use = 1, flat = 'no', pref_index = 0, wd_we_type = 1, P_series = False)
Inactive_EV_small_we.windows(w1 = window['inactive'][0], r_w = 0.1)
