from datetime import datetime
from typing import Dict

import pandas as pd


def save_dataframes(output_folder: str, data_dict: Dict[str, pd.DataFrame]) -> Dict[str, str]:

    output_folder = output_folder[:-1] if output_folder[-1] == "/" else output_folder
    for name, dataframe in data_dict.items():
        file = f"{output_folder}/{name}"
        if file.endswith(".csv") is False:
            file = file + ".csv"
        dataframe.to_csv(file)
        data_dict[name] = file
    return data_dict


def get_timestamp(short: bool = False) -> str:
    if short is True:
        return datetime.now().strftime('%Hh:%Mmin')
    else:
        return datetime.now().strftime("%Y-%m-%d_%Hh-%Mmin")