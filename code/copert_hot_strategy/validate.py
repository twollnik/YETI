import logging
import os

from code.constants.column_names import *
from code.constants.mappings import INPUT_DATA_TO_SHORTHAND_MAPPING
from code.strategy_helpers.input_data_validation import validate_dataset, check_mapping


def validate_copert_input_files(**kwargs):

    use_nh3_ef = kwargs["use_nh3_tier2_ef"]

    kwargs_to_validate = [
        (key, value) for key, value in kwargs.items() if key.startswith("input_") and key in INPUT_DATA_TO_SHORTHAND_MAPPING
    ]
    logging.debug(
        "Files to be validated: \n\t{}".format('\n\t'.join([f"{key}: {value}" for key, value in kwargs_to_validate])))
    for key, value in kwargs_to_validate:
        if validate_dataset(value, INPUT_DATA_TO_SHORTHAND_MAPPING[key]) is True:
            logging.debug(f"File {value} validated successfully.")

    check_mapping(kwargs["input_fleet_composition"], kwargs["input_vehicle_mapping"],
                  from_cols=[FLEET_COMP_VEH_NAME], to_cols=[MAP_VEH_NAME])
    check_mapping(kwargs["input_vehicle_mapping"], kwargs["input_emission_factors"],
                  from_cols=[MAP_VEH_CAT, MAP_FUEL, MAP_VEH_SEG, MAP_EURO, MAP_TECHNOLOGY],
                  to_cols=[EF_VEH_CAT, EF_FUEL, EF_VEH_SEG, EF_EURO, EF_TECHNOLOGY])

    if use_nh3_ef is True:
        check_mapping(kwargs["input_fleet_composition"], kwargs["input_nh3_mapping"],
                      from_cols=[FLEET_COMP_VEH_NAME], to_cols=[NH3_MAP_VEH_NAME])
        check_mapping(kwargs["input_nh3_mapping"], kwargs["input_nh3_emission_factors"],
                      from_cols=[NH3_MAP_VEH_CAT, NH3_MAP_VEH_SEG, NH3_MAP_FUEL, NH3_MAP_EURO],
                      to_cols=[NH3_EF_VEH_CAT, NH3_EF_VEH_SEG, NH3_EF_FUEL, NH3_EF_EURO])


def file_paths_are_valid(**kwargs) -> bool:

    files_are_valid = (
        os.path.isfile(kwargs["unified_emission_factors"]) and
        os.path.isfile(kwargs["unified_los_speeds"]) and
        os.path.isfile(kwargs["unified_vehicle_data"]) and
        os.path.isfile(kwargs["unified_link_data"]) and
        os.path.isfile(kwargs["unified_traffic_data"])
    )
    if files_are_valid is False:
        raise RuntimeError("Paths to unified_.. files are not valid. Please check the configuration yaml.")
    return True