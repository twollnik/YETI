import pandas as pd

from code.copert_hot_strategy.validate import validate_copert_unified_files
from code.strategy_helpers.validation_helpers import check_separator_is_comma, check_column_names, \
    check_categories_are_correct


def validate_copert_cold_unified_files(**kwargs):

    validate_copert_unified_files(**kwargs)

    cold_ef_file = kwargs["unified_cold_ef_table"]
    validate_cold_ef_table(cold_ef_file)

    veh_mapping_file = kwargs["unified_vehicle_mapping"]
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