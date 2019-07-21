import logging

from code.strategy_helpers.validate_yeti_format_data import validate_yeti_format_traffic_data, \
    validate_yeti_format_vehicle_data, \
    validate_yeti_format_link_data

from code.copert_hot_strategy.validate import validate_yeti_format_los_speeds_data
from code.strategy_helpers.validation_helpers import validate_dataset, check_mapping


def validate_pm_non_exhaust_berlin_format_files(**kwargs):

    fleet_comp_file = kwargs["berlin_format_fleet_composition"]
    link_data_file = kwargs["berlin_format_link_data"]
    traffic_data_file = kwargs["berlin_format_traffic_data"]
    los_speeds_file = kwargs["berlin_format_los_speeds"]

    logging.debug(f"Files to be validated: \n"
                  f"\t{link_data_file}\n"
                  f"\t{fleet_comp_file}\n"
                  f"\t{traffic_data_file}\n"
                  f"\t{los_speeds_file}\n")

    validate_dataset(fleet_comp_file, "FLEET_COMP")
    validate_dataset(link_data_file, "SHAPE")
    validate_dataset(traffic_data_file, "TRAFFIC_COUNT")
    validate_dataset(los_speeds_file, "LOS_SPEED")

    check_mapping(link_data_file, traffic_data_file, from_cols=["LinkID"], to_cols=["LinkID"])


def validate_pm_non_exhaust_yeti_format_files(**kwargs):

    los_speeds_file = kwargs["yeti_format_los_speeds"]
    vehicle_file = kwargs["yeti_format_vehicle_data"]
    link_file = kwargs["yeti_format_link_data"]
    traffic_file = kwargs["yeti_format_traffic_data"]

    validate_yeti_format_link_data(link_file)
    validate_yeti_format_vehicle_data(vehicle_file)
    validate_yeti_format_los_speeds_data(los_speeds_file)
    validate_yeti_format_traffic_data(traffic_file)

    check_mapping(link_file, traffic_file, from_cols=["LinkID"], to_cols=["LinkID"])
    check_mapping(link_file, los_speeds_file, from_cols=["LinkID"], to_cols=["LinkID"])
    check_mapping(vehicle_file, los_speeds_file, from_cols=["VehicleCategory"], to_cols=["VehicleCategory"])
