# -*- coding: utf-8 -*-
"""
"""

#%% Import required modules

import sys,os, importlib
sys.path.append('../')


from core.core import UseCase


def load_old_user_input_file(fname_path):
    """
    Imports an input file from a path and returns a processed User_list
    """

    print(os.path.sep)
    fname = fname_path.replace(".py", "").replace(os.path.sep, ".")
    output_fname = fname_path.replace(".py", "")
    file_module = importlib.import_module(fname)

    User_list = file_module.User_list

    UseCase(users=User_list).save(output_fname)

#Add your filepathes down there
print(load_old_user_input_file(os.path.join("input_files", "input_file_1.py")))
print(load_old_user_input_file("input_files/input_file_3.py"))