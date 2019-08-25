from code.copert_hot_strategy.load_berlin_format_data import load_copert_hot_berlin_format_data


def load_copert_cold_berlin_format_data(**kwargs):

    # The config parameter use_nh3_tier2_ef is not required by the CopertColdStrategy,
    # but is needed for the load_copert_hot_berlin_format_data function.
    kwargs["use_nh3_tier2_ef"] = False

    yeti_format_data_file_paths = load_copert_hot_berlin_format_data(**kwargs)

    yeti_format_data_file_paths["yeti_format_cold_ef_table"] = kwargs["berlin_format_cold_ef_table"]
    yeti_format_data_file_paths["yeti_format_vehicle_mapping"] = kwargs["berlin_format_vehicle_mapping"]

    return yeti_format_data_file_paths