import logging
import pandas as pd

from code.constants.column_names import *
from code.strategy_helpers.validate_unified_data import validate_unified_vehicle_data, validate_unified_link_data
from code.strategy_helpers.validation_helpers import check_mapping, check_separator_is_comma, \
    check_column_names, check_does_not_contain_nan, validate_dataset, check_column_values_above_zero
from code.copert_hot_strategy.validate import validate_unified_copert_ef_data


def validate_copert_fixed_speed_input_files(**kwargs):

    use_nh3_ef = kwargs.get("use_nh3_tier2_ef")

    fleet_comp_file = kwargs["input_fleet_composition"]
    link_data_file = kwargs["input_link_data"]
    emission_factor_file = kwargs["input_emission_factors"]
    traffic_data_file = kwargs["input_traffic_data"]
    vehicle_mapping_file = kwargs["input_vehicle_mapping"]
    nh3_ef_file = kwargs.get("input_nh3_emission_factors")
    nh3_mapping_file = kwargs.get("input_nh3_mapping")

    if use_nh3_ef is True:
        logging.debug(f"Files to be validated: \n"
                      f"\t{link_data_file}\n"
                      f"\t{fleet_comp_file}\n"
                      f"\t{emission_factor_file}\n"
                      f"\t{traffic_data_file}\n"
                      f"\t{vehicle_mapping_file}\n"
                      f"\t{nh3_ef_file}\n"
                      f"\t{nh3_mapping_file}")
    else:
        logging.debug(f"Files to be validated: \n"
                      f"\t{link_data_file}\n"
                      f"\t{fleet_comp_file}\n"
                      f"\t{emission_factor_file}\n"
                      f"\t{traffic_data_file}\n"
                      f"\t{vehicle_mapping_file}\n")

    validate_dataset(fleet_comp_file, "FLEET_COMP")
    validate_dataset(link_data_file, "SHAPE")
    validate_dataset(emission_factor_file, "EF")
    validate_dataset(traffic_data_file, "TRAFFIC_COUNT")
    validate_dataset(vehicle_mapping_file, "MAP")

    check_mapping(kwargs["input_fleet_composition"], kwargs["input_vehicle_mapping"],
                  from_cols=[FLEET_COMP_VEH_NAME], to_cols=[MAP_VEH_NAME])
    check_mapping(kwargs["input_vehicle_mapping"], kwargs["input_emission_factors"],
                  from_cols=[MAP_VEH_CAT, MAP_FUEL, MAP_VEH_SEG, MAP_EURO, MAP_TECHNOLOGY],
                  to_cols=[EF_VEH_CAT, EF_FUEL, EF_VEH_SEG, EF_EURO, EF_TECHNOLOGY])

    check_speed_specification(link_data_file, "Speed_kmh", **kwargs)

    if use_nh3_ef is True:
        validate_dataset(nh3_ef_file, "NH3_EF")
        validate_dataset(nh3_mapping_file, "NH3_MAP")
        check_mapping(kwargs["input_fleet_composition"], kwargs["input_nh3_mapping"],
                      from_cols=[FLEET_COMP_VEH_NAME], to_cols=[NH3_MAP_VEH_NAME])
        check_mapping(kwargs["input_nh3_mapping"], kwargs["input_nh3_emission_factors"],
                      from_cols=[NH3_MAP_VEH_CAT, NH3_MAP_VEH_SEG, NH3_MAP_FUEL, NH3_MAP_EURO],
                      to_cols=[NH3_EF_VEH_CAT, NH3_EF_VEH_SEG, NH3_EF_FUEL, NH3_EF_EURO])


def validate_copert_fixed_speed_unified_files(**kwargs):

    link_file = kwargs["unified_link_data"]
    vehicle_file = kwargs["unified_vehicle_data"]
    traffic_file = kwargs["unified_traffic_data"]
    ef_file = kwargs["unified_emission_factors"]

    logging.debug(f"Files to be validated: \n"
                  f"\t{link_file}\n"
                  f"\t{vehicle_file}\n"
                  f"\t{traffic_file}\n"
                  f"\t{ef_file}\n")

    validate_unified_link_data(link_file)
    validate_unified_vehicle_data(vehicle_file)
    validate_unified_copert_ef_data(ef_file)
    validate_pm_non_exhaust_unified_traffic_data(traffic_file)

    check_mapping(link_file, traffic_file, from_cols=["LinkID"], to_cols=["LinkID"])
    check_mapping(vehicle_file, ef_file, from_cols=["VehicleName"], to_cols=["VehicleName"])

    check_speed_specification(link_file, "Speed", **kwargs)


def validate_pm_non_exhaust_unified_traffic_data(filename):

    data = pd.read_csv(filename)

    check_separator_is_comma(filename)
    check_column_names(filename, data, ["LinkID", "DayType", "Dir", "Hour"])
    check_does_not_contain_nan(filename, data)


def check_speed_specification(link_file, speed_col, **kwargs):

    speed_given_in_config = "v" in kwargs.keys()
    if speed_given_in_config:
        link_data = pd.read_csv(link_file)
        if speed_col not in link_data.columns:
            logging.warning(f"{link_file}: Column Speed_kmh not found and 'v' is not specified in config.")
        else:
            check_column_values_above_zero(link_file, link_data, "Speed_kmh")