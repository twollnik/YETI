from code.data_loading.HbefaDataLoader import HbefaDataLoader
from code.strategy_helpers.helpers import save_dataframes


def load_hbefa_input_data(**kwargs):

    use_nh3_tier2_ef = False
    output_folder = kwargs.get("output_folder_for_unified_data", kwargs["output_folder"])

    loader = HbefaDataLoader(
        link_data_file=kwargs["input_link_data"],
        fleet_comp_file=kwargs["input_fleet_composition"],
        emission_factor_file=kwargs["input_emission_factors"],
        traffic_data_file=kwargs["input_traffic_data"]
    )
    data = loader.load_data(use_nh3_ef=use_nh3_tier2_ef)
    (link_data, vehicle_data, traffic_data, _, emission_factor_data, missing_ef_data) = data

    unified_data_file_paths = save_dataframes(
        output_folder,
        {
            "unified_emission_factors": emission_factor_data,
            "unified_vehicle_data": vehicle_data,
            "unified_link_data": link_data,
            "unified_traffic_data": traffic_data
        }
    )
    return unified_data_file_paths