from code.copert_hot_strategy.load_input_data import load_copert_input_data


def load_copert_cold_input_data(**kwargs):

    unified_data_file_paths = load_copert_input_data(**kwargs)

    unified_data_file_paths["unified_cold_ef_table"] = kwargs["input_cold_ef_table"]
    unified_data_file_paths["unified_vehicle_mapping"] = kwargs["input_vehicle_mapping"]

    return unified_data_file_paths