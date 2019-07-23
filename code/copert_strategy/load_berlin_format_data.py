from code.copert_cold_strategy.load_berlin_format_data import load_copert_cold_berlin_format_data
from code.copert_hot_strategy.load_berlin_format_data import load_copert_hot_berlin_format_data
from code.script_helpers.dynamic_import_from import dynamic_import_from


def load_copert_berlin_format_data(**kwargs):

    if kwargs.get("only_hot") is True:
        return load_copert_hot_berlin_format_data(**kwargs)

    elif "cold_strategy" in kwargs:

        paths_to_hot_yeti_format_data = load_hot_data(**kwargs)
        paths_to_cold_yeti_format_data = load_cold_data(**kwargs)

        return {
            **paths_to_cold_yeti_format_data,
            **paths_to_hot_yeti_format_data
        }

    return load_copert_cold_berlin_format_data(**kwargs)


def load_hot_data(**kwargs):

    kwargs_for_hot = drop_keys_starting_with("cold_", kwargs)
    kwargs_for_hot = remove_prefix_from_keys("hot_", kwargs_for_hot)

    paths_to_hot_yeti_format_data = load_copert_hot_berlin_format_data(**kwargs_for_hot)
    paths_to_hot_yeti_format_data = add_prefix_to_keys("hot", paths_to_hot_yeti_format_data)

    return paths_to_hot_yeti_format_data


def drop_keys_starting_with(starting_chars, dict):
    return {key: value for key, value in dict.items() if not key.startswith(starting_chars)}


def remove_prefix_from_keys(prefix, dict):
    for key, value in list(dict.items()):
        if key.startswith(prefix):
            del dict[key]
            dict[key[len(prefix):]] = value
    return dict


def load_cold_data(**kwargs):

    load_cold_berlin_format_data_function = dynamic_import_from(kwargs["cold_load_berlin_format_data_function"])

    kwargs_for_cold = drop_keys_starting_with("hot_", kwargs)
    kwargs_for_cold = remove_prefix_from_keys("cold_", kwargs_for_cold)

    paths_to_cold_yeti_format_data = load_cold_berlin_format_data_function(**kwargs_for_cold)
    paths_to_cold_yeti_format_data = add_prefix_to_keys("cold", paths_to_cold_yeti_format_data)

    return paths_to_cold_yeti_format_data


def add_prefix_to_keys(prefix, paths_to_cold_yeti_format_data):

    return {f"{prefix}_{key}": value for key, value in list(paths_to_cold_yeti_format_data.items())}

# TODO: handle naming conflicts in yeti_format output files