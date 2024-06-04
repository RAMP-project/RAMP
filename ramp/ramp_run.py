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
import os

# %% Import required modules

import sys
from ramp.core.core import UseCase
import ramp.post_process as pp

sys.path.append("../")

try:
    from .post_process import post_process as pp
except ImportError:
    from post_process import post_process as pp


def run_usecase(
    fname,
    ofname=None,
    num_days=None,
    date_start=None,
    date_end=None,
    plot=True,
    parallel=False,
):
    if fname.endswith(".xlsx"):
        usecase = UseCase(
            date_start=date_start, date_end=date_end, parallel_processing=parallel
        )
        usecase.initialize(num_days=num_days)
        usecase.load(fname)
        Profiles_list = usecase.generate_daily_load_profiles(flat=False)

        if plot is True:
            # TODO use new plotting
            # Post-processes the results and generates plots
            pp.old_post_process(Profiles_list, fname, ofname)
        else:
            return Profiles_list
    elif fname.endswith(".py"):
        if os.path.exists(fname):
            os.system(f"python {fname}")
        else:
            raise FileNotFoundError(f"{fname} is not an existing file")
    else:
        raise TypeError(
            "Only the .py and .xlsx file format are supported for ramp command line"
        )
