from code.data_loading.PMNonExhaustDataLoader import PMNonExhaustDataLoader
from code.strategy_helpers.helpers import save_dataframes


def load_pm_non_exhaust_berlin_format_data(**kwargs):

    output_folder = kwargs.get("output_folder_for_yeti_format_data", kwargs["output_folder"])

    loader = PMNonExhaustDataLoader(
        link_data_file=kwargs["berlin_format_link_data"],
        fleet_comp_file=kwargs["berlin_format_fleet_composition"],
        los_speeds_file=kwargs["berlin_format_los_speeds"],
        traffic_data_file=kwargs["berlin_format_traffic_data"]
    )
    (link_data, vehicle_data, traffic_data, los_speeds_data, _, _) = loader.load_data()

    yeti_format_data_file_paths = save_dataframes(
        output_folder,
        {
            "yeti_format_los_speeds": los_speeds_data,
            "yeti_format_vehicle_data": vehicle_data,
            "yeti_format_link_data": link_data,
            "yeti_format_traffic_data": traffic_data
        }
    )
    return yeti_format_data_file_paths