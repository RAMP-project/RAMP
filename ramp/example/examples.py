
import os
import pandas as pd


path = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
    )
)

available_data = {"shower":"shower_P.csv"}

def load_data(example:str) -> pd.DataFrame:

    if example not in available_data:
        raise ValueError(f"valid examples are {[*available_data]}")


    return pd.read_csv(
        f"{path}/{available_data[example]}"
    )


