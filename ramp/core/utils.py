import json
import random
import time
import datetime
import re
import os
import numpy as np
import pandas as pd
from openpyxl import load_workbook
from openpyxl.worksheet.cell_range import CellRange
from odf.table import Table
from odf.opendocument import load

POSSIBLE_FORMATS = """
    The possible formats of the power timeseries are :
        - a single value (int or float) if the power is constant throughout the load_profile (with random fluctuations if the variable 'thermal_p_var' is provided)
        - an array of value provided as text in a JSON array format, i.e. : [val1, val2, val3, ...]
        - a range of cells in another sheet of the input file (type '=' in the cell and then select the wished range of values to get the correct format automatically)

    ***Note***
    The last two formats will only accept one column (values only) or two columns (timestamps and values, respectively) and exactly 366 rows
    CSV file only accepts JSON array format for power timeseries.
"""


def read_input_file(filename):
    """Parse a RAMP input file based on its type (XLSX, ODS, CSV)"""
    _, file_extension = os.path.splitext(filename)
    if file_extension == ".xlsx":
        return read_excel_file(filename)
    elif file_extension == ".ods":
        return read_ods_file(filename)
    elif file_extension == ".csv":
        return read_csv_file(filename)
    else:
        raise ValueError(
            "Unsupported file format. Please provide 'xlsx', 'ods', or 'csv'."
        )


def read_excel_file(filename):
    """Parse a RAMP .xlsx input file"""

    wb = load_workbook(filename=filename)
    sheet_names = wb.sheetnames
    name = sheet_names[0]
    headers = [c.value for c in wb[name][1]]
    df = pd.DataFrame(tuple(wb[name].values)[1:], columns=headers)
    df = df.fillna(value=np.nan)

    df["p_series"] = False
    for i, v in enumerate(df["power"].values):
        if isinstance(v, str):
            appliance_name = df["name"].iloc[i]
            user_name = df["user_name"].iloc[i]
            # the timeseries is provided as a range of values in the spreadsheet
            if "=" in v:
                ts_sheet_name, ts_range = v.replace("=", "").split("!")
                cr = CellRange(ts_range)
                if cr.size["columns"] == 1:
                    ts = json.dumps(
                        [
                            wb[ts_sheet_name].cell(row=c[0], column=c[1]).value
                            for c in cr.cells
                        ]
                    )
                elif cr.size["columns"] == 2:
                    ts = pd.DataFrame(
                        [
                            [
                                wb[ts_sheet_name].cell(row=c[0], column=c[1]).value
                                for c in col
                            ]
                            for col in cr.cols
                        ]
                    ).T
                    ts = ts.to_json(orient="values")
                else:
                    raise (
                        ValueError(
                            f"The provided range for the power timeseries of the appliance '{appliance_name}' of user '{user_name} spans more than two columns in '{filename}' (range {ts_range} of sheet '{ts_sheet_name}')\n{POSSIBLE_FORMATS}"
                        )
                    )
                if cr.size["rows"] != 366:
                    raise (
                        ValueError(
                            f"The provided range for the power timeseries of the appliance '{appliance_name}' of user '{user_name}' in '{filename}' does not contain 366 values as expected  (range {ts_range} of sheet '{ts_sheet_name}')\n{POSSIBLE_FORMATS}"
                        )
                    )
            # the timeseries is expected as an array in json format
            else:
                try:
                    ts = json.loads(v)
                    if len(ts) != 366:
                        raise (
                            ValueError(
                                f"The provided power timeseries of the appliance '{appliance_name}' of user '{user_name}' in '{filename}' does not contain 366 values as expected\n{POSSIBLE_FORMATS}"
                            )
                        )
                    ts = v
                except json.JSONDecodeError:
                    raise (
                        ValueError(
                            f"Could not parse the power timeseries provided for appliance '{appliance_name}' of user '{user_name}' in '{filename}'\n{POSSIBLE_FORMATS}"
                        )
                    )
            df.loc[i, "power"] = ts
            df.loc[i, "p_series"] = True
    return df


