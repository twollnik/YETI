from code.hbefa_cold_strategy.load_yeti_format_data import load_hbefa_cold_yeti_format_data
from code.hbefa_hot_strategy.load_yeti_format_data import load_hbefa_hot_yeti_format_data
from code.strategy_helpers.helpers import load_yeti_format_data_for_composed_strategy


def load_hbefa_yeti_format_data(**kwargs):

    default_hot_load_function = load_hbefa_hot_yeti_format_data
    default_cold_load_function = load_hbefa_cold_yeti_format_data

    return load_yeti_format_data_for_composed_strategy(
        default_cold_load_function, default_hot_load_function, **kwargs)