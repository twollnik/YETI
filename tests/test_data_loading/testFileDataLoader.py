from unittest import TestCase, main
import os
from itertools import chain

from code.data_loading.FileDataLoader import FileDataLoader
from code.constants.column_names import *


class TestFileDataLoader(TestCase):

    def setUp(self) -> None:

        if os.path.isfile("./tests/test_data/input_data/copert_emission_factor_data.csv"):
            self.init_path = "./tests"
        else:
            self.init_path = ".."

        self.loader = FileDataLoader(
            emission_factor_file=f"{self.init_path}/test_data/input_data/copert_emission_factor_data.csv",
            los_speeds_file=f"{self.init_path}/test_data/input_data/los_speed_data.csv",
            fleet_comp_file=f"{self.init_path}/test_data/input_data/fleet_comp_data.csv",
            link_data_file=f"{self.init_path}/test_data/input_data/shape_data.csv",
            traffic_data_file=f"{self.init_path}/test_data/input_data/traffic_data.csv",
            vehicle_mapping_file=f"{self.init_path}/test_data/input_data/vehicle_emissions_category_mapping_data.csv",
            nh3_ef_file=f"{self.init_path}/test_data/input_data/nh3_ef_data.csv",
            nh3_mapping_file=f"{self.init_path}/test_data/input_data/nh3_mapping.csv"
        )

    def test_file_data_loading(self):

        (copert_emission_factor_data, fleet_comp_data, los_speed_data, link_data,
         traffic_count_data, vehicle_name_emissions_category_mapping_data,
         nh3_ef_data, nh3_mapping_data) = self.loader.load_data(use_hbefa_ef=False)

        self.loader.link_data_file = f"{self.init_path}/test_data/input_data/shape_data_with_speed.csv"
        (_, _, _, link_data_with_speed, _, _, _, _) = self.loader.load_data(use_hbefa_ef=False)

        self.assertTrue({
            SHAPE_LINK_ID, SHAPE_LENGTH, SHAPE_MAX_SPEED, SHAPE_PC_PERC, SHAPE_LCV_PERC,
            SHAPE_HDV_PERC, SHAPE_UBUS_PERC, SHAPE_COACH_PERC, SHAPE_MC_PERC,
            SHAPE_ROAD_CAT, SHAPE_AREA_CAT
        }.issubset(link_data.columns))
        self.assertTrue({
            SHAPE_LINK_ID, SHAPE_LENGTH, SHAPE_MAX_SPEED, SHAPE_PC_PERC, SHAPE_LCV_PERC,
            SHAPE_HDV_PERC, SHAPE_UBUS_PERC, SHAPE_COACH_PERC, SHAPE_MC_PERC,
            SHAPE_ROAD_CAT, SHAPE_AREA_CAT, SHAPE_SPEED_OPTIONAL
        }.issubset(link_data_with_speed.columns))

        self.assertTrue({
            FLEET_COMP_VEH_NAME, FLEET_COMP_VEH_CAT, FLEET_COMP_VEH_PERC
        }.issubset(fleet_comp_data.columns))

        self.assertTrue({
            LOS_SPEED_VEH_CAT, LOS_SPEED_TRAFFIC_SITUATION, LOS_SPEED_SPEED
        }.issubset(los_speed_data.columns))

        self.assertTrue({
            TRAFFIC_COUNT_LINK_ID, TRAFFIC_COUNT_DIR, TRAFFIC_COUNT_DAY_TYPE,
            TRAFFIC_COUNT_HOUR, TRAFFIC_COUNT_VEH_COUNT, TRAFFIC_COUNT_LOS_1_PERC,
            TRAFFIC_COUNT_LOS_2_PERC, TRAFFIC_COUNT_LOS_3_PERC,
            TRAFFIC_COUNT_LOS_4_PERC
        }.issubset(traffic_count_data.columns))

        self.assertTrue({
            EF_VEH_CAT, EF_FUEL, EF_VEH_SEG, EF_EURO, EF_POLL, EF_MIN_SPEED,
            EF_MAX_SPEED, EF_ALPHA, EF_BETA, EF_GAMMA, EF_DELTA, EF_EPSILON,
            EF_ZITA, EF_HTA, EF_THITA, EF_REDUC_FAC, EF_TECHNOLOGY,
            EF_LOAD, EF_SLOPE, EF_MODE
        }.issubset(copert_emission_factor_data.columns))

        self.assertTrue({
            MAP_VEH_NAME, MAP_VEH_CAT, MAP_FUEL, MAP_VEH_SEG, MAP_EURO, MAP_TECHNOLOGY
        }.issubset(vehicle_name_emissions_category_mapping_data.columns))

        self.assertTrue({
            NH3_EF_EF, NH3_EF_VEH_SEG, NH3_EF_VEH_CAT, NH3_EF_FUEL, NH3_EF_EURO
        }.issubset(nh3_ef_data.columns))

        self.assertTrue({
            NH3_MAP_VEH_NAME, NH3_MAP_VEH_CAT, NH3_MAP_FUEL, NH3_MAP_EURO, NH3_MAP_VEH_SEG
        }.issubset(nh3_mapping_data.columns))

    def test_dfs_not_empty(self):

        data = self.loader.load_data(use_hbefa_ef=False)

        self.loader.link_data_file = f"{self.init_path}/test_data/input_data/shape_data_with_speed.csv"
        data_with_speed = self.loader.load_data(use_hbefa_ef=False)

        for df in chain(data_with_speed, data):
            self.assertFalse(df.empty)

if __name__ == "__main__":
    main()
