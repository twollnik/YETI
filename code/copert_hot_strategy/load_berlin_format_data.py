from code.data_loading.DataLoader import DataLoader
from code.strategy_helpers.helpers import save_dataframes


def load_copert_hot_berlin_format_data(**kwargs):

    use_nh3_tier2_ef = kwargs["use_nh3_tier2_ef"]
    output_folder = kwargs.get("output_folder_for_yeti_format_data", kwargs["output_folder"])

    loader = DataLoader(
        link_data_file=kwargs["berlin_format_link_data"],
        fleet_comp_file=kwargs["berlin_format_fleet_composition"],
        emission_factor_file=kwargs["berlin_format_emission_factors"],
        los_speeds_file=kwargs["berlin_format_los_speeds"],
        traffic_data_file=kwargs["berlin_format_traffic_data"],
        vehicle_mapping_file=kwargs["berlin_format_vehicle_mapping"],
        nh3_ef_file=kwargs.get("berlin_format_nh3_emission_factors"),
        nh3_mapping_file=kwargs.get("berlin_format_nh3_mapping")
    )
    data = loader.load_data(use_nh3_ef=use_nh3_tier2_ef)
    (link_data, vehicle_data, traffic_data, los_speeds_data, emission_factor_data, missing_ef_data) = data

    yeti_format_data_file_paths = save_dataframes(
        output_folder,
        {
            "yeti_format_emission_factors": emission_factor_data,
            "yeti_format_los_speeds": los_speeds_data,
            "yeti_format_vehicle_data": vehicle_data,
            "yeti_format_link_data": link_data,
            "yeti_format_traffic_data": traffic_data
         }
    )
    return yeti_format_data_file_paths