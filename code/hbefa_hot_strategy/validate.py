import logging

from code.constants.column_names import FLEET_COMP_VEH_NAME, HBEFA_EF_VEH_NAME
from code.constants.mappings import INPUT_DATA_TO_SHORTHAND_MAPPING
from code.strategy_helpers.validation_helpers import validate_dataset, check_mapping


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