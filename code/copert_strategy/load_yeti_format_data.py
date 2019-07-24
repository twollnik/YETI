from code.copert_cold_strategy.load_yeti_format_data import load_copert_cold_yeti_format_data
from code.copert_hot_strategy.load_yeti_format_data import load_copert_hot_yeti_format_data
from code.strategy_helpers.helpers import remove_prefix_from_keys, \
    load_yeti_format_hot_data, load_yeti_format_cold_data


def load_copert_yeti_format_data(**kwargs):

    if kwargs.get("only_hot") is True:
        kwargs = remove_prefix_from_keys("hot_", kwargs)
        return load_copert_hot_yeti_format_data(**kwargs)

    if "cold_strategy" in kwargs:

        hot_data = load_yeti_format_hot_data(load_copert_hot_yeti_format_data, **kwargs)
        cold_data = load_yeti_format_cold_data(load_copert_cold_yeti_format_data, **kwargs)

        return {
            **hot_data,
            **cold_data
        }

    return load_copert_cold_yeti_format_data(**kwargs)
