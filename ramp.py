import argparse
import datetime
import os.path
import time

import pandas as pd
import numpy as np
from ramp.ramp_run import run_usecase

BASE_PATH = os.path.dirname(os.path.abspath(__file__))

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

parser.add_argument(
    "-y",
    dest="years",
    nargs="+",
    type=int,
    help="Years for which one should generate demand profiles",
)

parser.add_argument(
    "--start-date",
    dest="date_start",
    type=datetime.date.fromisoformat,
    help="Date of start in YYYY-MM-DD format",
)

parser.add_argument(
    "--end-date",
    dest="date_end",
    type=datetime.date.fromisoformat,
    help="Date of end in YYYY-MM-DD format",
)

parser.add_argument(
    "--ext",
    dest="extension",
    type=str,
    help="Format of input files",
    default="xlsx"
)

if __name__ == "__main__":
    ts = time.time()
    args = vars(parser.parse_args())
    fnames = args["fname_path"]
    num_profiles = args["num_profiles"]
    # Define which input files should be considered and run.
    date_start = args["date_start"]
    date_end = args["date_end"]
    ext = args["extension"]

    years = args["years"]

    if date_start is None:
        if date_end is not None:
            date_start = datetime.date(date_end.year, 1, 1)
    else:
        if date_end is None:
            date_end = datetime.date(date_start.year, 12, 31)

    month_files = False

    if years is not None:
        if date_start is not None or date_end is not None:
            raise ValueError("You cannot use the option -y in combinaison with --date-start and/or --date-end")
        else:
            date_start = datetime.date(years[0], 1, 1)
            date_end = datetime.date(years[-1], 12, 31)
        if len(years) == 1 and fnames is not None:
            # This special combination (option -y with only 1 year and option -i with a directory as parameter)
            # Triggers the special mode "one input file per month"
            if os.path.isdir(fnames[0]):
                dir_path = fnames[0]
                fnames = [os.path.join(dir_path, f) for f in os.listdir(fnames[0]) if f.endswith(ext)]
                fnames.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))

                if len(fnames) == 12:
                    print("The following input files were found and will be used in this exact order for month inputs")
                    print("\n".join(fnames))
                    month_files = True
                    year = years[0]
                else:
                    raise ValueError(f"You want to simulate a whole year, yet the folder {dir_path} only contains {len(fnames)} out of the 12 monthes required")
            else:
                print("You selected a single year but the input path is not a folder.")


    if date_start is not None and date_end is not None:
        days = pd.date_range(start=date_start, end=date_end)
    else:
        days = None


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
        if month_files is True:
            year_profile = []
            for i, fname in enumerate(fnames):
                month_start = datetime.date(year, i+1, 1)
                month_end = datetime.date(year, i+1, pd.Period(month_start, freq="D").days_in_month)
                days = pd.date_range(start=month_start, end=month_end, freq='D')
                monthly_profiles = run_usecase(fname=fname, num_profiles=num_profiles[i], days=days, plot=False)
                year_profile.append(np.hstack(monthly_profiles))

            # Create a dataFrame to save the year profile with timestamps every minutes
            series_frame = pd.DataFrame(
                np.hstack(year_profile),
                index=pd.date_range(start=f"{year}-1-1", end=f"{year}-12-31 23:59", freq="T")
            )
            # Save to minute and hour resolution
            # TODO let the user choose where to save the files/file_name, make sure the user wants to overwrite the file
            # if it already exists
            series_frame.to_csv(os.path.join(BASE_PATH, 'yearly_profile_min_resolution.csv'))
            series_frame.resample("H").mean().to_csv(os.path.join(BASE_PATH, 'yearly_profile_hourly_resolution.csv'))
        else:
            for i, fname in enumerate(fnames):
                run_usecase(fname=fname, num_profiles=num_profiles[i], days=days)

    print(f" Time elapsed: {time.time()-ts}")