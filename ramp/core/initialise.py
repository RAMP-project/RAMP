# -*- coding: utf-8 -*-

#%% Initialisation of a model instance

import numpy as np
import importlib
from ramp.core.core import UseCase


def yearly_pattern():
    """Definition of a yearly pattern of weekends and weekdays, in case some appliances have specific wd/we behaviour"""

    year_behaviour = np.zeros(365)
    year_behaviour[5:365:7] = 1
    year_behaviour[6:365:7] = 1

    return year_behaviour


def user_defined_inputs(j=None, fname=None):
    """Imports an input file and returns a processed user_list

    Parameters
    ----------
    j: int
        the index of a .py input file that is in the format input_files/input_file_j.py
    fname: path
        path to a .xlsx input file
        if provided, overrides the loading of input_files/input_file_j.py

    Returns
    -------
    A list of User instances
    """

    # Back compatibility with old code
    if j is not None:
        file_module = importlib.import_module(f"ramp.input_files.input_file_{j}")
        user_list = file_module.User_list

    if fname is not None:
        usecase = UseCase()
        usecase.load(fname)
        user_list = usecase.users

    return user_list


def initialise_inputs(j=None, fname=None, num_profiles=None):
    """Loads the provided input file and prompt the user for number of profiles if not defined

    Parameters
    ----------
    j: int
        the index of a .py input file that is in the format input_files/input_file_j.py
    fname: path
        path to a .xlsx input file
        if provided, overrides the loading of input_files/input_file_j.py
    num_profiles: int
        the number of different usecase profiles which need to be generated

    Returns
    -------

    """

    year_behaviour = yearly_pattern()
    user_list = user_defined_inputs(j, fname)

    peak_enlarge = 0.15  # percentage random enlargement or reduction of peak time range length, corresponds to \delta_{peak} in [1], p.7

    if num_profiles is None:
        # asks the user how many profiles (i.e. code runs) they want
        num_profiles = int(
            input("please indicate the number of profiles to be generated: ")
        )
        print("Please wait...")

    return (peak_enlarge, year_behaviour, user_list, num_profiles)
