"""
This file contains the complete list of all column names for the datasets belonging to the input_data class.
For categorical data columns it also contains the possible categories.

Naming convention:
- Column names start with the shorthand of the file that the column is in.
- Percentage columns end in 'PERC'.
- Variables specifying the values a column can take end in 'LEVELS' and start with the column name they are referring to.

You may alter the column names in section "1. input data" to fit the dataset
you are currently working with. However you need to make sure to only use
letters, numbers and underscores in the column names. Using other characters
may result in errors or bugs down the line.
"""

# ---------------- 1. input data ---------------- #

# fleet composition data
FLEET_COMP_VEH_NAME = "VehName"
FLEET_COMP_VEH_CAT = "VehCat"
FLEET_COMP_VEH_PERC = "VehPercOfCat"
FLEET_COMP_NUM_AXLES = "NumberOfAxles"

FLEET_COMP_VEH_CAT_LEVELS = ["P", "L", "S", "R", "B", "M", "Moped"]

# link data
SHAPE_LINK_ID = "LinkID"
SHAPE_LENGTH = "Length_m"
SHAPE_SPEED_OPTIONAL = "Speed_kmh"
SHAPE_MAX_SPEED = "MaxSpeed_kmh"
SHAPE_PC_PERC = "PC_Perc"
SHAPE_LCV_PERC = "LCV_Perc"
SHAPE_HDV_PERC = "HDV_Perc"
SHAPE_UBUS_PERC = "UBus_Perc"
SHAPE_COACH_PERC = "Coach_Perc"
SHAPE_MC_PERC = "MC_Perc"
SHAPE_ROAD_CAT = "RoadCat"
SHAPE_AREA_CAT = "AreaCat"

SHAPE_AREA_CAT_LEVELS = ["0", "1"] # 0: rural, 1: urban
SHAPE_ROAD_CAT_LEVELS = ["6", "5", "9", "8", "1", "3", "0"]

# traffic count data
TRAFFIC_COUNT_LINK_ID = "LinkID"
TRAFFIC_COUNT_DIR = "Dir"
TRAFFIC_COUNT_DAY_TYPE = "DayType"
TRAFFIC_COUNT_HOUR = "Hour"
TRAFFIC_COUNT_VEH_COUNT = "VehCount"
TRAFFIC_COUNT_LOS_1_PERC = "LOS1Perc"
TRAFFIC_COUNT_LOS_2_PERC = "LOS2Perc"
TRAFFIC_COUNT_LOS_3_PERC = "LOS3Perc"
TRAFFIC_COUNT_LOS_4_PERC = "LOS4Perc"

TRAFFIC_COUNT_DIR_LEVELS = ["R", "L"]
TRAFFIC_COUNT_DAY_TYPE_LEVELS = ["1", "2", "3", "7"]

# los speeds data
LOS_SPEED_VEH_CAT = "VehCat"
LOS_SPEED_TRAFFIC_SITUATION = "TrafficSituation"
LOS_SPEED_SPEED = "Speed_kmh"

LOS_SPEED_VEH_CAT_LEVELS = ["pass. car", "LCV", "HGV", "coach", "urban bus", "motorcycle"]

# emission factor data
EF_VEH_CAT = "VehCat"
EF_FUEL = "Fuel"
EF_VEH_SEG = "VehSegment"
EF_EURO = "EuroStandard"
EF_TECHNOLOGY = "Technology"
EF_POLL = "Pollutant"
EF_MIN_SPEED = "MinSpeed_kmh"
EF_MAX_SPEED = "MaxSpeed_kmh"
EF_ALPHA = "Alpha"
EF_BETA = "Beta"
EF_GAMMA = "Gamma"
EF_DELTA = "Delta"
EF_EPSILON = "Epsilon"
EF_ZITA = "Zita"
EF_HTA = "Hta"
EF_THITA = "Thita"
EF_REDUC_FAC = "ReductionPerc"
EF_SLOPE = "Slope"
EF_LOAD = "Load"
EF_MODE = "Mode"

EF_VEH_CAT_LEVELS = ["Passenger Cars", "Light Commercial Vehicles", "Heavy Duty Trucks",
                     "Buses", "L-Category"]

# vehicle name to copert categories mapping data
MAP_VEH_NAME = "VehName"
MAP_VEH_CAT = "VehCat"
MAP_FUEL = "Fuel"
MAP_VEH_SEG = "VehSegment"
MAP_EURO = "EuroStandard"
MAP_TECHNOLOGY = "Technology"

MAP_VEH_CAT_LEVELS = ["Passenger Cars", "Light Commercial Vehicles", "Heavy Duty Trucks",
                      "Buses", "L-Category"]

# NH3 Tier 2 emission factor data
NH3_EF_VEH_CAT = "VehCat"
NH3_EF_VEH_SEG = "VehSegment"
NH3_EF_FUEL = "Fuel"
NH3_EF_EURO = "EuroStandard"
NH3_EF_EF = "EF"

# vehicle names to NH3 ef categories mapping data
NH3_MAP_VEH_CAT = "VehCat"
NH3_MAP_VEH_SEG = "VehSegment"
NH3_MAP_FUEL = "Fuel"
NH3_MAP_EURO = "EuroStandard"
NH3_MAP_VEH_NAME = "VehName"

# hbefa emission factor data
HBEFA_EF_POLL = "Component"
HBEFA_EF_TRAFFIC_SIT = "TrafficSit"
HBEFA_EF_VEH_NAME = "Subsegment"
HBEFA_EF_EF = "EFA"