from code.hbefa_cold_strategy.load_berlin_format_data import load_hbefa_cold_berlin_format_data
from code.hbefa_hot_strategy.load_berlin_format_data import load_hbefa_hot_berlin_format_data
from code.script_helpers.dynamic_import_from import dynamic_import_from
from code.strategy_helpers.helpers import create_output_folder_if_necessary, remove_prefix_from_keys, \
    drop_keys_starting_with, add_prefix_to_keys


def load_hbefa_berlin_format_data(**kwargs):

    create_output_folder_if_necessary(**kwargs)

    if kwargs.get("only_hot") is True:
        kwargs = remove_prefix_from_keys("hot_", kwargs)
        return load_hbefa_hot_berlin_format_data(**kwargs)

    paths_to_hot_yeti_format_data = load_hot_data(**kwargs)
    paths_to_cold_yeti_format_data = load_cold_data(**kwargs)

    return {
        **paths_to_cold_yeti_format_data,
        **paths_to_hot_yeti_format_data
    }


def load_hot_data(**kwargs):

    kwargs_for_hot = drop_keys_starting_with("cold_", kwargs)
    kwargs_for_hot = remove_prefix_from_keys("hot_", kwargs_for_hot)

    kwargs_for_hot["output_folder"] = f"{kwargs_for_hot['output_folder']}/yeti_format_data_for_hot_strategy"

    paths_to_hot_yeti_format_data = load_hbefa_hot_berlin_format_data(**kwargs_for_hot)
    paths_to_hot_yeti_format_data = add_prefix_to_keys("hot", paths_to_hot_yeti_format_data)

    return paths_to_hot_yeti_format_data


def load_cold_data(**kwargs):

    load_cold_data_function = kwargs.get("cold_load_berlin_format_data_function")
    if load_cold_data_function is None:
        load_cold_berlin_format_data_function = load_hbefa_cold_berlin_format_data
    else:
        load_cold_berlin_format_data_function = dynamic_import_from(load_cold_data_function)

    kwargs_for_cold = drop_keys_starting_with("hot_", kwargs)
    kwargs_for_cold = remove_prefix_from_keys("cold_", kwargs_for_cold)

    kwargs_for_cold["output_folder"] = f"{kwargs_for_cold['output_folder']}/yeti_format_data_for_cold_strategy"

    paths_to_cold_yeti_format_data = load_cold_berlin_format_data_function(**kwargs_for_cold)
    paths_to_cold_yeti_format_data = add_prefix_to_keys("cold", paths_to_cold_yeti_format_data)

    return paths_to_cold_yeti_format_data