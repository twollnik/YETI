import logging

import pandas as pd

from code.copert_hot_strategy.validate import validate_copert_yeti_format_files, validate_copert_berlin_format_files
from code.strategy_helpers.validation_helpers import check_separator_is_comma, check_column_names, \
    check_categories_are_correct


def validate_copert_cold_berlin_format_files(**kwargs):

    logging.debug("Validation: Part 1 of 2")
    validate_copert_berlin_format_files(**kwargs)

    cold_ef_file = kwargs["berlin_format_cold_ef_table"]
    veh_mapping_file= kwargs["berlin_format_vehicle_mapping"]

    logging.debug("Validation: Part 2 of 2")
    logging.debug(f"Files to be validated: \n"
                  f"\t{cold_ef_file}\n"
                  f"\t{veh_mapping_file}\n")

    validate_cold_ef_table(cold_ef_file)
    validate_veh_mapping(veh_mapping_file)


def validate_copert_cold_yeti_format_files(**kwargs):

    logging.debug("Validation: Part 1 of 2")
    validate_copert_yeti_format_files(**kwargs)

    cold_ef_file = kwargs["yeti_format_cold_ef_table"]
    veh_mapping_file = kwargs["yeti_format_vehicle_mapping"]

    logging.debug("Validation: Part 2 of 2")
    logging.debug(f"Files to be validated: \n"
                  f"\t{cold_ef_file}\n"
                  f"\t{veh_mapping_file}\n")

    validate_cold_ef_table(cold_ef_file)
    validate_veh_mapping(veh_mapping_file)


def validate_cold_ef_table(filename):

    data = pd.read_csv(filename)

    check_separator_is_comma(filename)
    check_column_names(filename, data, ["VehSegment", "Pollutant", "MinSpeed", "MaxSpeed", "MinTemp", "MaxTemp", "A", "B", "C"])
    check_categories_are_correct(filename, data, "Pollutant", ["CO", "NOx", "VOC"])
    check_categories_are_correct(filename, data, "VehSegment", ["Mini", "Small", "Medium", "Large-SUV-Executive"])


def validate_veh_mapping(filename):

    data = pd.read_csv(filename)

    check_separator_is_comma(filename)
    check_column_names(filename, data, ["VehCat", "Fuel", "VehSegment", "EuroStandard", "Technology", "VehName"])