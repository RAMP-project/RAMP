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

#%% Import required modules and objects
import pandas as pd

from stochastic_process import Stochastic_Process
from post_process import*
from utils import save_obj

administrative_units = pd.read_csv('time_series/administrative_units.csv', sep=',')
provinces = administrative_units['province'].to_list()
#provinces = pd.read_csv('time_series/gw_temp_province.csv', sep=';', index_col=0).columns.to_list()
archetypes = pd.read_csv('time_series/building_archetypes.csv', sep=';', index_col=0)
for prov in provinces:
    archetypes[prov] = (round(archetypes[prov] * administrative_units['share_DHW_independent'][administrative_units['province']==prov].values))
archetypes_ratio = {'single_family': 2.1, 'double_family': 1.6 , 'multi_family': 1.2 , 'apartment_block': 1.0 }
n_dict = {'U1': 0.253, 'U2': 0.263, 'U3': 0.484}
us_dict = {'U1': 1, 'U2': 2, 'U3': 3}

#%% Main script
profiles_dict = {}

for prov in provinces:
    profiles_dict[prov] = {}
    for arch in archetypes[prov].index:
        profiles_dict[prov][arch] = {}
        n = archetypes[prov].loc[arch]/1e2
        for us in n_dict.keys():
            profiles_dict[prov][arch][us] = {}
            for k in range(int(round(n_dict[us]*n))):
                j = us_dict[us]
                Profiles_list = Stochastic_Process(j,archetypes_ratio[arch],prov)
                Profiles_avg, Profiles_list_kW, Profiles_series = Profile_formatting(Profiles_list)
                profiles_dict[prov][arch][us]['%d' %k] = Profiles_series
                        
# Saving the results
save_obj(profiles_dict, 'profiles_dict_Italy_50k')

