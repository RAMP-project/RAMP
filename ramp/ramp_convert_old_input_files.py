#%% Import required modules

import sys, os, importlib

sys.path.append("../")
import argparse
from ramp.core.core import UseCase

parser = argparse.ArgumentParser(
    prog="python ramp_convert_old_input_files.py",
    description="Convert old python input files to xlsx ones",
)
parser.add_argument(
    "-i",
    dest="fname_path",
    nargs="+",
    type=str,
    help="path to the input file (including filename)",
)
parser.add_argument(
    "-o",
    dest="output_path",
    nargs=1,
    type=str,
    help="path where to save the converted filename",
)
parser.add_argument(
    "--suffix",
    dest="suffix",
    nargs=1,
    type=str,
    help="suffix appended to the converted filename",
)


convert_names = """
# Code automatically added by ramp_convert_old_input_files.py
from ramp.core.core import Appliance
local_var_names = [(i, a) for i, a in locals().items() if isinstance(a, Appliance)]
for i, a in local_var_names:
    a.name = i
"""


def convert_old_user_input_file(
    fname_path, output_path=None, suffix="", keep_names=True
):
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

    if output_path is None:
        output_path = os.path.dirname(fname_path)
    output_fname = fname_path.split(os.path.sep)[-1].replace(".py", suffix)
    output_fname = os.path.join(output_path, output_fname)

    if "ramp" not in fname:
        fname = f"ramp.{fname}"
    file_module = importlib.import_module(fname)

    user_list = file_module.User_list

    UseCase(users=user_list).save(output_fname)


if __name__ == "__main__":

    args = vars(parser.parse_args())
    fname = args["fname_path"]
    output_path = args.get("output_path")
    suffix = args.get("suffix")

    if output_path is not None:
        output_path = output_path[0]

    if suffix is None:
        suffix = ""
    else:
        suffix = suffix[0]

    if fname is None:
        print("Please provide path to input file with option -i")
    else:
        if isinstance(fname, list):
            fnames = fname
            for fname in fnames:
                convert_old_user_input_file(
                    fname, output_path=output_path, suffix=suffix
                )
        else:
            convert_old_user_input_file(fname, output_path=output_path, suffix=suffix)
