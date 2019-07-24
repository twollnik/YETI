from code.data_loading.HbefaDataLoader import HbefaDataLoader
from code.strategy_helpers.helpers import save_dataframes


def load_hbefa_hot_berlin_format_data(**kwargs):

    output_folder = kwargs.get("output_folder_for_yeti_format_data", kwargs["output_folder"])

    loader = HbefaDataLoader(
        link_data_file=kwargs["berlin_format_link_data"],
        fleet_comp_file=kwargs["berlin_format_fleet_composition"],
        emission_factor_file=kwargs["berlin_format_emission_factors"],
        traffic_data_file=kwargs["berlin_format_traffic_data"]
    )
    data = loader.load_data(use_nh3_ef=False)
    (link_data, vehicle_data, traffic_data, _, emission_factor_data, missing_ef_data) = data

    yeti_format_data_file_paths = save_dataframes(
        output_folder,
        {
            "yeti_format_emission_factors": emission_factor_data,
            "yeti_format_vehicle_data": vehicle_data,
            "yeti_format_link_data": link_data,
            "yeti_format_traffic_data": traffic_data
        }
    )
    return yeti_format_data_file_paths