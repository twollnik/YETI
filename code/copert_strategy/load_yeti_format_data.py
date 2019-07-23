from code.copert_cold_strategy.load_yeti_format_data import load_copert_cold_yeti_format_data
from code.copert_hot_strategy.load_yeti_format_data import load_copert_hot_yeti_format_data
from code.copert_strategy.copert_helpers import drop_keys_starting_with, remove_prefix_from_keys, add_prefix_to_keys
from code.script_helpers.dynamic_import_from import dynamic_import_from


def load_copert_yeti_format_data(**kwargs):

    if kwargs.get("only_hot") is True:
        return load_copert_hot_yeti_format_data(**kwargs)

    if "cold_strategy" in kwargs:

        hot_data = load_hot_data(**kwargs)
        cold_data = load_cold_data(**kwargs)

        return {
            **hot_data,
            **cold_data
        }

    return load_copert_cold_yeti_format_data(**kwargs)


def load_hot_data(**kwargs):

    kwargs_for_hot = drop_keys_starting_with("cold_", kwargs)
    kwargs_for_hot = remove_prefix_from_keys("hot_", kwargs_for_hot)

    hot_data = load_copert_hot_yeti_format_data(**kwargs_for_hot)
    hot_data = add_prefix_to_keys("hot", hot_data)

    return hot_data


def load_cold_data(**kwargs):

    load_cold_berlin_format_data_function = dynamic_import_from(kwargs["cold_load_yeti_format_data_function"])

    kwargs_for_cold = drop_keys_starting_with("hot_", kwargs)
    kwargs_for_cold = remove_prefix_from_keys("cold_", kwargs_for_cold)

    cold_data = load_cold_berlin_format_data_function(**kwargs_for_cold)
    cold_data = add_prefix_to_keys("cold", cold_data)

    return cold_data
