from code.hbefa_cold_strategy.load_yeti_format_data import load_hbefa_cold_yeti_format_data
from code.hbefa_hot_strategy.load_yeti_format_data import load_hbefa_hot_yeti_format_data
from code.strategy_helpers.helpers import remove_prefix_from_keys, \
    load_yeti_format_hot_data, load_yeti_format_cold_data


def load_hbefa_yeti_format_data(**kwargs):

    if kwargs.get("only_hot") is True:
        kwargs = remove_prefix_from_keys("hot_", kwargs)
        return load_hbefa_hot_yeti_format_data(**kwargs)

    hot_data = load_yeti_format_hot_data(load_hbefa_hot_yeti_format_data, **kwargs)
    cold_data = load_yeti_format_cold_data(load_hbefa_cold_yeti_format_data, **kwargs)

    return {
        **hot_data,
        **cold_data
    }
