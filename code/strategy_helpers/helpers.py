import logging
import os
from copy import copy
from datetime import datetime
from typing import Dict

import pandas as pd

from code.script_helpers.dynamic_import_from import dynamic_import_from


def save_dataframes(output_folder: str, data_dict: Dict[str, pd.DataFrame]) -> Dict[str, str]:

    output_folder = output_folder[:-1] if output_folder[-1] == "/" else output_folder
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)

    for name, dataframe in data_dict.items():
        file = f"{output_folder}/{name}"
        if file.endswith(".csv") is False:
            file = file + ".csv"
        dataframe.to_csv(file, index=False)
        data_dict[name] = file
    return data_dict


def get_timestamp(short: bool = False) -> str:
    if short is True:
        return datetime.now().strftime('%Hh:%Mmin')
    else:
        return datetime.now().strftime("%Y-%m-%d_%Hh-%Mmin")


def load_berlin_format_data_for_composed_strategy(default_cold_load_function, default_hot_load_function, **kwargs):

    output_folder = kwargs.get("output_folder_for_yeti_format_data", kwargs["output_folder"])
    create_output_folder_if_necessary(output_folder)

    if kwargs.get("only_hot") is True:
        kwargs = remove_prefix_from_keys("hot_", kwargs)
        return default_hot_load_function(**kwargs)

    logging.debug("Converting berlin_format data to yeti_format data for the hot Strategy.")
    paths_to_hot_yeti_format_data = load_berlin_format_hot_data(default_hot_load_function, output_folder, **kwargs)

    logging.debug("Converting berlin_format data to yeti_format data for the cold Strategy.")
    paths_to_cold_yeti_format_data = load_berlin_format_cold_data(default_cold_load_function, output_folder, **kwargs)

    return {
        **paths_to_cold_yeti_format_data,
        **paths_to_hot_yeti_format_data
    }


def create_output_folder_if_necessary(output_folder):

    if output_folder is None:
        return None

    if not os.path.exists(output_folder):
        os.mkdir(output_folder)


def load_berlin_format_hot_data(load_data_function, output_folder_for_yeti_data, **kwargs):

    kwargs_for_hot = drop_keys_starting_with("cold_", kwargs)
    kwargs_for_hot = remove_prefix_from_keys("hot_", kwargs_for_hot)

    kwargs_for_hot["output_folder_for_yeti_format_data"] = f"{output_folder_for_yeti_data}/yeti_format_data_for_hot_strategy"

    paths_to_hot_yeti_format_data = load_data_function(**kwargs_for_hot)
    paths_to_hot_yeti_format_data = add_prefix_to_keys("hot", paths_to_hot_yeti_format_data)

    return paths_to_hot_yeti_format_data


def load_berlin_format_cold_data(default_load_data_function, output_folder_for_yeti_data, **kwargs):

    load_cold_data_function = kwargs.get("cold_load_berlin_format_data_function")
    if load_cold_data_function is None:
        load_cold_berlin_format_data_function = default_load_data_function
    else:
        load_cold_berlin_format_data_function = dynamic_import_from(load_cold_data_function)

    kwargs_for_cold = drop_keys_starting_with("hot_", kwargs)
    kwargs_for_cold = remove_prefix_from_keys("cold_", kwargs_for_cold)

    kwargs_for_cold["output_folder_for_yeti_format_data"] = f"{output_folder_for_yeti_data}/yeti_format_data_for_cold_strategy"

    paths_to_cold_yeti_format_data = load_cold_berlin_format_data_function(**kwargs_for_cold)
    paths_to_cold_yeti_format_data = add_prefix_to_keys("cold", paths_to_cold_yeti_format_data)

    return paths_to_cold_yeti_format_data


def load_yeti_format_data_for_composed_strategy(default_cold_load_function, default_hot_load_function, **kwargs):

    if kwargs.get("only_hot") is True:
        kwargs = remove_prefix_from_keys("hot_", kwargs)
        return default_hot_load_function(**kwargs)

    logging.debug("Loading yeti_format data for the hot Strategy.")
    hot_data = load_yeti_format_hot_data(default_hot_load_function, **kwargs)

    logging.debug("Loading yeti_format data for the cold Strategy.")
    cold_data = load_yeti_format_cold_data(default_cold_load_function, **kwargs)

    return {
        **hot_data,
        **cold_data
    }


def load_yeti_format_hot_data(load_data_function, **kwargs):

    kwargs_for_hot = drop_keys_starting_with("cold_", kwargs)
    kwargs_for_hot = remove_prefix_from_keys("hot_", kwargs_for_hot)

    hot_data = load_data_function(**kwargs_for_hot)

    return hot_data


def load_yeti_format_cold_data(default_load_data_function, **kwargs):

    load_cold_data_function = kwargs.get("cold_load_yeti_format_data_function")
    if load_cold_data_function is None:
        load_cold_yeti_format_data_function = default_load_data_function
    else:
        load_cold_yeti_format_data_function = dynamic_import_from(load_cold_data_function)

    kwargs_for_cold = drop_keys_starting_with("hot_", kwargs)
    kwargs_for_cold = remove_prefix_from_keys("cold_", kwargs_for_cold)

    cold_data = load_cold_yeti_format_data_function(**kwargs_for_cold)
    cold_data = add_prefix_to_keys("cold", cold_data)

    return cold_data


def drop_keys_starting_with(starting_chars, dict):

    return {key: value for key, value in dict.items() if not key.startswith(starting_chars)}


def remove_prefix_from_keys(prefix, dict):

    output_dict = copy(dict)

    for key, value in list(output_dict.items()):
        if key.startswith(prefix):
            del output_dict[key]
            output_dict[key[len(prefix):]] = value
    return output_dict


def add_prefix_to_keys(prefix, paths_to_cold_yeti_format_data):

    return {f"{prefix}_{key}": value for key, value in list(paths_to_cold_yeti_format_data.items())}
