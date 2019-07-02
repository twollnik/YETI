from code.constants.column_names import *
from code.constants.enumerations import PollutantType, VehicleCategory
from code.constants.mappings import INPUT_DATA_TO_SHORTHAND_MAPPING
from code.strategy_helpers.validation_helpers import *
from code.strategy_helpers.validate_unified_data import validate_unified_vehicle_data, \
    validate_unified_link_data, validate_unified_traffic_data


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


def validate_copert_unified_files(**kwargs):

    ef_file = kwargs["unified_emission_factors"]
    los_speeds_file = kwargs["unified_los_speeds"]
    vehicle_file = kwargs["unified_vehicle_data"]
    link_file = kwargs["unified_link_data"]
    traffic_file = kwargs["unified_traffic_data"]

    validate_unified_link_data(link_file)
    validate_unified_vehicle_data(vehicle_file)
    validate_unified_copert_ef_data(ef_file)
    validate_unified_los_speeds_data(los_speeds_file)
    validate_unified_traffic_data(traffic_file)

    check_mapping(link_file, los_speeds_file, from_cols=["LinkID"], to_cols=["LinkID"])
    check_mapping(link_file, traffic_file, from_cols=["LinkID"], to_cols=["LinkID"])
    check_mapping(vehicle_file, ef_file, from_cols=["VehicleName"], to_cols=["VehicleName"])


def validate_unified_copert_ef_data(filename):

    data = pd.read_csv(filename)

    check_separator_is_comma(filename)
    check_column_names(filename, data, ["VehicleName", "Pollutant", "Mode", "Load", "Slope", "MinSpeed", "MaxSpeed",
                                        "Alpha", "Beta", "Gamma", "Delta", "Epsilon", "Hta", "Thita", "Zita",
                                        "ReductionPerc"])
    check_categories_are_correct(filename, data, "Pollutant", [str(poll) for poll in PollutantType])

    if "EF" in data.columns:
        data_excluding_nh3_tier2 = data[data["EF"].isnull()]
    else:
        data_excluding_nh3_tier2 = data
    check_column_values_above_zero(filename, data_excluding_nh3_tier2, ["MaxSpeed", "MinSpeed"])
    check_is_perc_column(filename, data_excluding_nh3_tier2, "ReductionPerc")


def validate_unified_los_speeds_data(filename):

    data = pd.read_csv(filename)

    check_separator_is_comma(filename)
    check_column_names(filename, data, ["LinkID", "VehicleCategory", "LOS1Speed", "LOS2Speed", "LOS3Speed", "LOS4Speed"])
    check_does_not_contain_nan(filename, data)
    check_categories_are_correct(filename, data, "VehicleCategory", [str(veh_cat) for veh_cat in VehicleCategory])
    check_column_values_above_zero(filename, data, ["LOS1Speed", "LOS2Speed", "LOS3Speed", "LOS4Speed"])
