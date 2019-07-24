from code.hbefa_cold_strategy.load_berlin_format_data import load_hbefa_cold_berlin_format_data
from code.hbefa_hot_strategy.load_berlin_format_data import load_hbefa_hot_berlin_format_data
from code.strategy_helpers.helpers import remove_prefix_from_keys, create_output_folder_if_necessary, load_berlin_format_hot_data, \
    load_berlin_format_cold_data


def load_hbefa_berlin_format_data(**kwargs):

    create_output_folder_if_necessary(**kwargs)

    if kwargs.get("only_hot") is True:
        kwargs = remove_prefix_from_keys("hot_", kwargs)
        return load_hbefa_hot_berlin_format_data(**kwargs)

    paths_to_hot_yeti_format_data = load_berlin_format_hot_data(load_hbefa_hot_berlin_format_data, **kwargs)
    paths_to_cold_yeti_format_data = load_berlin_format_cold_data(load_hbefa_cold_berlin_format_data, **kwargs)

    return {
        **paths_to_cold_yeti_format_data,
        **paths_to_hot_yeti_format_data
    }
