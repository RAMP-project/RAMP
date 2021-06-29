# -*- coding: utf-8 -*-
"""
Minimal qualitative test functionality. Compares outputs of the code to default outputs,
for the 3 reference input files. The judgement about whether the resulting changes are
as expected or not is left to the developers
"""

#%% Import required modules
import pandas as pd
import matplotlib.pyplot as plt
import os
#%% Function to test the output against reference results
'''
By default, reference results are provided for a series of 30 days and for
all th 3 reference input files. If this is changed, the function below must
be called for the correct number of input files and days through the related
parameters
'''

def test_output(results_folder,test_folder, num_input_files=3, num_days=30):
    
    def series_to_average(profile_series, num_days):
        
        average_series = profile_series[0:1440]
        for d in range(1,num_days):
            average_series += profile_series[0+1440*d:1440+1440*d].set_index(average_series.index)
            average_series = average_series/ (d+1)
        
        return average_series
    
    default_out = {}
    current_out = {}
    axes = {}
    
    fig = plt.figure(figsize=(14,14))
    
    for n in range(1,num_input_files+1):
        
        default_out[n] = series_to_average(pd.read_csv('{}/output_file_{}.csv'.format(test_folder,n), index_col=0), num_days)
        current_out[n] = series_to_average(pd.read_csv('{}/output_file_{}.csv'.format(results_folder,n), index_col=0), num_days)
        
        axes[n] = fig.add_subplot((310+n))
   
        axes[n].plot(default_out[n], color='red', linewidth=2, label='default')
        axes[n].plot(current_out[n], color='blue',linewidth=1, alpha=0.8, linestyle='--', label='new results')
        axes[n].set_xmargin(0)
        axes[n].set_ymargin(0)
        axes[n].set_ylabel('Power demand (kW)')
        
    axes[n].get_shared_x_axes().join(axes[n], axes[n-1], axes[n-2])
    axes[n-1].legend()
    axes[n-1].set_xticklabels([])
    axes[n-2].set_xticklabels([])
    
#%% Testing the output and providing visual result
'''
Here the visual comparison between default and new/current results occurs.
Besides the difference naturally occurring due to different realisations of stochastic
parameters, the developers should check whether any other differences are brought by
by the tested code changes. If any differences are there, the developers should 
evaluate whether these are as expected/designed or not
'''
os.chdir('..')
test_output('results','test')