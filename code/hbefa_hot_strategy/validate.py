import logging

import pandas as pd
from code.strategy_helpers.validate_yeti_format_data import validate_yeti_format_link_data, \
    validate_yeti_format_vehicle_data, \
    validate_yeti_format_traffic_data

from code.constants.column_names import *
from code.constants.enumerations import PollutantType
from code.strategy_helpers.validation_helpers import validate_dataset, check_mapping, check_categories_are_correct, \
    check_column_names, check_separator_is_comma, check_does_not_contain_nan


def validate_hbefa_berlin_format_files(**kwargs):

    link_data_file = kwargs["berlin_format_link_data"]
    fleet_comp_file = kwargs["berlin_format_fleet_composition"]
    emission_factor_file = kwargs["berlin_format_emission_factors"]
    traffic_data_file = kwargs["berlin_format_traffic_data"]

    logging.debug(f"Files to be validated: \n"
                  f"\t{link_data_file}\n"
                  f"\t{fleet_comp_file}\n"
                  f"\t{emission_factor_file}\n"
                  f"\t{traffic_data_file}\n")

    validate_dataset(link_data_file, "SHAPE")
    validate_dataset(fleet_comp_file, "FLEET_COMP")
    validate_dataset(emission_factor_file, "HBEFA_EF")
    validate_dataset(traffic_data_file, "TRAFFIC_COUNT")

    check_mapping(fleet_comp_file, emission_factor_file, from_cols=[FLEET_COMP_VEH_NAME], to_cols=[HBEFA_EF_VEH_NAME])
    check_mapping(link_data_file, traffic_data_file, from_cols=[SHAPE_LINK_ID], to_cols=[TRAFFIC_COUNT_LINK_ID])


def validate_hbefa_yeti_format_files(**kwargs):

    ef_file = kwargs["yeti_format_emission_factors"]
    vehicle_file = kwargs["yeti_format_vehicle_data"]
    link_file = kwargs["yeti_format_link_data"]
    traffic_file = kwargs["yeti_format_traffic_data"]

    logging.debug(f"Files to be validated: \n"
                  f"\t{ef_file}\n"
                  f"\t{vehicle_file}\n"
                  f"\t{link_file}\n"
                  f"\t{traffic_file}\n")

    validate_yeti_format_link_data(link_file)
    validate_yeti_format_vehicle_data(vehicle_file)
    validate_yeti_format_traffic_data(traffic_file)
    validate_yeti_format_hbefa_emission_factor_data(ef_file)

    check_mapping(link_file, traffic_file, from_cols=["LinkID"], to_cols=["LinkID"])
    check_mapping(vehicle_file, ef_file, from_cols=["VehicleName"], to_cols=["VehicleName"])


def validate_yeti_format_hbefa_emission_factor_data(filename):

    data = pd.read_csv(filename)

    check_separator_is_comma(filename)
    check_column_names(filename, data, ["VehicleName", "Pollutant", "TrafficSituation", "EF"])
    check_does_not_contain_nan(filename, data)
    check_categories_are_correct(filename, data, "Pollutant", [str(poll) for poll in PollutantType])