def read_ods_file(filename):
    """Parse a RAMP .ods input file"""
    df = pd.read_excel(filename, engine="odf")
    doc = load(filename)

    # df = pd.DataFrame(data[1:], columns=headers)  # Skip header row
    df = df.fillna(value=np.nan)

    df["p_series"] = False
    for i, v in enumerate(df["power"].values):
        appliance_name = df["name"].iloc[i]
        user_name = df["user_name"].iloc[i]

        if isinstance(v, str):
            # the timeseries is provided as a range of values in the spreadsheet like "Sheet2!A2:B367"
            if "[" not in v:
                ts_sheet_name, ts_range = v.split(".")
                read_excel_args = range_string_to_pandas_read_excel_args(ts_range)

                if read_excel_args.get("nrows") != 366:
                    raise ValueError(
                        f"The provided range for the power timeseries of the appliance '{appliance_name}' of user '{user_name}' in '{filename}' does not contain 366 values as expected (range {ts_range} of sheet '{ts_sheet_name}')\n{POSSIBLE_FORMATS}"
                    )
                df_power = pd.read_excel(
                    filename,
                    engine="odf",
                    sheet_name=ts_sheet_name,
                    header=None,
                    **read_excel_args,
                )
                if df_power.shape[1] == 1:
                    ts = df_power.iloc[:, 0].to_json(orient="values")
                    print(f"=====ts: {ts}")
                elif df_power.shape[1] == 2:
                    ts = df_power.to_json(orient="values")
                else:
                    raise ValueError(
                        f"The provided range for the power timeseries of the appliance '{appliance_name}' of user '{user_name}' spans more than two columns in '{filename}' (range {ts_range} of sheet '{ts_sheet_name}')\n{POSSIBLE_FORMATS}"
                    )
            # the timeseries is expected as an array in json format
            else:
                try:
                    ts = json.loads(v)
                    if len(ts) != 366:
                        raise ValueError(
                            f"The provided power timeseries of the appliance '{appliance_name}' of user '{user_name}' in '{filename}' does not contain 366 values as expected\n{POSSIBLE_FORMATS}"
                        )
                    ts = v
                except json.JSONDecodeError:
                    raise ValueError(
                        f"Could not parse the power timeseries provided for appliance '{appliance_name}' of user '{user_name}' in '{filename}'\n{POSSIBLE_FORMATS}"
                    )
            df.loc[i, "power"] = ts
            df.loc[i, "p_series"] = True
    return df


def read_csv_file(filename):
    df = pd.read_csv(filename)
    df = df.fillna(value=np.nan)
    df["p_series"] = False

    def power_convertion(row):
        value = row["power"]
        try:
            row["power"] = int(value)
            return row
        except (ValueError, TypeError):
            try:
                power_list = json.loads(value)
            except:
                raise ValueError(
                    f"Could not parse the power timeseries provided in '{filename} at index {row.name}'\n{POSSIBLE_FORMATS}"
                )

            if len(power_list) != 366:
                raise ValueError(
                    f"The provided power timeseries does not contain 366 values as expected in '{filename} at index {row.name}'\n{POSSIBLE_FORMATS}"
                )

            row["p_series"] = True
            return row

    df = df.apply(power_convertion, axis=1)

    return df


def range_string_to_pandas_read_excel_args(cell_range):
    """Converts a range of cells (like format 'A2:B367') and returns corresponding
    arguments to use in pandas.read_excel method.
    """
    matches = re.findall(r"([A-Za-z]+)(\d+)", cell_range)
    if len(matches) != 2:
        raise ValueError(f"Expected 2 parts of cell range, got {len(matches)} parts.")

    return {
        "usecols": f"{matches[0][0]}:{matches[1][0]}",
        "skiprows": int(matches[0][1]) - 1,
        "nrows": int(matches[1][1]) - int(matches[0][1]) + 1,
    }


def random_variation(var, norm=1):
    """Pick a random variable within a uniform distribution of range [1-var, 1+var]

    Parameters
    ----------
    var: float
        sets the range of the uniform distribution around one
    norm: float
        multiplication factor of the random variable, default = 1

    Returns
    -------
    random number close to norm
    """
    return norm * random.uniform((1 - var), (1 + var))


