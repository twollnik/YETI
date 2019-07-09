from code.data_loading.HbefaColdDataLoader import HbefaColdDataLoader
from code.strategy_helpers.helpers import save_dataframes


def load_hbefa_cold_input_data(**kwargs):

    output_folder = kwargs.get("output_folder_for_unified_data", kwargs["output_folder"])

    loader = HbefaColdDataLoader(
        link_data_file=kwargs["input_link_data"],
        fleet_comp_file=kwargs["input_fleet_composition"],
        emission_factor_file=kwargs["input_emission_factors"],
        cold_starts_file=kwargs["input_cold_starts_data"]
    )
    data = loader.load_data(use_nh3_ef=False)
    (link_data, vehicle_data, cold_starts_data, _, emission_factor_data, _) = data

    unified_data_file_paths = save_dataframes(
        output_folder,
        {
            "unified_emission_factors": emission_factor_data,
            "unified_vehicle_data": vehicle_data,
            "unified_link_data": link_data,
            "unified_cold_starts_data": cold_starts_data
        }
    )
    return unified_data_file_paths