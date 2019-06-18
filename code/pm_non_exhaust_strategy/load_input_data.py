from code.data_loading.PMNonExhaustDataLoader import PMNonExhaustDataLoader
from code.strategy_helpers.helpers import save_dataframes


def load_pm_non_exhaust_input_data(**kwargs):

    output_folder = kwargs.get("output_folder_for_unified_data", kwargs["output_folder"])

    loader = PMNonExhaustDataLoader(
        link_data_file=kwargs["input_link_data"],
        fleet_comp_file=kwargs["input_fleet_composition"],
        los_speeds_file=kwargs["input_los_speeds"],
        traffic_data_file=kwargs["input_traffic_data"]
    )
    (link_data, vehicle_data, traffic_data, los_speeds_data, _, _) = loader.load_data()

    unified_data_file_paths = save_dataframes(
        output_folder,
        {
            "unified_los_speeds": los_speeds_data,
            "unified_vehicle_data": vehicle_data,
            "unified_link_data": link_data,
            "unified_traffic_data": traffic_data
        }
    )
    return unified_data_file_paths