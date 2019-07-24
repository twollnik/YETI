from code.hbefa_cold_strategy.load_yeti_format_data import load_hbefa_cold_yeti_format_data
from code.hbefa_hot_strategy.load_yeti_format_data import load_hbefa_hot_yeti_format_data
from code.script_helpers.dynamic_import_from import dynamic_import_from
from code.strategy_helpers.helpers import remove_prefix_from_keys, \
    drop_keys_starting_with, add_prefix_to_keys


def load_hbefa_yeti_format_data(**kwargs):

    if kwargs.get("only_hot") is True:
        kwargs = remove_prefix_from_keys("hot_", kwargs)
        return load_hbefa_hot_yeti_format_data(**kwargs)

    hot_data = load_hot_data(**kwargs)
    cold_data = load_cold_data(**kwargs)

    return {
        **hot_data,
        **cold_data
    }


def load_hot_data(**kwargs):

    kwargs_for_hot = drop_keys_starting_with("cold_", kwargs)
    kwargs_for_hot = remove_prefix_from_keys("hot_", kwargs_for_hot)

    hot_data = load_hbefa_hot_yeti_format_data(**kwargs_for_hot)

    return hot_data


def load_cold_data(**kwargs):

    load_cold_data_function = kwargs.get("cold_load_yeti_format_data_function")
    if load_cold_data_function is None:
        load_cold_yeti_format_data_function = load_hbefa_cold_yeti_format_data
    else:
        load_cold_yeti_format_data_function = dynamic_import_from(load_cold_data_function)

    kwargs_for_cold = drop_keys_starting_with("hot_", kwargs)
    kwargs_for_cold = remove_prefix_from_keys("cold_", kwargs_for_cold)

    cold_data = load_cold_yeti_format_data_function(**kwargs_for_cold)
    cold_data = add_prefix_to_keys("cold", cold_data)

    return cold_data