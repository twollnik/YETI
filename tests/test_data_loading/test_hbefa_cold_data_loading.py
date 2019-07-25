import os
import shutil
from unittest import TestCase, main

import pandas as pd

from code.hbefa_cold_strategy.load_berlin_format_data import load_hbefa_cold_berlin_format_data
from code.hbefa_cold_strategy.load_yeti_format_data import load_hbefa_cold_yeti_format_data
from tests.helpers_and_mocks import df_equal


class TestHbefaColdDataLoading(TestCase):

    def setUp(self) -> None:

        if os.path.isfile("./tests/test_data/berlin_format_data/cold_starts.csv"):
            self.init_path = "./tests"
        else:
            self.init_path = ".."

        os.mkdir(f'{self.init_path}/temp_for_hbefa_cold_data_loading_test')

    def tearDown(self) -> None:

        shutil.rmtree(f"{self.init_path}/temp_for_hbefa_cold_data_loading_test")

    def test_load_berlin_format_data(self):

        data_actual_file_locations = load_hbefa_cold_berlin_format_data(
            berlin_format_link_data=f'{self.init_path}/test_data/berlin_format_data/shape_data.csv',
            berlin_format_fleet_composition=f'{self.init_path}/test_data/berlin_format_data/fleet_comp_data.csv',
            berlin_format_emission_factors=f'{self.init_path}/test_data/berlin_format_data/hbefa_cold_starts_ef.csv',
            berlin_format_cold_starts_data=f'{self.init_path}/test_data/berlin_format_data/cold_starts.csv',
            output_folder=f'{self.init_path}/temp_for_hbefa_cold_data_loading_test'
        )

        yeti_format_emission_factors_expected = pd.read_csv(f'{self.init_path}/test_data/yeti_format_data/hbefa_cold_starts_ef.csv')
        yeti_format_vehicle_data_expected = pd.read_csv(f'{self.init_path}/test_data/yeti_format_data/vehicle_data.csv')
        yeti_format_link_data_expected = pd.read_csv(f'{self.init_path}/test_data/yeti_format_data/link_data.csv')
        yeti_format_cold_starts_expected = pd.read_csv(f'{self.init_path}/test_data/yeti_format_data/cold_starts.csv')

        self.assertTrue(df_equal(
            pd.read_csv(data_actual_file_locations["yeti_format_emission_factors"]),
            yeti_format_emission_factors_expected))
        self.assertTrue(df_equal(
            pd.read_csv(data_actual_file_locations["yeti_format_vehicle_data"]),
            yeti_format_vehicle_data_expected))
        self.assertTrue(df_equal(
            pd.read_csv(data_actual_file_locations["yeti_format_link_data"]),
            yeti_format_link_data_expected))
        self.assertTrue(df_equal(
            pd.read_csv(data_actual_file_locations["yeti_format_cold_starts_data"]),
            yeti_format_cold_starts_expected))

    def test_load_builder_data(self):

        data_actual = load_hbefa_cold_yeti_format_data(
            yeti_format_emission_factors=f'{self.init_path}/test_data/yeti_format_data/hbefa_cold_starts_ef.csv',
            yeti_format_vehicle_data=f'{self.init_path}/test_data/yeti_format_data/vehicle_data.csv',
            yeti_format_link_data=f'{self.init_path}/test_data/yeti_format_data/link_data.csv',
            yeti_format_cold_starts_data=f'{self.init_path}/test_data/yeti_format_data/cold_starts.csv'
        )

        yeti_format_emission_factors_expected = pd.read_csv(f'{self.init_path}/test_data/yeti_format_data/hbefa_cold_starts_ef.csv')
        yeti_format_vehicle_data_expected = pd.read_csv(f'{self.init_path}/test_data/yeti_format_data/vehicle_data.csv')
        yeti_format_link_data_expected = pd.read_csv(f'{self.init_path}/test_data/yeti_format_data/link_data.csv')
        yeti_format_cold_starts_expected = pd.read_csv(f'{self.init_path}/test_data/yeti_format_data/cold_starts.csv')

        self.assertTrue(df_equal(data_actual["link_data"], yeti_format_link_data_expected))
        self.assertTrue(df_equal(data_actual["vehicle_data"], yeti_format_vehicle_data_expected))
        self.assertTrue(df_equal(data_actual["traffic_data"], yeti_format_cold_starts_expected))
        self.assertTrue(df_equal(data_actual["emission_factor_data"], yeti_format_emission_factors_expected))

if __name__ == '__main__':
    main()