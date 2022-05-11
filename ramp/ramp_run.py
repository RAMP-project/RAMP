# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 14:35:00 2019
This is the code for the open-source stochastic model for the generation of 
multi-energy load profiles in off-grid areas, called RAMP, v0.3.0.

@authors:
- Francesco Lombardi, Politecnico di Milano
- Sergio Balderrama, Université de Liège
- Sylvain Quoilin, KU Leuven
- Emanuela Colombo, Politecnico di Milano

Copyright 2019 RAMP, contributors listed above.
Licensed under the European Union Public Licence (EUPL), Version 1.2;
you may not use this file except in compliance with the License.

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations
under the License.
"""

#%% Import required modules

import sys,os
sys.path.append('../')
import argparse


from core.stochastic_process import Stochastic_Process
from post_process import post_process as pp


parser = argparse.ArgumentParser(
    prog="python ramp_run.py", description="Execute RAMP code"
)
parser.add_argument(
    "-i",
    dest="fname_path",
    nargs="+",
    type=str,
    help="path to the (xlsx) input files (including filename). If not provided, then legacy .py input files will be fetched",
)
parser.add_argument(
    "-n",
    dest="num_profiles",
    nargs="+",
    type=int,
    help="number of profiles to be generated",
)

def run_usecase(j=None, fname=None, num_profiles=None):
    # Calls the stochastic process and saves the result in a list of stochastic profiles
    Profiles_list = Stochastic_Process(j=j, fname=fname, num_profiles=num_profiles)

    # Post-processes the results and generates plots
    Profiles_avg, Profiles_list_kW, Profiles_series = pp.Profile_formatting(Profiles_list)
    pp.Profile_series_plot(Profiles_series)  # by default, profiles are plotted as a series

    pp.export_series(Profiles_series, j, fname)

    if len(Profiles_list) > 1:  # if more than one daily profile is generated, also cloud plots are shown
        pp.Profile_cloud_plot(Profiles_list, Profiles_avg)


if __name__ == "__main__":

    args = vars(parser.parse_args())
    fnames = args["fname_path"]
    num_profiles = args["num_profiles"]
    # Define which input files should be considered and run.


    if fnames is None:
        print("Please provide path to input file with option -i, \n\nDefault to old version of RAMP input files\n")
        # Files are specified as numbers in a list (e.g. [1,2] will consider input_file_1.py and input_file_2.py)
        input_files_to_run = [1, 2, 3]

        if num_profiles is not None:
            if len(num_profiles) == 1:
                num_profiles = num_profiles * len(input_files_to_run)
            else:
                if len(num_profiles) != len(input_files_to_run):
                    raise ValueError("The number of profiles parameters  should match the number of input files provided")
        else:
            num_profiles = [None] * len(input_files_to_run)

        for i, j in enumerate(input_files_to_run):
            run_usecase(j=j, num_profiles=num_profiles[i])
    else:
        if num_profiles is not None:
            if len(num_profiles) == 1:
                num_profiles = num_profiles * len(fnames)
            else:
                if len(num_profiles) != len(fnames):
                    raise ValueError(
                        "The number of profiles parameters  should match the number of input files provided")
        else:
            num_profiles = [None] * len(fnames)

        for i, fname in enumerate(fnames):
            run_usecase(fname=fname, num_profiles=num_profiles[i])




