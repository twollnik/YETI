import os
from unittest import TestCase, main
from unittest.mock import patch

from code.copert_strategy.load_yeti_format_data import load_copert_yeti_format_data


class TestLoadYetiFormatDataForCopertStrategy(TestCase):

    def setUp(self) -> None:

        if os.path.isfile("./tests/test_copert_strategy/test_load_yeti_format_data.py"):
            self.init_path = "./tests/test_copert_strategy"
        else:
            self.init_path = "."

    @patch("code.copert_strategy.load_yeti_format_data.load_copert_hot_yeti_format_data",
           return_value={"some": "return", "value": "for mocking"})
    def test_case_only_hot(self, mocked_copert_hot_load_function):

        actual_return_value = load_copert_yeti_format_data(
            only_hot=True, hot_test_arg1=1, cold_test_arg2="abc", test_arg3=7)

        self.assertEqual(actual_return_value, {"some": "return", "value": "for mocking"})
        mocked_copert_hot_load_function.assert_called_once_with(
            only_hot=True, test_arg1=1, cold_test_arg2="abc", test_arg3=7)

    @patch("code.copert_strategy.load_yeti_format_data.load_copert_cold_yeti_format_data",
           return_value={"strategy cold": "data"})
    @patch("code.copert_strategy.load_yeti_format_data.load_copert_hot_yeti_format_data",
           return_value={"strategy hot": "loaded data"})
    def test_case_hot_and_cold_using_copert_cold_strategy(self, mocked_hot_load_function, mocked_cold_load_function):

        actual_return_value = load_copert_yeti_format_data(hot_test_arg1=1, cold_test_arg2="abc", test_arg3=9)

        self.assertEqual(actual_return_value, {"strategy hot": "loaded data", "cold_strategy cold": "data"})
        mocked_cold_load_function.assert_called_once_with(test_arg2="abc", test_arg3=9)
        mocked_hot_load_function.assert_called_once_with(test_arg1=1, test_arg3=9)

    @patch("code.copert_strategy.load_yeti_format_data.load_copert_hot_yeti_format_data",
           return_value={"some": "return", "value": "for mocking"})
    def test_case_hot_and_cold_using_arbitrary_cold_strategy(self, mocked_copert_hot_load_function):

        actual_return_value = load_copert_yeti_format_data(
            cold_strategy="tests.test_copert_strategy.MockStrategy.MockStrategy",
            cold_load_yeti_format_data_function="tests.helper.mock_load_data_function",
            test_arg1=1, test_arg2="abc", hot_test_arg3=4, output_folder="tests"
        )

        mocked_copert_hot_load_function.assert_called_once_with(
            test_arg1=1, test_arg2="abc", test_arg3=4, output_folder='tests')

        self.assertEqual(actual_return_value,
                         {"some": "return", "value": "for mocking",
                          "cold_strategy": "tests.test_copert_strategy.MockStrategy.MockStrategy",
                          "cold_load_yeti_format_data_function": "tests.helper.mock_load_data_function",
                          "cold_output_folder": "tests",
                          "cold_test_arg1": 1, "cold_test_arg2": "abc"
                          })

    def test_case_hot_and_cold_using_example_data(self):

        data = load_copert_yeti_format_data(
            hot_yeti_format_emission_factors=f"{self.init_path}/../../example/example_yeti_format_data/copert_emission_factors.csv",
            yeti_format_los_speeds=f"{self.init_path}/../../example/example_yeti_format_data/los_speeds.csv",
            yeti_format_vehicle_data=f"{self.init_path}/../../example/example_yeti_format_data/vehicle_data.csv",
            yeti_format_link_data=f"{self.init_path}/../../example/example_yeti_format_data/link_data.csv",
            yeti_format_traffic_data=f"{self.init_path}/../../example/example_yeti_format_data/traffic_data.csv",

            cold_yeti_format_emission_factors=f"{self.init_path}/../../example/example_yeti_format_data/hbefa_cold_start_emission_factors.csv",
            yeti_format_cold_starts_data=f"{self.init_path}/../../example/example_yeti_format_data/cold_starts_data.csv",

            cold_strategy="path.to.some.ColdStrategy",
            cold_load_yeti_format_data_function="code.hbefa_cold_strategy.load_yeti_format_data.load_hbefa_cold_yeti_format_data"
        )

        self.assertIn("link_data", data)
        self.assertIn("vehicle_data", data)
        self.assertIn("traffic_data", data)
        self.assertIn("los_speeds_data", data)
        self.assertIn("emission_factor_data", data)

        self.assertIn("cold_link_data", data)
        self.assertIn("cold_vehicle_data", data)
        self.assertIn("cold_traffic_data", data)
        self.assertIn("cold_emission_factor_data", data)


if __name__ == '__main__':
    main()
