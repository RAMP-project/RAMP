#%% Import required modules
import sys,os, importlib
sys.path.append('../')
import argparse
from core.core import UseCase

parser = argparse.ArgumentParser(
    prog="python ramp_convert_old_input_files.py", description="Convert old python input files to xlsx ones"
)
parser.add_argument(
    "-i",
    dest="fname_path",
    nargs="+",
    type=str,
    help="path to the input file (including filename)",
)


convert_names = """
# Code automatically added by ramp_convert_old_input_files.py
from ramp.core.core import Appliance
local_var_names = [(i, a) for i, a in locals().items() if isinstance(a, Appliance)]
for i, a in local_var_names:
    a.name = i
"""


def convert_old_user_input_file(fname_path, keep_names=True):
    """
    Imports an input file from a path and returns a processed User_list
    """

    # Check if the lines to save the names of the Appliance instances is already there
    with open(fname_path, "r") as fp:
        lines = fp.readlines()
        if "# Code automatically added by ramp_convert_old_input_files.py\n" in lines:
            keep_names = False

    # Add code to the input file to assign the variable name of the Appliance instances to their name attribute
    if keep_names is True:
        with open(fname_path, "a") as fp:
            fp.write(convert_names)

    fname = fname_path.replace(".py", "").replace(os.path.sep, ".")
    output_fname = fname_path.replace(".py", "")
    file_module = importlib.import_module(fname)

    User_list = file_module.User_list

    UseCase(users=User_list).save(output_fname)


if __name__ == "__main__":

    args = vars(parser.parse_args())
    fname = args["fname_path"]
    if fname is None:
        print("Please provide path to input file with option -i")
    else:
        if isinstance(fname, list):
            fnames = fname
            for fname in fnames:
                convert_old_user_input_file(fname)
        else:
            convert_old_user_input_file(fname)
