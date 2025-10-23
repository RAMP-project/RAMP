# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 10:28:55 2024

@author: nilsl
"""

import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np
from openpyxl import load_workbook
from ramp import UseCase, User
import time
import datetime

start = time.time()



workbook = load_workbook(filename="example_excel_usecase_filled_final.xlsx")
workbook.save(filename="example_excel_usecase_filled_new_final.xlsx")

use_case = UseCase()  # creating a new UseCase instance

use_case.load("example_excel_usecase_filled_new_final.xlsx")

#dictionary for the user and appliance limits
user_lim = {}
user_lim['household_low'] = 15
user_lim['household_low_growth'] = 15
user_lim['household_med'] = 15
user_lim['household_med_growth'] = 15
user_lim['household_high'] = 7
user_lim['household_high_growth'] = 7
user_lim['IGA'] = 3
user_lim['Church'] = 2
user_lim['PL'] = 1
app_lim  = {}
app_lim['light'] = 8
app_lim['radio'] = 2
app_lim['tv'] = 1
app_lim['decoder'] = 1
app_lim['dvd'] = 1
app_lim['charger'] = 3
app_lim['woofer'] = 1
app_lim['freezer'] = 1
app_lim['speaker'] = 1
app_lim['light_fresh'] = 8
app_lim['radio_fresh'] = 2
app_lim['tv_fresh'] = 1
app_lim['decoder_fresh'] = 1
app_lim['dvd_fresh'] = 1
app_lim['charger_fresh'] = 4
app_lim['woofer_fresh'] = 1
app_lim['freezer_fresh'] = 1
app_lim['speaker_fresh'] = 1
app_lim['laptop_fresh'] = 1

app_lim['Appliance_1'] = 2
app_lim['Appliance_2'] = 2
app_lim['Appliance_3'] = 2
app_lim['Appliance_4'] = 2
app_lim['Appliance_5'] = 5



Load_ECOS = np.mean(np.load("Load_ECOS.npy").reshape((24,60)),axis = 1)

n_days = 30
date_start = "2024-01-01"
use_case.date_start = date_start
use_case.initialize(num_days=n_days, force=True)
n_years = 5
profile = use_case.generate_daily_load_profiles(flat=True, num_years = n_years, num_app_lim=app_lim, num_user_lim=user_lim, load_growth='yes')





if n_years == 1:
    Load = profile.reshape((n_days,60*24))
    Load_mean_day = np.mean(Load, axis = 0).reshape((24,60))
    Load_RAMP = np.mean(Load_mean_day, axis = 1)
    plt.plot(Load_RAMP)
    plt.show()

else:
    Load = profile.iloc[:].to_numpy()
    Load_mean_day = np.zeros((n_years,1440))
    for n in range(n_years):
        Load_year_n = np.transpose(Load[:,n])
        Load_year_n_reshape = Load_year_n.reshape((n_days,1440))
        Load_mean_day[n,:] = np.mean(Load_year_n_reshape, axis = 0)
    
    Load_plot = np.mean(Load_mean_day.reshape((n_years,24,60)),axis=2)
    fig, ax = plt.subplots()
    time_axis = [datetime.datetime(2024, 1, 1, 8) + datetime.timedelta(hours=i) for i in range(24)]  # 08:00 to 08:00 next day
    tick_times = [time_axis[0] + datetime.timedelta(hours=i) for i in range(0, 24, 2)]
    plot_legend = []
    for n2 in range(n_years):
        plt.plot(time_axis,Load_plot[n2,:], label = str(n2))
        plot_legend.append("Year" + str(n2)) 
    plt.xticks(fontsize = 11)
    plt.yticks(fontsize = 11)
    
    ax.set_xticks(tick_times)
    ax.set_xticklabels([dt.strftime('%H:%M') for dt in tick_times], rotation=45)
    plt.legend(plot_legend, fontsize = 12)
    plt.xlabel("Time [Hour]", fontsize = 13)
    plt.ylabel("Electrical Demand [kW]", fontsize = 13)
    plt.tight_layout()
    plt.show()
    
    
    
    
   

