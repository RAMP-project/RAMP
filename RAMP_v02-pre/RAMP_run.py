# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 14:35:00 2019
This is the code for the open-source stochastic model for the generation of 
multi-energy load profiles in off-grid areas, called RAMP, v.0.2.1-pre.

@authors:
- Francesco Lombardi, Politecnico di Milano
- Sergio Balderrama, Université de Liège
- Sylvain Quoilin, KU Leuven
- Emanuela Colombo, Politecnico di Milano

Copyright 2019 RAMP, contributors listed above.
Licensed under the European Union Public Licence (EUPL), Version 1.1;
you may not use this file except in compliance with the License.

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations
under the License.
"""

#%% Import required modules

from stochastic_process import Stochastic_Process
from post_process import*
import time

provinces = pd.read_csv('time_series/gw_temp_province.csv', sep=';', index_col=0).columns.to_list()
archetypes = pd.read_csv('time_series/building_archetypes.csv', sep=';', index_col=0)
archetypes_ratio = {'single_family': 1, 'double_family': 1.2 , 'multi_family': 1.6 , 'apartment_block': 2.1 }
n_dict = {'U1': 0.253, 'U2': 0.263, 'U3': 0.484}

#provinces_lomb = 
        
profiles_dict = {}

for prov in provinces:
    profiles_dict[prov] = {}
    for arch in archetypes[prov].index:
        profiles_dict[prov][arch] = {}
        n = archetypes[prov].loc[arch]/1e3
        for us in n_dict.keys():
            profiles_dict[prov][arch][us] = {}
            for k in range(int(round(n_dict[us]*n))):
                for j in range(1,2):
                        seconds = time.time()
                        Profiles_list = Stochastic_Process(j,archetypes_ratio[arch],prov)
                        Profiles_avg, Profiles_list_kW, Profiles_series = Profile_formatting(Profiles_list)
                        profiles_dict[prov][arch][us]['%d' %k] = Profiles_series
                        seconds = time.time() -seconds
        # Post-processes the results and generates plots
        
#        Profile_series_plot(Profiles_series) #by default, profiles are plotted as a series
        
#        export_series(Profiles_series,j,arch)

#    if len(Profiles_list) > 1: #if more than one daily profile is generated, also cloud plots are shown
#        Profile_cloud_plot(Profiles_list, Profiles_avg)

