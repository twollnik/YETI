import numpy as np
import pandas as pd

from code.constants.column_names import *


class FileDataLoader:
    """ This class provides functionality to load input data from file. """

    def __init__(self, **kwargs):
        """ Initialize a FileDataLoader instance.

        You may pass the following keyword arguments to specify file locations. If you don't pass
        some of these arguments, the default locations as specified in 'default_filenames.py' will be used.
        Possible keyword arguments:
        - emission_factor_file
        - los_speeds_file
        - fleet_comp_file
        - link_data_file
        - traffic_data_file
        - vehicle_mapping_file
        - nh3_ef_file
        - nh3_mapping_file
        """

        self.emission_factor_file = kwargs.get('emission_factor_file')
        self.los_speeds_file = kwargs.get('los_speeds_file')
        self.fleet_comp_file = kwargs.get('fleet_comp_file')
        self.link_data_file = kwargs.get('link_data_file')
        self.traffic_file = kwargs.get('traffic_data_file')
        self.vehicle_name_to_category_mapping = kwargs.get(
            'vehicle_mapping_file')
        self.nh3_ef_file = kwargs.get('nh3_ef_file')
        self.nh3_mapping_file = kwargs.get('nh3_mapping_file')

    def load_data(self, use_nh3_ef: bool = True, **kwargs):
        """ Load input data from file.

        This method will load the dataframes required by the other AbstractDataLoader subclasses from file.
        It will use the column names as specified in 'column_names.py' under section '1. input data'.

        :param use_nh3_ef: If True, don't load nh3 ef data and nh3 mapping data.

        :return: copert_emission_factor_data, fleet_comp_data, los_speed_data, link_data,
                 traffic_count_data, vehicle_name_emissions_category_mapping_data
                 -> a 6-tuple of pd.Dataframes
        """

        link_data = self.load_link_data_from_file()
        fleet_comp_data = self.load_fleet_comp_data_from_file()
        traffic_count_data = self.load_traffic_count_data_from_file()
        emission_factor_data = self.load_emission_factor_data_from_file()
        los_speed_data = self.load_los_speeds_data_from_file()
        vehicle_name_emissions_category_mapping_data = self.load_vehicle_mapping_data_from_file()
        nh3_ef_data, nh3_mapping_data = self.load_nh3_ef_data_from_file_if_wanted(use_nh3_ef)

        return (emission_factor_data, fleet_comp_data, los_speed_data, link_data,
                traffic_count_data, vehicle_name_emissions_category_mapping_data, nh3_ef_data, nh3_mapping_data)

    def load_link_data_from_file(self):
        usecols_for_link_data = [
            SHAPE_LINK_ID, SHAPE_LENGTH, SHAPE_MAX_SPEED, SHAPE_PC_PERC, SHAPE_LCV_PERC,
            SHAPE_HDV_PERC, SHAPE_UBUS_PERC, SHAPE_COACH_PERC, SHAPE_MC_PERC,
            SHAPE_ROAD_CAT, SHAPE_AREA_CAT
        ]
        if self.speed_col_in_link_data():
            usecols_for_link_data.append(SHAPE_SPEED_OPTIONAL)
        link_data = pd.read_csv(self.link_data_file,
                                usecols=usecols_for_link_data,
                                dtype={
                                    SHAPE_LINK_ID: str, SHAPE_LENGTH: "float32", SHAPE_MAX_SPEED: np.uint8,
                                    SHAPE_PC_PERC: "float32", SHAPE_LCV_PERC: "float32", SHAPE_HDV_PERC: "float32",
                                    SHAPE_UBUS_PERC: "float32", SHAPE_COACH_PERC: "float32", SHAPE_MC_PERC: "float32",
                                    SHAPE_ROAD_CAT: "category", SHAPE_AREA_CAT: "category"
                                })
        return link_data

    def load_fleet_comp_data_from_file(self):
        fleet_comp_data = pd.read_csv(self.fleet_comp_file,
                                      usecols=[FLEET_COMP_VEH_NAME, FLEET_COMP_VEH_CAT,
                                               FLEET_COMP_VEH_PERC, FLEET_COMP_NUM_AXLES],
                                      dtype={FLEET_COMP_VEH_CAT: "category", FLEET_COMP_VEH_PERC: "float32",
                                             FLEET_COMP_VEH_NAME: str})
        return fleet_comp_data

    def load_traffic_count_data_from_file(self):
        traffic_count_data = pd.read_csv(self.traffic_file,
                                         usecols=[
                                             TRAFFIC_COUNT_LINK_ID, TRAFFIC_COUNT_DIR, TRAFFIC_COUNT_DAY_TYPE,
                                             TRAFFIC_COUNT_HOUR, TRAFFIC_COUNT_VEH_COUNT, TRAFFIC_COUNT_LOS_1_PERC,
                                             TRAFFIC_COUNT_LOS_2_PERC, TRAFFIC_COUNT_LOS_3_PERC,
                                             TRAFFIC_COUNT_LOS_4_PERC
                                         ],
                                         dtype={TRAFFIC_COUNT_LINK_ID: str, TRAFFIC_COUNT_DIR: "category",
                                                TRAFFIC_COUNT_DAY_TYPE: np.uint8, TRAFFIC_COUNT_HOUR: np.uint8,
                                                TRAFFIC_COUNT_VEH_COUNT: np.uint16, TRAFFIC_COUNT_LOS_1_PERC: "float32",
                                                TRAFFIC_COUNT_LOS_2_PERC: "float32",
                                                TRAFFIC_COUNT_LOS_3_PERC: "float32",
                                                TRAFFIC_COUNT_LOS_4_PERC: "float32"})
        return traffic_count_data

    def load_emission_factor_data_from_file(self):

        ef_columns = [
            EF_VEH_CAT, EF_FUEL, EF_VEH_SEG, EF_EURO, EF_POLL, EF_MIN_SPEED,
            EF_MAX_SPEED, EF_ALPHA, EF_BETA, EF_GAMMA, EF_DELTA, EF_EPSILON,
            EF_ZITA, EF_HTA, EF_THITA, EF_REDUC_FAC, EF_TECHNOLOGY,
            EF_LOAD, EF_SLOPE, EF_MODE
        ]
        emission_factor_data = pd.read_csv(self.emission_factor_file,
                                           usecols=ef_columns)
        return emission_factor_data

    def load_los_speeds_data_from_file(self):
        los_speed_data = pd.read_csv(self.los_speeds_file,
                                     usecols=[LOS_SPEED_VEH_CAT, LOS_SPEED_TRAFFIC_SITUATION, LOS_SPEED_SPEED],
                                     dtype={LOS_SPEED_VEH_CAT: "category", LOS_SPEED_TRAFFIC_SITUATION: str,
                                            LOS_SPEED_SPEED: "float32"})
        return los_speed_data

    def load_vehicle_mapping_data_from_file(self):

        vehicle_name_emissions_category_mapping_data = \
            pd.read_csv(self.vehicle_name_to_category_mapping,
                        usecols=[MAP_VEH_NAME, MAP_VEH_CAT, MAP_FUEL, MAP_VEH_SEG, MAP_EURO, MAP_TECHNOLOGY],
                        dtype={MAP_VEH_CAT: "category", MAP_FUEL: "category",
                               MAP_VEH_SEG: "category", MAP_EURO: "category", MAP_VEH_NAME: str})
        return vehicle_name_emissions_category_mapping_data

    def load_nh3_ef_data_from_file_if_wanted(self, use_nh3_ef):

        if use_nh3_ef is True:
            nh3_ef_data = pd.read_csv(self.nh3_ef_file)
            nh3_mapping_data = pd.read_csv(self.nh3_mapping_file)
        else:
            nh3_ef_data = None
            nh3_mapping_data = None
        return nh3_ef_data, nh3_mapping_data

    def speed_col_in_link_data(self):

        data = pd.read_csv(self.link_data_file, nrows=1)
        return SHAPE_SPEED_OPTIONAL in data.columns


class HbefaFileDataLoader(FileDataLoader):

    def load_emission_factor_data_from_file(self):

        ef_columns = [HBEFA_EF_EF, HBEFA_EF_POLL, HBEFA_EF_TRAFFIC_SIT, HBEFA_EF_VEH_NAME]
        emission_factor_data = pd.read_csv(self.emission_factor_file,
                                           usecols=ef_columns)
        return emission_factor_data

    def load_los_speeds_data_from_file(self):

        return None

    def load_vehicle_mapping_data_from_file(self):

        return None


class PMNonExhaustFileDataLoader(FileDataLoader):

    def load_emission_factor_data_from_file(self):

        return None

    def load_vehicle_mapping_data_from_file(self):

        return None
