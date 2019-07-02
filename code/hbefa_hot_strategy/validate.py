import logging
import pandas as pd

from code.constants.column_names import FLEET_COMP_VEH_NAME, HBEFA_EF_VEH_NAME
from code.constants.mappings import INPUT_DATA_TO_SHORTHAND_MAPPING
from code.constants.enumerations import PollutantType
from code.strategy_helpers.validation_helpers import validate_dataset, check_mapping, check_categories_are_correct, \
    check_column_names, check_separator_is_comma, check_does_not_contain_nan
from code.strategy_helpers.validate_unified_data import validate_unified_link_data, validate_unified_vehicle_data, \
    validate_unified_traffic_data


def validate_hbefa_input_files(**kwargs):

    kwargs_to_validate = [
        (key, value) for key, value in kwargs.items() if key.startswith("input_")
    ]
    logging.debug(
        "Files to be validated: \n\t{}".format('\n\t'.join([f"{key}: {value}" for key, value in kwargs_to_validate])))
    for key, value in kwargs_to_validate:
        shorthand = INPUT_DATA_TO_SHORTHAND_MAPPING[key] if key != "input_emission_factors" else "HBEFA_EF"
        if validate_dataset(value, shorthand) is True:
            logging.debug(f"File {value} validated successfully.")

    check_mapping(kwargs["input_fleet_composition"], kwargs["input_emission_factors"],
                  from_cols=[FLEET_COMP_VEH_NAME], to_cols=[HBEFA_EF_VEH_NAME])


def validate_hbefa_unified_files(**kwargs):

    ef_file = kwargs["unified_emission_factors"]
    vehicle_file = kwargs["unified_vehicle_data"]
    link_file = kwargs["unified_link_data"]
    traffic_file = kwargs["unified_traffic_data"]

    validate_unified_link_data(link_file)
    validate_unified_vehicle_data(vehicle_file)
    validate_unified_traffic_data(traffic_file)
    validate_unified_hbefa_emission_factor_data(ef_file)

    check_mapping(link_file, traffic_file, from_cols=["LinkID"], to_cols=["LinkID"])
    check_mapping(vehicle_file, ef_file, from_cols=["VehicleName"], to_cols=["VehicleName"])


def validate_unified_hbefa_emission_factor_data(filename):

    data = pd.read_csv(filename)

    check_separator_is_comma(filename)
    check_column_names(filename, data, ["VehicleName", "Pollutant", "TrafficSituation", "EF"])
    check_does_not_contain_nan(filename, data)
    check_categories_are_correct(filename, data, "Pollutant", [str(poll) for poll in PollutantType])
