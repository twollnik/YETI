from unittest import TestCase, main
import pandas as pd
import numpy as np
import os

from code.data_loading.DataLoader import DataLoader
from code.data_loading.HbefaDataLoader import HbefaDataLoader
from code.hbefa_hot_strategy.load_unified_data import load_hbefa_unified_data
from code.copert_hot_strategy.load_unified_data import load_copert_unified_data
from tests.helper import df_equal


class TestDataLoader(TestCase):

    def setUp(self):

        if os.path.isfile("./tests/test_data/input_data/shape_data.csv"):
            self.init_path = "./tests"
        else:
            self.init_path = ".."

        self.loader = DataLoader(
            link_data_file=f'{self.init_path}/test_data/input_data/shape_data.csv',
            fleet_comp_file=f'{self.init_path}/test_data/input_data/fleet_comp_data.csv',
            emission_factor_file=f'{self.init_path}/test_data/input_data/copert_emission_factor_data.csv',
            los_speeds_file=f'{self.init_path}/test_data/input_data/los_speed_data.csv',
            traffic_data_file=f'{self.init_path}/test_data/input_data/traffic_data.csv',
            vehicle_mapping_file=f'{self.init_path}/test_data/input_data/vehicle_emissions_category_mapping_data.csv',
            nh3_ef_file=f'{self.init_path}/test_data/input_data/nh3_ef_data.csv',
            nh3_mapping_file=f'{self.init_path}/test_data/input_data/nh3_mapping.csv'
        )

    def test_dataframe_format(self):

        (link_data, vehicle_data, traffic_data, los_speeds_data,
         emission_factor_data, missing_ef_data) = self.loader.load_data()

        self.loader.filenames_dict["link_data_file"] = f"{self.init_path}/test_data/input_data/shape_data_with_speed.csv"
        (link_data_with_speed, vehicle_data_with_speed, traffic_data_with_speed, los_speeds_data_with_speed,
         emission_factor_data_with_speed, missing_ef_data_with_speed) = self.loader.load_data()

        self.assertTrue(vehicle_data.equals(vehicle_data_with_speed))
        self.assertTrue(traffic_data.equals(traffic_data_with_speed))
        self.assertTrue(los_speeds_data.equals(los_speeds_data_with_speed))
        self.assertTrue(emission_factor_data.equals(emission_factor_data_with_speed))
        self.assertTrue(missing_ef_data.equals(missing_ef_data_with_speed))

        self.assertTrue({'LinkID', 'Length', 'RoadType', 'AreaType'}.issubset(link_data.columns))
        self.assertTrue({'LinkID', 'Length', 'Speed', 'RoadType', 'AreaType'}.issubset(link_data_with_speed.columns))
        self.assertTrue({'VehicleName', 'VehicleCategory'}.issubset(vehicle_data.columns))
        self.assertTrue({'LinkID', 'Dir', 'DayType', 'Hour',
                         'pc vehicle_a', 'lcv vehicle_b', 'LOS1Percentage',
                         'LOS2Percentage', 'LOS3Percentage', 'LOS4Percentage'}.issubset(traffic_data.columns))
        self.assertTrue({'LinkID', 'VehicleCategory', 'LOS1Speed', 'LOS2Speed', 'LOS3Speed', 'LOS4Speed'}.issubset(los_speeds_data.columns))
        self.assertTrue({'VehicleName', 'Pollutant', 'MinSpeed', 'MaxSpeed',
                         'Alpha', 'Beta', 'Gamma', 'Delta', 'Epsilon',
                         'Zita', 'Hta', 'Thita', 'ReductionPerc', 'Mode', 'Load', 'Slope'}.issubset(emission_factor_data.columns))
        self.assertTrue({"Pollutant", "VehicleName"}.issubset(missing_ef_data.columns))

    def test_data_is_equal(self):
        (link_data, vehicle_data, traffic_data, los_speeds_data,
         emission_factor_data, missing_ef_data) = self.loader.load_data()
        link_data.Length = link_data.Length.apply(lambda val: round(val, 4))

        unified_data = load_copert_unified_data(
            unified_emission_factors=f'{self.init_path}/test_data/unified_data/emission_factor_data.csv',
            unified_los_speeds=f'{self.init_path}/test_data/unified_data/los_speeds_data.csv',
            unified_vehicle_data=f'{self.init_path}/test_data/unified_data/vehicle_data.csv',
            unified_link_data=f'{self.init_path}/test_data/unified_data/link_data.csv',
            unified_traffic_data=f'{self.init_path}/test_data/unified_data/traffic_data.csv'
        )
        link_data_pre = unified_data["link_data"]
        vehicle_data_pre = unified_data["vehicle_data"]
        traffic_data_pre = unified_data["traffic_data"]
        los_speeds_data_pre = unified_data["los_speeds_data"]
        emission_factor_data_pre = unified_data["emission_factor_data"]

        self.assertTrue(df_equal(link_data, link_data_pre))
        self.assertTrue(df_equal(vehicle_data, vehicle_data_pre))
        self.assertTrue(df_equal(los_speeds_data, los_speeds_data_pre))
        self.assertTrue(df_equal(traffic_data, traffic_data_pre))
        self.assertTrue(
            df_equal(missing_ef_data, pd.read_csv(f"{self.init_path}/test_data/other_data/missing_ef_data.csv")))

        # avoid error due to floating point inaccuracy
        for colname in ['Alpha', 'Beta', 'Gamma', 'Delta', 'Epsilon','Zita', 'Hta', 'Thita', 'ReductionPerc']:
            emission_factor_data[colname] = pd.Series(
                np.around(emission_factor_data[colname].values, 5))
            emission_factor_data_pre[colname] = pd.Series(
                np.around(emission_factor_data_pre[colname].values, 5))

        self.assertTrue(df_equal(emission_factor_data, emission_factor_data_pre))

    def test_use_hbefa_ef_works_correctly(self):

        data_loader = HbefaDataLoader(
            link_data_file=f'{self.init_path}/test_data/input_data/shape_data.csv',
            fleet_comp_file=f'{self.init_path}/test_data/input_data/fleet_comp_data.csv',
            emission_factor_file=f'{self.init_path}/test_data/input_data/hbefa_ef_data.csv',
            los_speeds_file=f'{self.init_path}/test_data/input_data/los_speed_data.csv',
            traffic_data_file=f'{self.init_path}/test_data/input_data/traffic_data.csv'
        )
        (link_data, vehicle_data, traffic_data, los_speeds_data,
         emission_factor_data, missing_ef_data) = data_loader.load_data()
        link_data.Length = link_data.Length.apply(lambda val: round(val, 4))

        unified_data = load_hbefa_unified_data(
            unified_emission_factors=f'{self.init_path}/test_data/unified_data/hbefa_ef_data.csv',
            unified_vehicle_data=f'{self.init_path}/test_data/unified_data/vehicle_data.csv',
            unified_link_data=f'{self.init_path}/test_data/unified_data/link_data.csv',
            unified_traffic_data=f'{self.init_path}/test_data/unified_data/traffic_data.csv'
        )

        link_data_pre = unified_data["link_data"]
        vehicle_data_pre = unified_data["vehicle_data"]
        traffic_data_pre = unified_data["traffic_data"]
        emission_factor_data_pre = unified_data["emission_factor_data"]

        self.assertTrue(df_equal(link_data, link_data_pre))
        self.assertTrue(df_equal(vehicle_data, vehicle_data_pre))
        self.assertTrue(los_speeds_data is None)
        self.assertTrue(df_equal(traffic_data, traffic_data_pre))
        self.assertTrue(df_equal(emission_factor_data, emission_factor_data_pre))


if __name__ == '__main__':
    main()
