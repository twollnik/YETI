from unittest import TestCase, main
import os
import shutil
import pandas as pd

from code.hbefa_cold_strategy.load_input_data import load_hbefa_cold_input_data
from tests.helper import df_equal


class TestHbefaColdDataLoading(TestCase):

    def setUp(self) -> None:

        if os.path.isfile("./tests/test_data/input_data/cold_starts.csv"):
            self.init_path = "./tests"
        else:
            self.init_path = ".."

        os.mkdir(f'{self.init_path}/temp_for_hbefa_cold_data_loading_test')

    def tearDown(self) -> None:

        shutil.rmtree(f"{self.init_path}/temp_for_hbefa_cold_data_loading_test")

    def test(self):

        data_actual_file_locations = load_hbefa_cold_input_data(
            input_link_data=f'{self.init_path}/test_data/input_data/shape_data.csv',
            input_fleet_composition=f'{self.init_path}/test_data/input_data/fleet_comp_data.csv',
            input_emission_factors=f'{self.init_path}/test_data/input_data/hbefa_cold_starts_ef.csv',
            input_cold_starts_data=f'{self.init_path}/test_data/input_data/cold_starts.csv',
            output_folder=f'{self.init_path}/temp_for_hbefa_cold_data_loading_test'
        )

        unified_emission_factors_expected = pd.read_csv(f'{self.init_path}/test_data/unified_data/hbefa_cold_starts_ef.csv')
        unified_vehicle_data_expected = pd.read_csv(f'{self.init_path}/test_data/unified_data/vehicle_data.csv')
        unified_link_data_expected = pd.read_csv(f'{self.init_path}/test_data/unified_data/link_data.csv')
        unified_cold_starts_expected = pd.read_csv(f'{self.init_path}/test_data/unified_data/cold_starts.csv')

        self.assertTrue(df_equal(
            pd.read_csv(data_actual_file_locations["unified_emission_factors"]),
            unified_emission_factors_expected))
        self.assertTrue(df_equal(
            pd.read_csv(data_actual_file_locations["unified_vehicle_data"]),
            unified_vehicle_data_expected))
        self.assertTrue(df_equal(
            pd.read_csv(data_actual_file_locations["unified_link_data"]),
            unified_link_data_expected))
        self.assertTrue(df_equal(
            pd.read_csv(data_actual_file_locations["unified_cold_starts_data"]),
            unified_cold_starts_expected))


if __name__ == '__main__':
    main()