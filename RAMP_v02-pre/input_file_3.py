# -*- coding: utf-8 -*-

#%% Definition of the inputs
'''
Input data definition 
'''

from core import User, np, pd
User_list = []

#Create new user classes
Working = User(name = "Working", n_users = 50, us_pref = 0)
User_list.append(Working)

Student = User(name = "Student", n_users = 25, us_pref = 0)
User_list.append(Student)

Inactive = User(name = "Inactive", n_users = 10, us_pref = 0)
User_list.append(Inactive)

# Working 
Working_EV = Working.Appliance(Working, n = 1, P_max = 50*1e3, P_var = 0.1, w = 2, d_tot = 40, r_d = 0.4, t_func = 25, r_v = 0.3, d_min = 6.2, fixed = 'no', fixed_cycle = 0, occasional_use = 1, flat = 'no', pref_index = 0, wd_we_type = 1, P_series = False)
Working_EV.windows(w1 = [420,540], w2 = [960, 1140], r_w = 0.3)

# Student
Student_EV = Student.Appliance(Student, n = 1, P_max = 50*1e3, P_var = 0.1, w = 3, d_tot = 40, r_d = 0.4, t_func = 25, r_v = 0.3, d_min = 6.2, fixed = 'no', fixed_cycle = 0, occasional_use = 1, flat = 'no', pref_index = 0, wd_we_type = 0, P_series = False)
Student_EV.windows(w1 = [420,540], w2 = [720, 900], w3 = [960,1140], r_w = 0.3)

# Inactive
Inactive_EV = Inactive.Appliance(Inactive, n = 1, P_max = 50*1e3, P_var = 0.1, w = 1, d_tot = 40, r_d = 0.4, t_func = 25, r_v = 0.3, d_min = 6.2, fixed = 'no', fixed_cycle = 0, occasional_use = 1, flat = 'no', pref_index = 0, wd_we_type = 0, P_series = False)
Inactive_EV.windows(w1 = [420,1140], r_w = 0.1)

#Define yearly Temperature profile in form of hourly dataframe with one columns
#Here data from Renewables Ninja for 2016 and all EU were loaded, but you can choose your own temperature profile


inputfile = r"C:\Users\Andrea\GitHub\RAMP\RAMP_v02-pre\TimeSeries\temp_2016_pop.csv"

country = 'IT' # To filter ony for one columns

temp_profile = pd.read_csv(inputfile, index_col = 0)
temp_profile = pd.DataFrame(temp_profile[country])
