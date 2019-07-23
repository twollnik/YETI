from unittest import TestCase, main
from unittest.mock import patch

from code.copert_strategy.load_berlin_format_data import load_copert_berlin_format_data


class TestLoadBerlinFormatDataForCopertStrategy(TestCase):

    @patch("code.copert_strategy.load_berlin_format_data.load_copert_hot_berlin_format_data",
           return_value={"some": "return", "value": "for mocking"})
    def test_case_only_hot(self, mocked_copert_hot_load_function):

        actual_return_value = load_copert_berlin_format_data(only_hot=True, test_arg1=1, test_arg2="abc")

        self.assertEqual(actual_return_value, {"some": "return", "value": "for mocking"})
        mocked_copert_hot_load_function.assert_called_once_with(only_hot=True, test_arg1=1, test_arg2="abc")

    @patch("code.copert_strategy.load_berlin_format_data.load_copert_cold_berlin_format_data",
           return_value={"some": "return", "value": "for mocking"})
    def test_case_hot_and_cold_using_copert_cold_strategy(self, mocked_copert_cold_load_function):

        actual_return_value = load_copert_berlin_format_data(test_arg1=1, test_arg2="abc")

        self.assertEqual(actual_return_value, {"some": "return", "value": "for mocking"})
        mocked_copert_cold_load_function.assert_called_once_with(test_arg1=1, test_arg2="abc")

    @patch("code.copert_strategy.load_berlin_format_data.load_copert_hot_berlin_format_data",
           return_value={"some": "return", "value": "for mocking"})
    def test_case_hot_and_cold_using_arbitrary_cold_strategy(self, mocked_copert_hot_load_function):

        actual_return_value = load_copert_berlin_format_data(
            cold_strategy="tests.test_copert_strategy.MockStrategy.MockStrategy",
            cold_load_berlin_format_data_function="tests.test_copert_strategy.mock_load_berlin_data_function.mock_load_berlin_data_function",
            test_arg1=1, test_arg2="abc", hot_test_arg3=4
        )

        mocked_copert_hot_load_function.assert_called_once_with(test_arg1=1, test_arg2="abc", test_arg3=4)

        self.assertEqual(actual_return_value,
                         {"hot_some": "return", "hot_value": "for mocking",
                          "cold_strategy": "tests.test_copert_strategy.MockStrategy.MockStrategy",
                          "cold_load_berlin_format_data_function": "tests.test_copert_strategy.mock_load_berlin_data_function.mock_load_berlin_data_function",
                          "cold_test_arg1": 1, "cold_test_arg2": "abc"
        })


if __name__ == '__main__':
    main()