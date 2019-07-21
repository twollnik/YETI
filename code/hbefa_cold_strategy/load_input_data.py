from code.data_loading.HbefaColdDataLoader import HbefaColdDataLoader
from code.strategy_helpers.helpers import save_dataframes


def load_hbefa_cold_berlin_format_data(**kwargs):

    output_folder = kwargs.get("output_folder_for_yeti_format_data", kwargs["output_folder"])

    loader = HbefaColdDataLoader(
        link_data_file=kwargs["berlin_format_link_data"],
        fleet_comp_file=kwargs["berlin_format_fleet_composition"],
        emission_factor_file=kwargs["berlin_format_emission_factors"],
        cold_starts_file=kwargs["berlin_format_cold_starts_data"]
    )
    data = loader.load_data(use_nh3_ef=False)
    (link_data, vehicle_data, cold_starts_data, _, emission_factor_data, _) = data

    yeti_format_data_file_paths = save_dataframes(
        output_folder,
        {
            "yeti_format_emission_factors": emission_factor_data,
            "yeti_format_vehicle_data": vehicle_data,
            "yeti_format_link_data": link_data,
            "yeti_format_cold_starts_data": cold_starts_data
        }
    )
    return yeti_format_data_file_paths