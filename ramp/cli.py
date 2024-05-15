import argparse
import datetime
import os.path

import pandas as pd
import numpy as np
from ramp.ramp_run import run_usecase

BASE_PATH = os.path.dirname(os.path.abspath(__file__))

parser = argparse.ArgumentParser(
    prog="ramp",
    description="Execute RAMP code",
    epilog="To convert '.py' input files into '.xlsx' input files use the command 'ramp_convert'",
)
parser.add_argument(
    "-i",
    dest="fname_path",
    nargs="+",
    type=str,
    help="Path to the (.xlsx/.py) input files (including filename). Must be provided",
)
parser.add_argument(
    "-o",
    dest="ofname_path",
    nargs="+",
    type=str,
    help=f"Path to the csv output files (including filename). If not provided, default output will be provided in {os.path.join(BASE_PATH, 'results')}",
)
parser.add_argument(
    "-n",
    dest="num_days",
    nargs="+",
    type=int,
    help="Number of daily profiles to be generated",
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
    help="Format of input files for monthly variability (only used in combination with -y option and when -i path is a directory)",
    default="xlsx",
)

parser.add_argument(
    "-p",
    dest="parallel",
    default=False,
    const=True,
    nargs="?",
    type=bool,
    help="Whether or not the simulation uses parallel processing",
)


def main():
    args = vars(parser.parse_args())
    fnames = args["fname_path"]
    ofnames = args["ofname_path"]
    num_days = args["num_days"]
    # Define which input files should be considered and run.
    date_start = args["date_start"]
    date_end = args["date_end"]
    ext = args["extension"]
    parallel_processing = args["parallel"]

    years = args["years"]

    if num_days is None:
        if date_start is None:
            if date_end is not None:
                date_start = datetime.date(date_end.year, 1, 1)
                # logging.info
                print(
                    f"You did not provide a start date, this is chosen automatically for you: {date_start}"
                )

        else:
            if date_end is None:
                date_end = datetime.date(date_start.year, 12, 31)
                # logging.info
                print(
                    f"You did not provide an end date, this is chosen automatically for you: {date_end}"
                )

    month_files = False

    if years is not None:
        if date_start is not None or date_end is not None:
            raise ValueError(
                "You cannot use the option -y in combinaison with --date-start and/or --date-end"
            )
        else:
            date_start = datetime.date(years[0], 1, 1)
            date_end = datetime.date(years[-1], 12, 31)
        if len(years) == 1 and fnames is not None:
            # This special combination (option -y with only 1 year and option -i with a directory as parameter)
            # Triggers the special mode "one input file per month"
            if os.path.isdir(fnames[0]):
                dir_path = fnames[0]
                fnames = [
                    os.path.join(dir_path, f)
                    for f in os.listdir(fnames[0])
                    if f.endswith(ext)
                ]
                fnames.sort(key=lambda f: int("".join(filter(str.isdigit, f))))

                if len(fnames) == 12:
                    print(
                        "The following input files were found and will be used in this exact order for month inputs"
                    )
                    print("\n".join(fnames))
                    month_files = True
                    year = years[0]
                else:
                    raise ValueError(
                        f"You want to simulate a whole year, yet the folder {dir_path} only contains {len(fnames)} out of the 12 monthes required"
                    )
            else:
                print("You selected a single year but the input path is not a folder.")

    if ofnames is None:
        ofnames = [None]

    if fnames is None:
        print("Please provide path to input file with option -i, \n\n")
    else:
        if num_days is not None:
            if len(num_days) == 1:
                num_days = num_days * len(fnames)
            else:
                if len(num_days) != len(fnames):
                    raise ValueError(
                        "The number of profiles parameters  should match the number of input files provided"
                    )
        else:
            num_days = [None] * len(fnames)

        if month_files is False:
            if len(ofnames) == 1:
                ofnames = ofnames * len(fnames)
            elif len(fnames) != len(ofnames):
                raise ValueError(
                    f"The number of output file paths({len(ofnames)}) should match the number of input files paths ({len(fnames)})"
                )

            for i, fname in enumerate(fnames):
                run_usecase(
                    fname=fname,
                    ofname=ofnames[i],
                    num_days=num_days[i],
                    date_start=date_start,
                    date_end=date_end,
                    plot=True,
                    parallel=parallel_processing,
                )
        else:
            year_profile = []
            for i, fname in enumerate(fnames):
                month_start = datetime.date(year, i + 1, 1)
                month_end = datetime.date(
                    year, i + 1, pd.Period(month_start, freq="D").days_in_month
                )
                month_profiles = run_usecase(
                    fname=fname,
                    ofname=None,
                    num_days=num_days[i],
                    date_start=month_start,
                    date_end=month_end,
                    plot=False,
                    parallel=parallel_processing,
                )
                month_profiles = month_profiles.reshape(
                    1, 1440 * month_profiles.shape[0]
                ).squeeze()
                year_profile.append(month_profiles)

            # Create a dataFrame to save the year profile with timestamps every minutes
            series_frame = pd.DataFrame(
                np.hstack(year_profile),
                index=pd.date_range(
                    start=f"{year}-1-1", end=f"{year}-12-31 23:59", freq="min"
                ),
            )
            # Save to minute and hour resolution
            if len(ofnames) == 1:
                ofname = ofnames[0]
            else:
                ofname = None

            if ofname is None:
                ofname = os.path.abspath(os.path.curdir)

            if not os.path.exists(ofname):
                os.mkdir(ofname)

            series_frame.to_csv(
                os.path.join(ofname, "yearly_profile_min_resolution.csv")
            )
            resampled = pd.DataFrame()

            resampled["mean"] = series_frame.resample("h").mean()
            resampled["max"] = series_frame.resample("h").max()
            resampled["min"] = series_frame.resample("h").min()
            # TODO add more columns with other resampled functions (do this in Jupyter)
            resampled.to_csv(
                os.path.join(ofname, "yearly_profile_hourly_resolution.csv")
            )
            print(
                f"Results of the yearly RAMP simulation with seasonality are located in the folder {ofname}"
            )


if __name__ == "__main__":
    main()
