import argparse

from ramp.ramp_run import run_usecase


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


if __name__ == "__main__":

    args = vars(parser.parse_args())
    fnames = args["fname_path"]
    num_profiles = args["num_profiles"]
    # Define which input files should be considered and run.

    if fnames is None:
        print("Please provide path to input file with option -i, \n\nDefault to old version of RAMP input files\n")
        # Files are specified as numbers in a list (e.g. [1,2] will consider input_file_1.py and input_file_2.py)
        from ramp.ramp_run import input_files_to_run

        if num_profiles is not None:
            if len(num_profiles) == 1:
                num_profiles = num_profiles * len(input_files_to_run)
            else:
                if len(num_profiles) != len(input_files_to_run):
                    raise ValueError(
                        "The number of profiles parameters  should match the number of input files provided")
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
