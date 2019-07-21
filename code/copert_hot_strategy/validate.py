from code.strategy_helpers.validate_yeti_format_data import validate_yeti_format_vehicle_data, \
    validate_yeti_format_link_data, validate_yeti_format_traffic_data

from code.constants.column_names import *
from code.constants.enumerations import PollutantType, VehicleCategory
from code.strategy_helpers.validation_helpers import *


def validate_copert_berlin_format_files(**kwargs):

    use_nh3_ef = kwargs["use_nh3_tier2_ef"]

    fleet_comp_file = kwargs["berlin_format_fleet_composition"]
    link_data_file = kwargs["berlin_format_link_data"]
    emission_factor_file = kwargs["berlin_format_emission_factors"]
    traffic_data_file = kwargs["berlin_format_traffic_data"]
    vehicle_mapping_file = kwargs["berlin_format_vehicle_mapping"]
    los_speeds_file = kwargs["berlin_format_los_speeds"]
    nh3_ef_file = kwargs.get("berlin_format_nh3_emission_factors")
    nh3_mapping_file = kwargs.get("berlin_format_nh3_mapping")

    if use_nh3_ef is True:
        logging.debug(f"Files to be validated: \n"
                      f"\t{link_data_file}\n"
                      f"\t{fleet_comp_file}\n"
                      f"\t{emission_factor_file}\n"
                      f"\t{traffic_data_file}\n"
                      f"\t{vehicle_mapping_file}\n"
                      f"\t{los_speeds_file}\n"
                      f"\t{nh3_ef_file}\n"
                      f"\t{nh3_mapping_file}")
    else:
        logging.debug(f"Files to be validated: \n"
                      f"\t{link_data_file}\n"
                      f"\t{fleet_comp_file}\n"
                      f"\t{emission_factor_file}\n"
                      f"\t{traffic_data_file}\n"
                      f"\t{vehicle_mapping_file}\n"
                      f"\t{los_speeds_file}\n")

    validate_dataset(fleet_comp_file, "FLEET_COMP")
    validate_dataset(link_data_file, "SHAPE")
    validate_dataset(emission_factor_file, "EF")
    validate_dataset(traffic_data_file, "TRAFFIC_COUNT")
    validate_dataset(vehicle_mapping_file, "MAP")
    validate_dataset(los_speeds_file, "LOS_SPEED")

    check_mapping(kwargs["berlin_format_fleet_composition"], kwargs["berlin_format_vehicle_mapping"],
                  from_cols=[FLEET_COMP_VEH_NAME], to_cols=[MAP_VEH_NAME])
    check_mapping(kwargs["berlin_format_vehicle_mapping"], kwargs["berlin_format_emission_factors"],
                  from_cols=[MAP_VEH_CAT, MAP_FUEL, MAP_VEH_SEG, MAP_EURO, MAP_TECHNOLOGY],
                  to_cols=[EF_VEH_CAT, EF_FUEL, EF_VEH_SEG, EF_EURO, EF_TECHNOLOGY])

    if use_nh3_ef is True:
        validate_dataset(nh3_ef_file, "NH3_EF")
        validate_dataset(nh3_mapping_file, "NH3_MAP")
        check_mapping(kwargs["berlin_format_fleet_composition"], kwargs["berlin_format_nh3_mapping"],
                      from_cols=[FLEET_COMP_VEH_NAME], to_cols=[NH3_MAP_VEH_NAME])
        check_mapping(kwargs["berlin_format_nh3_mapping"], kwargs["berlin_format_nh3_emission_factors"],
                      from_cols=[NH3_MAP_VEH_CAT, NH3_MAP_VEH_SEG, NH3_MAP_FUEL, NH3_MAP_EURO],
                      to_cols=[NH3_EF_VEH_CAT, NH3_EF_VEH_SEG, NH3_EF_FUEL, NH3_EF_EURO])


def validate_copert_yeti_format_files(**kwargs):

    link_file = kwargs["yeti_format_link_data"]
    traffic_file = kwargs["yeti_format_traffic_data"]
    vehicle_file = kwargs["yeti_format_vehicle_data"]
    ef_file = kwargs["yeti_format_emission_factors"]
    los_speeds_file = kwargs["yeti_format_los_speeds"]

    logging.debug(f"Files to be validated: \n"
                  f"\t{link_file}\n"
                  f"\t{traffic_file}\n"
                  f"\t{vehicle_file}\n"
                  f"\t{los_speeds_file}\n"
                  f"\t{vehicle_file}")

    validate_yeti_format_link_data(link_file)
    validate_yeti_format_vehicle_data(vehicle_file)
    validate_yeti_format_copert_ef_data(ef_file)
    validate_yeti_format_los_speeds_data(los_speeds_file)
    validate_yeti_format_traffic_data(traffic_file)

    check_mapping(link_file, los_speeds_file, from_cols=["LinkID"], to_cols=["LinkID"])
    check_mapping(link_file, traffic_file, from_cols=["LinkID"], to_cols=["LinkID"])
    check_mapping(vehicle_file, ef_file, from_cols=["VehicleName"], to_cols=["VehicleName"])


def validate_yeti_format_copert_ef_data(filename):

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


def validate_yeti_format_los_speeds_data(filename):

    data = pd.read_csv(filename)

    check_separator_is_comma(filename)
    check_column_names(filename, data, ["LinkID", "VehicleCategory", "LOS1Speed", "LOS2Speed", "LOS3Speed", "LOS4Speed"])
    check_does_not_contain_nan(filename, data)
    check_categories_are_correct(filename, data, "VehicleCategory", [str(veh_cat) for veh_cat in VehicleCategory])
    check_column_values_above_zero(filename, data, ["LOS1Speed", "LOS2Speed", "LOS3Speed", "LOS4Speed"])
