from code.strategy_helpers.validate_unified_data import validate_unified_traffic_data, validate_unified_vehicle_data, \
    validate_unified_link_data
from code.strategy_helpers.validation_helpers import check_mapping
from code.copert_hot_strategy.validate import validate_unified_los_speeds_data


def validate_pm_non_exhaust_unified_files(**kwargs):

    los_speeds_file = kwargs["unified_los_speeds"]
    vehicle_file = kwargs["unified_vehicle_data"]
    link_file = kwargs["unified_link_data"]
    traffic_file = kwargs["unified_traffic_data"]

    validate_unified_link_data(link_file)
    validate_unified_vehicle_data(vehicle_file)
    validate_unified_los_speeds_data(los_speeds_file)
    validate_unified_traffic_data(traffic_file)

    check_mapping(link_file, traffic_file, from_cols=["LinkID"], to_cols=["LinkID"])
    check_mapping(link_file, los_speeds_file, from_cols=["LinkID"], to_cols=["LinkID"])
    check_mapping(vehicle_file, los_speeds_file, from_cols=["VehicleCategory"], to_cols=["VehicleCategory"])