def duty_cycle(var, t1, p1, t2, p2):
    """Assign a two period duty cycle

    concatenate an array where values equal p1 for a time (t1 +- random variation)
    followed by values equal to p2 for a time (t2 +- random variation)

    Parameters
    ----------
    var: float
        sets the range of the uniform distribution around t1 and t2
    t1: int
        time interval of the first part of the duty cycle in minutes
    p1: float
        power of the first part of the duty cycle in Watt
    t2: int
        time interval of the second part of the duty cycle in minutes
    p2: int
        power of the second part of the duty cycle in Watt

    Returns
    -------
    Power during each timestep of the duty cycle where p1 is repeated (t1 +- random variation) times and p2 is repeated (t2 +- random variation) times.
    The duty cycle is implicitly sampled every minutes (which is the unit for t1 and t2)
    """
    return np.concatenate(
        (
            np.ones(int(random_variation(var=-var, norm=t1))) * p1,
            np.ones(int(random_variation(var=-var, norm=t2))) * p2,
        )
    )


def range_within_window(range_low, range_high, window):
    """Compare a range with a window to see if there is an overlap

    The two cases where there is no overlap between two windows are when the
    range boundaries are both lower than the lowest window value or both
    higher than the highest window value

    """
    return not (
        (range_low < window[0] and range_high < window[0])
        or (range_low > window[1] and range_high > window[1])
    )


def random_choice(var, t1, p1, t2, p2):
    """Chooses one of two duty cycles randomly

    The choice is between a normal duty cycle and a reversed duty cycle (where t1 is swapped with t2 and p1 with p2)

    Parameters
    ----------
    var: float
        sets the range of the uniform distribution around t1 and t2
    t1: int
        time interval of the first part of the duty cycle in minutes
    p1: float
        power of the first part of the duty cycle in Watt
    t2: int
        time interval of the second part of the duty cycle in minutes
    p2: int
        power of the second part of the duty cycle in Watt

    Returns
    -------
    A duty cycle, see function duty_cycle
    """
    return random.choice(
        [
            duty_cycle(var, t1=t1, p1=p1, t2=t2, p2=p2),
            duty_cycle(var, t1=t2, p1=p2, t2=t1, p2=p1),
        ]
    )


def get_day_type(day):
    """Given a datetime object return 0 for weekdays or 1 for weekends"""

    if isinstance(day, str):
        day = datetime.date.fromisoformat(day)

    if day.weekday() > 4:
        answer = 1
    else:
        answer = 0
    return answer


def yearly_pattern(year=None):
    """
    Definition of a yearly pattern of weekends and weekdays, in case some appliances have specific wd/we behaviour
    If no argument is provided, the pattern always starts a monday and lasts 365 days, otherwise the pattern matches
    the weekdays and weekends of the provided year
    """
    if year is None:
        year_behaviour = np.zeros(365)
        year_behaviour[5:365:7] = 1
        year_behaviour[6:365:7] = 1
        year_behaviour = year_behaviour.tolist()
    else:
        # a list with 0 for weekdays and 1 for weekends
        year_behaviour = (
            pd.date_range(start=f"{year}-01-01", end=f"{year}-12-31", freq="D")
            .map(get_day_type)
            .to_list()
        )
    return year_behaviour


def within_peak_time_window(win_start, win_stop, peak_win_start, peak_win_stop):
    """Given determines if a switch on window falls within the peak time window"""
    answer = True
    # start and stop of the given window are both below the lower limit of peak time window
    if win_start < peak_win_start and win_stop < peak_win_start:
        answer = False
    # start and stop of the given window are both above the upper limit of peak time window
    if win_start > peak_win_stop and win_stop > peak_win_stop:
        answer = False
    return answer


def calc_time_taken(func):
    """Calculates the time elapsed during the execution of a function"""

    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(
            func.__name__
            + " required "
            + str((end - start) * 1)
            + " seconds for execution. "
        )
        return result

    return wrapper
