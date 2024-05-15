# %% Import required modules

import sys, os, importlib

sys.path.append("../")
import argparse
from ramp.core.core import UseCase

parser = argparse.ArgumentParser(
    prog="ramp_convert", description="Convert RAMP python input files to xlsx ones"
)
parser.add_argument(
    "-i",
    dest="fname_path",
    nargs="+",
    type=str,
    help="path to the input file (including filename)",
)
parser.add_argument(
    "-o", dest="output_path", type=str, help="path where to save the converted filename"
)
parser.add_argument(
    "--suffix",
    dest="suffix",
    type=str,
    help="suffix appended to the converted filename",
    default="",
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
    """Convert old RAMP python input files to xlsx ones

    The old (RAMP version < 0.5) .py input files defined all users and gathered them in a variable named User_list,
    this variable must be defined in the .py file to be converted to .xlsx.

    To convert a .py input file to an .xlsx using the UseCase objects, please refer to
    https://rampdemand.readthedocs.io/en/latest/examples/using_excel/using_excel.html#exporting-the-database

    Parameters
    ----------
    fname_path: path
        path to a .py ramp input file containing a variable named User_list
    output_path: path, optional
        path to the converted .xlsx ramp input file, by default the same folder as the .py file
    suffix: str, optional
        suffix to be added to the converted .xlsx ramp input file name, default ''
    keep_names: bool, optional
        keep the variable names of the Appliance instances as their 'name' attribute, default True

    """

    line_to_change = -1

    # Check if the lines to save the names of the Appliance instances is already there
    # And check if the import of the User class is correct, otherwise adapt the file
    with open(fname_path, "r") as fp:
        lines = fp.readlines()
        if "# Code automatically added by ramp_convert_old_input_files.py\n" in lines:
            keep_names = False
        for i, l in enumerate(lines):
            if "from core import" in l:
                line_to_change = i
        # Change import statement by explicitly naming the full package path
        lines[line_to_change] = lines[line_to_change].replace(
            "from core import", "from ramp.core.core import"
        )

    # Modify import statement in file
    if line_to_change != -1:
        with open(fname_path, "w") as fp:
            fp.writelines(lines)

    # Add code to the input file to assign the variable name of the Appliance instances to their name attribute
    if keep_names is True:
        with open(fname_path, "a") as fp:
            fp.write(convert_names)

    fname = fname_path.replace(".py", "").replace(os.path.sep, ".")

    if output_path is None:
        output_path = os.path.dirname(fname_path)
    output_fname = fname_path.split(os.path.sep)[-1].replace(".py", suffix)
    output_fname = os.path.join(output_path, output_fname)

    if os.name != "posix":
        sys.path.insert(0, os.path.dirname(os.path.abspath(fname_path)))
    file_module = importlib.import_module(fname)

    user_list = file_module.User_list

    UseCase(users=user_list).save(output_fname)


def cli():
    args = vars(parser.parse_args())
    fname = args["fname_path"]
    output_path = args.get("output_path")
    suffix = args.get("suffix")

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


if __name__ == "__main__":
    cli()
