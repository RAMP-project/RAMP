import os
import pandas as pd
import shutil

path = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
    )
)

available_data = {"shower": "shower_P.csv"}


def load_data(example: str) -> pd.DataFrame:
    if example not in available_data:
        raise ValueError(f"valid examples are {[*available_data]}")

    return pd.read_csv(f"{path}/{available_data[example]}")


def download_example(destination: str):
    """Copies the model files from the ramp package to a given path
    Parameters
    -----------
    destination : str
        The path to copy the model files.
    """
    files = [
        "input_file_1.py",
        "input_file_2.py",
        "input_file_3.py",
        "shower_P.csv",
        "daily_T.csv",
        "T_gw.csv",
    ]

    for file in files:
        shutil.copyfile(src=f"{path}/{file}", dst=f"{destination}/{file}")
