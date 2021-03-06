import os
import shutil
from unittest import TestCase, main
from unittest.mock import patch

from code.copert_strategy.load_berlin_format_data import load_copert_berlin_format_data


class TestLoadBerlinFormatDataForCopertStrategy(TestCase):

    def setUp(self) -> None:

        if os.path.isfile("./tests/test_copert_strategy/test_load_berlin_format_data.py"):
            self.init_path = "./tests/test_copert_strategy"
        else:
            self.init_path = "."

    @patch("code.copert_strategy.load_berlin_format_data.load_copert_hot_berlin_format_data",
           return_value={"some": "return", "value": "for mocking"})
    def test_case_only_hot(self, mocked_copert_hot_load_function):

        actual_return_value = load_copert_berlin_format_data(only_hot=True, hot_test_arg1=1, cold_test_arg2="abc", output_folder="tests")

        self.assertEqual(actual_return_value, {"some": "return", "value": "for mocking"})
        mocked_copert_hot_load_function.assert_called_once_with(only_hot=True, test_arg1=1, cold_test_arg2="abc", output_folder="tests")

    @patch("code.copert_strategy.load_berlin_format_data.load_copert_cold_berlin_format_data",
           return_value={"some": "return", "value": "for mocking"})
    @patch("code.copert_strategy.load_berlin_format_data.load_copert_hot_berlin_format_data",
           return_value={"hot": "return", "data": "for mocking"})
    def test_case_hot_and_cold_using_copert_cold_strategy(self, mocked_hot_load_function, mocked_cold_load_function):

        actual_return_value = load_copert_berlin_format_data(hot_test_arg1=1, cold_test_arg2="abc", test_arg3=1, output_folder="tests")

        self.assertEqual(actual_return_value, {"cold_some": "return", "cold_value": "for mocking", "hot_hot": "return", "hot_data": "for mocking"})
        mocked_cold_load_function.assert_called_once_with(test_arg2="abc", test_arg3=1, output_folder="tests",
                                                          output_folder_for_yeti_format_data="tests/yeti_format_data_for_cold_strategy")
        mocked_hot_load_function.assert_called_once_with(test_arg1=1, test_arg3=1, output_folder="tests",
                                                         output_folder_for_yeti_format_data="tests/yeti_format_data_for_hot_strategy")

    @patch("code.copert_strategy.load_berlin_format_data.load_copert_hot_berlin_format_data",
           return_value={"some": "return", "value": "for mocking"})
    def test_case_hot_and_cold_using_arbitrary_cold_strategy(self, mocked_copert_hot_load_function):

        actual_return_value = load_copert_berlin_format_data(
            cold_strategy="tests.test_copert_strategy.MockStrategy.MockStrategy",
            cold_load_berlin_format_data_function="tests.helper.mock_load_data_function",
            test_arg1=1, test_arg2="abc", hot_test_arg3=4, output_folder="tests"
        )

        mocked_copert_hot_load_function.assert_called_once_with(
            test_arg1=1, test_arg2="abc", test_arg3=4, output_folder="tests",
            output_folder_for_yeti_format_data='tests/yeti_format_data_for_hot_strategy')

        self.assertEqual(actual_return_value,
                         {"hot_some": "return", "hot_value": "for mocking",
                          "cold_strategy": "tests.test_copert_strategy.MockStrategy.MockStrategy",
                          "cold_load_berlin_format_data_function": "tests.helper.mock_load_data_function",
                          "cold_output_folder": "tests",
                          "cold_output_folder_for_yeti_format_data": "tests/yeti_format_data_for_cold_strategy",
                          "cold_test_arg1": 1, "cold_test_arg2": "abc"
        })

    def test_case_hot_and_cold_data_is_saved_in_folders_named_hot_and_cold(self):

        # delete the folder
        dirpath = f"{self.init_path}/output_yeti_format_data"
        if os.path.exists(dirpath) and os.path.isdir(dirpath):
            shutil.rmtree(dirpath)

        # use data as requried for CopertHotStrategy and HbefaColdStrategy
        data_for_hot_strategy = {
            "berlin_format_link_data": f"{self.init_path}/../../example/example_berlin_format_data/link_data.csv",
            "berlin_format_fleet_composition": f"{self.init_path}/../../example/example_berlin_format_data/fleet_composition.csv",
            "hot_berlin_format_emission_factors": f"{self.init_path}/../../example/example_berlin_format_data/copert_emission_factors.csv",
            "berlin_format_los_speeds": f"{self.init_path}/../../example/example_berlin_format_data/los_speeds.csv",
            "berlin_format_traffic_data": f"{self.init_path}/../../example/example_berlin_format_data/traffic_data.csv",
            "berlin_format_vehicle_mapping": f"{self.init_path}/../../example/example_berlin_format_data/vehicle_mapping.csv",
            "use_nh3_tier2_ef": False
        }
        additional_data_for_cold_strategy = {
            "cold_berlin_format_emission_factors": f"{self.init_path}/../../example/example_berlin_format_data/hbefa_cold_start_emission_factors.csv",
            "berlin_format_cold_starts_data": f"{self.init_path}/../../example/example_berlin_format_data/cold_starts.csv"
        }

        load_copert_berlin_format_data(
            **data_for_hot_strategy,
            **additional_data_for_cold_strategy,
            output_folder=f"{self.init_path}/output_yeti_format_data",
            cold_strategy="path.to.some.ColdStrategy",
            cold_load_berlin_format_data_function="code.hbefa_cold_strategy.load_berlin_format_data.load_hbefa_cold_berlin_format_data"
        )

        self.assertTrue(os.path.isfile(f"{self.init_path}/output_yeti_format_data/yeti_format_data_for_hot_strategy/yeti_format_emission_factors.csv"))
        self.assertTrue(os.path.isfile(f"{self.init_path}/output_yeti_format_data/yeti_format_data_for_hot_strategy/yeti_format_los_speeds.csv"))
        self.assertTrue(os.path.isfile(f"{self.init_path}/output_yeti_format_data/yeti_format_data_for_hot_strategy/yeti_format_vehicle_data.csv"))
        self.assertTrue(os.path.isfile(f"{self.init_path}/output_yeti_format_data/yeti_format_data_for_hot_strategy/yeti_format_link_data.csv"))
        self.assertTrue(os.path.isfile(f"{self.init_path}/output_yeti_format_data/yeti_format_data_for_hot_strategy/yeti_format_traffic_data.csv"))

        self.assertTrue(os.path.isfile(f"{self.init_path}/output_yeti_format_data/yeti_format_data_for_cold_strategy/yeti_format_emission_factors.csv"))
        self.assertTrue(os.path.isfile(f"{self.init_path}/output_yeti_format_data/yeti_format_data_for_cold_strategy/yeti_format_vehicle_data.csv"))
        self.assertTrue(os.path.isfile(f"{self.init_path}/output_yeti_format_data/yeti_format_data_for_cold_strategy/yeti_format_link_data.csv"))
        self.assertTrue(os.path.isfile(f"{self.init_path}/output_yeti_format_data/yeti_format_data_for_cold_strategy/yeti_format_cold_starts_data.csv"))

    @patch("code.copert_strategy.load_berlin_format_data.load_copert_cold_berlin_format_data",
           return_value={"some": "return", "value": "for mocking"})
    @patch("code.copert_strategy.load_berlin_format_data.load_copert_hot_berlin_format_data",
           return_value={"hot": "return", "data": "for mocking"})
    def test_use_output_folder_for_yeti_format_data(self, mocked_hot_load_function, mocked_cold_load_function):

        actual_return_value = load_copert_berlin_format_data(
            hot_test_arg1=1, cold_test_arg2="abc", test_arg3=1,
            output_folder="tests", output_folder_for_yeti_format_data="docs")

        self.assertEqual(actual_return_value,
                         {"cold_some": "return", "cold_value": "for mocking", "hot_hot": "return",
                          "hot_data": "for mocking"})
        mocked_cold_load_function.assert_called_once_with(
            test_arg2="abc", test_arg3=1, output_folder="tests",
            output_folder_for_yeti_format_data="docs/yeti_format_data_for_cold_strategy")
        mocked_hot_load_function.assert_called_once_with(
            test_arg1=1, test_arg3=1, output_folder="tests",
            output_folder_for_yeti_format_data="docs/yeti_format_data_for_hot_strategy")

if __name__ == '__main__':
    main()