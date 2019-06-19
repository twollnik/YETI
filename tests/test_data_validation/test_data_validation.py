from unittest import TestCase, main
import os
import pandas as pd

from code.strategy_helpers.input_data_validation import validate_dataset, check_mapping


class TestDataValidation(TestCase):

    def setUp(self) -> None:

        if os.path.isfile("./tests/test_data_validation/wrong_separator.csv"):
            self.init_path = "./tests"
        else:
            self.init_path = ".."

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


if __name__ == '__main__':
    main()