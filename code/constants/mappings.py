from code.constants.enumerations import VehicleCategory, LOSType
from code.constants.column_names import *


# Mapping the road categories specified in the link data to the road categories
# used by the los speeds data file.
HEBEFA_ROAD_CAT_TO_LOS_SPEEDS_DATA_ROAD_CAT_MAPPING = {
    "6": "MW-Nat.",
    "5": "MW-City",
    "9": "Trunk-Nat.",
    "8": "Trunk-City",
    "1": "Distr",
    "3": "Local",
    "0": "Access"
}

ROAD_CAT_FROM_ENUM = {
    "RoadType.MW_Nat": "MW-Nat.",
    "RoadType.MW_City": "MW-City",
    "RoadType.Trunk_Nat": "Trunk-Nat.",
    "RoadType.Trunk_City": "Trunk-City",
    "RoadType.Distr": "Distr",
    "RoadType.Local": "Local",
    "RoadType.Access": "Access"
}

VEH_CAT_MAPPING = {
            "pass. car": "VehicleCategory.PC",
            "LCV": "VehicleCategory.LCV",
            "coach": "VehicleCategory.COACH",
            "urban bus": "VehicleCategory.UBUS",
            "motorcycle": "VehicleCategory.MC",
            "HGV": "VehicleCategory.HDV",
}

# Mapping the VehicleCategoriy enumerations to the vehicle categories used in the
# los speeds dataset.
VEHICLE_CAT_TO_STRING_MAPPING = {
    VehicleCategory.PC: "pass. car",
    VehicleCategory.LCV: "LCV",
    VehicleCategory.HDV: "HGV",
    VehicleCategory.COACH: "coach",
    VehicleCategory.UBUS: "urban bus",
    VehicleCategory.MOPED: "motorcycle",
    VehicleCategory.MC: "motorcycle"
}

# Mapping the LOSType enumerations to the los types used in the los speeds dataset.
LOS_TYPE_TO_STRING_MAPPING ={
    LOSType.LOS1: "Freeflow",
    LOSType.LOS2: "Heavy",
    LOSType.LOS3: "Satur.",
    LOSType.LOS4: "St+Go"
}

# Mapping the vehicle categories from the fleet composition data to the names of the columns
# that contain category percentage information in the link data.
FLEET_COMP_VEH_CAT_TO_LINK_DATA_TRAFFIC_PERC_MAPPING = {
    "P": SHAPE_PC_PERC,
    "L": SHAPE_LCV_PERC,
    "S": SHAPE_HDV_PERC,
    "R": SHAPE_COACH_PERC,
    "B": SHAPE_UBUS_PERC,
    "M": SHAPE_MC_PERC,
    "Moped": SHAPE_MC_PERC
}

# Mapping the vehicle categories from the fleet composition data to the VehicleCategory enumerations.
FLEET_COMP_VEH_CAT_TO_UNIFIED_VEH_CAT_MAPPING = {
    "P": VehicleCategory.PC,
    "L": VehicleCategory.LCV,
    "S": VehicleCategory.HDV,
    "R": VehicleCategory.COACH,
    "B": VehicleCategory.UBUS,
    "M": VehicleCategory.MC,
    "Moped": VehicleCategory.MOPED
}

# Mapping lowercase pollutants to the casing used in the PollutantType enumeration type definition.
# This is used to make user input of pollutants case insensitive.
LOWERCASE_POLLUTANT_NAMES_TO_POLLUTANT_ENUMERATION_TYPES = {
    "nox": "NOx",
    "co": "CO",
    "nh3": "NH3",
    "voc": "VOC",
    "pm_exhaust": "PM_Exhaust"
}

INPUT_DATA_TO_SHORTHAND_MAPPING = {
    "input_link_data": "SHAPE",
    "input_fleet_composition": "FLEET_COMP",
    "input_emission_factors": "EF",
    "input_los_speeds": "LOS_SPEED",
    "input_traffic_data": "TRAFFIC_COUNT",
    "input_vehicle_mapping": "MAP",
    "input_nh3_emission_factors": "NH3_EF",
    "input_nh3_mapping": "NH3_MAP"
}