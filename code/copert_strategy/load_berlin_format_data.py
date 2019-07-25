from code.copert_cold_strategy.load_berlin_format_data import load_copert_cold_berlin_format_data
from code.copert_hot_strategy.load_berlin_format_data import load_copert_hot_berlin_format_data
from code.strategy_helpers.helpers import load_berlin_format_data_for_composed_strategy


def load_copert_berlin_format_data(**kwargs):

    default_hot_load_function = load_copert_hot_berlin_format_data
    default_cold_load_function = load_copert_cold_berlin_format_data

    return load_berlin_format_data_for_composed_strategy(
        default_cold_load_function, default_hot_load_function, **kwargs)