from unittest import TestCase, main
from unittest.mock import MagicMock
import os
import pandas as pd
import numpy as np
import logging

from code.strategy_helpers.validation_helpers import *
from code.strategy_helpers.validate_unified_data import validate_unified_link_data, validate_unified_vehicle_data, \
    validate_unified_traffic_data
from code.copert_hot_strategy.validate import validate_unified_copert_ef_data, validate_unified_los_speeds_data, \
    validate_copert_unified_files
from code.copert_hot_fixed_speed_strategy.validate import validate_copert_fixed_speed_unified_files
from code.copert_cold_strategy.validate import validate_cold_ef_table, validate_veh_mapping, validate_copert_cold_unified_files
from code.hbefa_hot_strategy.validate import validate_unified_hbefa_emission_factor_data


class TestDataValidation(TestCase):

    def setUp(self) -> None:

        if os.path.isfile("./tests/test_data_validation/wrong_separator.csv"):
            self.init_path = "./tests"
        else:
            self.init_path = ".."

        # The logger's warning function is mocked in the tests. To recover the function after the test, save it in an instance var.
        self.logging_warning_function = logging.warning

    def tearDown(self) -> None:

        logging.warning = self.logging_warning_function

    def test_validate_format(self):

        with self.assertLogs(level="DEBUG") as mock_logger:
            self.assertFalse(validate_dataset(f"{self.init_path}/test_data_validation/wrong_separator.csv", ""))

        self.assertTrue(
            any("tests/test_data_validation/wrong_separator.csv does not have the correct separator. Use ',' "
                "instead of ';'. Also make sure to use '.' as decimal point (the decimal point is not "
                "checked automatically)." in line for line in mock_logger.output)
        )

    def test_check_columns(self):

        with self.assertLogs(level="DEBUG") as mock_logger:
            fleet_comp_data = pd.read_csv(f"{self.init_path}/test_data_validation/fleet_comp_data.csv")
            self.assertTrue(validate_dataset(f"{self.init_path}/test_data_validation/fleet_comp_data.csv",
                                             "FLEET_COMP", fleet_comp_data))
            self.assertFalse(validate_dataset(f"{self.init_path}/test_data_validation/fleet_comp_data.csv",
                                              "FLEET_COMP", fleet_comp_data.drop("VehPercOfCat", axis=1)))

        self.assertTrue(
            any("/tests/test_data_validation/fleet_comp_data.csv is missing the column VehPercOfCat" in line for line in mock_logger.output)
        )

    def test_check_categorical_data(self):

        df = pd.DataFrame({
            "VehName": ['a', 'a'],
            "VehCat": ['P', 'Z'],
            "VehPercOfCat": [0.9, 0.4]
        })
        with self.assertLogs(level="DEBUG") as mock_logger:
            self.assertFalse(validate_dataset(f"{self.init_path}/test_data_validation/fleet_comp_data.csv",
                                              "FLEET_COMP", df))

        self.assertTrue(
            any("tests/test_data_validation/fleet_comp_data.csv: The values in VehCat don't match the expected values.\n"
            "\t expected values: P, L, S, R, B, M, Moped\n"
            "\t actual values: P, Z" in line for line in mock_logger.output)
        )

    def test_check_perc_columns(self):

        with self.assertLogs(level="DEBUG") as mock_logger:
            df = pd.DataFrame({
                "VehName": ['a', 'a'],
                "VehCat": ['P', 'P'],
                "VehPercOfCat": [-1, 10]
            })
            self.assertFalse(validate_dataset(f"{self.init_path}/test_data_validation/fleet_comp_data.csv",
                                              "FLEET_COMP", df))

        self.assertTrue(
            any("/tests/test_data_validation/fleet_comp_data.csv: All values in column VehPercOfCat should be between 0 and 1." in line for line in
                mock_logger.output)
        )

    def test_check_mapping(self):

        df1 = pd.DataFrame({
            'a': ['1', '2', '3'],
            'b': [1, 2, 3],
            'c': ['a', 'b', 'c']
        })
        df2 = pd.DataFrame({
            'h': [1, 2, 3],
            'j': ['a', 'b', 'c'],
            'k': ['x', 'y', 'z']
        })
        self.assertTrue(check_mapping('file1', 'file2', ['b', 'c'], ['h', 'j'], df1, df2))

        df3 = pd.DataFrame({
            '6': [1, 2],
            '7': ['a', 'b'],
            'm': ['x', 'y']
        })
        with self.assertLogs(level="DEBUG") as mock_logger:
            self.assertFalse(check_mapping('file1', 'file2', ['b', 'c'], ['6', '7'], df1, df3))
        self.assertTrue(
            any("The mapping between file1 and file2 seems to be incorrect. Make sure all the values in "
                "the columns [b, c] in file1 are present in the columns [6, 7] in file2"
                in line for line in mock_logger.output)
        )

        df4 = pd.DataFrame(columns=['1', '2'])
        with self.assertLogs(level="DEBUG") as mock_logger:
            self.assertFalse(check_mapping('file1', 'file2', ['h', 'j'], ['1', '2'], df2, df4))
        self.assertTrue(
            any("The mapping between file1 and file2 seems to be incorrect. Make sure all the "
                "values in the columns [h, j] in file1 are present in the columns [1, 2] in file2."
                in line for line in mock_logger.output)
        )

        df5 = pd.DataFrame({
            'a': ['y', 'z'],
            'b': [1, 2]
        })
        df6 = pd.DataFrame({
            'c': ['y', 'z'],
            'd': [4, 5]
        })
        self.assertTrue(check_mapping('f1', 'f2', ['a'], ['c'], df5, df6))
        self.assertRaises(Exception, check_mapping, df5, df6, ['a'], ['d'], 'f1', 'f2')

    def test_check_does_not_contain_nan(self):

        logging.warning = MagicMock()

        df = pd.DataFrame(np.random.randn(10, 6))

        self.assertTrue(check_does_not_contain_nan("abc", df))

        # Make a few areas have NaN values
        df.iloc[1:3, 1] = np.nan
        df.iloc[5, 3] = np.nan
        df.iloc[7:9, 5] = np.nan

        self.assertFalse(check_does_not_contain_nan("abc", df))
        logging.warning.assert_called_once()


    def test_check_column_values_above_zero(self):

        logging.warning = MagicMock()

        df = pd.DataFrame(np.random.rand(10, 6), columns=["a", "b", "c", "d", "e", "f"])

        self.assertTrue(check_column_values_above_zero("abc", df, "b"))
        logging.warning.assert_not_called()

        df.iloc[2, 1] = 0
        self.assertFalse(check_column_values_above_zero("abc", df, "b"))
        logging.warning.assert_called_once()

        logging.warning.reset_mock()

        df.iloc[5, 1] = -20
        self.assertFalse(check_column_values_above_zero("abc", df, "b"))
        logging.warning.assert_called_once()

        logging.warning.reset_mock()

        self.assertFalse(check_column_values_above_zero("abc", df, ["b", "c"]))
        logging.warning.assert_called_once()
        logging.warning.reset_mock()

        self.assertTrue(check_column_values_above_zero("abc", df, ["e", "f"]))
        logging.warning.assert_not_called()

    def test_validate_unified_link_data(self):

        logging.warning = MagicMock()

        validate_unified_link_data(f"{self.init_path}/test_data/unified_data/link_data.csv")
        logging.warning.assert_not_called()

    def test_validate_unified_vehicle_data(self):

        logging.warning = MagicMock()

        validate_unified_vehicle_data(f"{self.init_path}/test_data/unified_data/vehicle_data.csv")
        logging.warning.assert_not_called()

    def test_validate_unified_traffic_data(self):

        logging.warning = MagicMock()

        validate_unified_traffic_data(f"{self.init_path}/test_data/unified_data/traffic_data.csv")
        logging.warning.assert_not_called()

    def test_validate_unified_copert_ef_data(self):

        logging.warning = MagicMock()

        validate_unified_copert_ef_data(f"{self.init_path}/test_data/unified_data/emission_factor_data.csv")
        logging.warning.assert_called_once()

    def test_validate_unified_los_speeds_data(self):

        logging.warning = MagicMock()

        validate_unified_los_speeds_data(f"{self.init_path}/test_data/unified_data/los_speeds_data.csv")
        logging.warning.assert_not_called()

    def test_validate_copert_unified_files(self):

        logging.warning = MagicMock()

        validate_copert_unified_files(
            unified_emission_factors = f"{self.init_path}/test_data/unified_data/emission_factor_data.csv",
            unified_los_speeds = f"{self.init_path}/test_data/unified_data/los_speeds_data.csv",
            unified_vehicle_data = f"{self.init_path}/test_data/unified_data/vehicle_data.csv",
            unified_link_data = f"{self.init_path}/test_data/unified_data/link_data.csv",
            unified_traffic_data = f"{self.init_path}/test_data/unified_data/traffic_data.csv"
        )
        logging.warning.assert_called_once()

    def test_validate_copert_fixed_speed_unified_files(self):

        logging.warning = MagicMock()

        validate_copert_fixed_speed_unified_files(
            unified_emission_factors = f"{self.init_path}/test_data/unified_data/emission_factor_data.csv",
            unified_vehicle_data = f"{self.init_path}/test_data/unified_data/vehicle_data.csv",
            unified_link_data = f"{self.init_path}/test_data/unified_data/link_data.csv",
            unified_traffic_data = f"{self.init_path}/test_data/unified_data/traffic_data.csv"
        )
        logging.warning.assert_called_once()

    def test_validate_cold_ef_table(self):

        logging.warning = MagicMock()

        validate_cold_ef_table(f"{self.init_path}/test_data/input_data/TableColdEF_minmax.csv")
        logging.warning.assert_not_called()

    def test_validate_veh_mapping(self):

        logging.warning = MagicMock()

        validate_veh_mapping(f"{self.init_path}/test_data/input_data/vehicle_emissions_category_mapping_data.csv")
        logging.warning.assert_not_called()

    def test_validate_copert_cold_unified_files(self):

        logging.warning = MagicMock()

        validate_copert_cold_unified_files(
            unified_emission_factors = f"{self.init_path}/test_data/unified_data/emission_factor_data.csv",
            unified_vehicle_data = f"{self.init_path}/test_data/unified_data/vehicle_data.csv",
            unified_link_data = f"{self.init_path}/test_data/unified_data/link_data.csv",
            unified_traffic_data = f"{self.init_path}/test_data/unified_data/traffic_data.csv",
            unified_los_speeds=f"{self.init_path}/test_data/unified_data/los_speeds_data.csv",
            unified_cold_ef_table = f"{self.init_path}/test_data/input_data/TableColdEF_minmax.csv",
            unified_vehicle_mapping = f"{self.init_path}/test_data/input_data/vehicle_emissions_category_mapping_data.csv"
        )
        logging.warning.assert_called_once()

    def test_validate_unified_hbefa_emission_factor_data(self):

        logging.warning = MagicMock()

        validate_unified_hbefa_emission_factor_data(f"{self.init_path}/test_data/unified_data/hbefa_ef_data.csv")
        logging.warning.assert_not_called()


if __name__ == '__main__':
    main()
