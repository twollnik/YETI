import pandas as pd

from code.constants.enumerations import VehicleCategory
from code.strategy_helpers.validation_helpers import check_separator_is_comma, check_column_names, \
    check_categories_are_correct, check_does_not_contain_nan, check_column_values_above_zero, check_are_perc_columns


def validate_unified_link_data(filename):

    data = pd.read_csv(filename)

    check_separator_is_comma(filename)
    check_column_names(filename, data, ["LinkID", "Length", "AreaType", "RoadType", "MaxSpeed"])
    check_categories_are_correct(filename, data, "AreaType", ["AreaType.Urban", "AreaType.Rural"])
    check_does_not_contain_nan(filename, data)
    check_column_values_above_zero(filename, data, ["MaxSpeed", "Length"])


def validate_unified_vehicle_data(filename):

    data = pd.read_csv(filename)

    check_separator_is_comma(filename)
    check_column_names(filename, data, ["VehicleName", "VehicleCategory", "NumberOfAxles"])
    check_categories_are_correct(filename, data, "VehicleCategory", [str(cat) for cat in VehicleCategory])
    check_does_not_contain_nan(filename, data[["VehicleName", "VehicleCategory"]])


def validate_unified_traffic_data(filename):

    data = pd.read_csv(filename)

    check_separator_is_comma(filename)
    check_column_names(filename, data, ["LinkID", "DayType", "Dir", "Hour", "LOS1Percentage",
                                        "LOS2Percentage", "LOS3Percentage", "LOS4Percentage"])
    check_are_perc_columns(filename, data, ["LOS1Percentage", "LOS2Percentage",
                                            "LOS3Percentage", "LOS4Percentage"])
    check_does_not_contain_nan(filename, data)