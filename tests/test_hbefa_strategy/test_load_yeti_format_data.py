from unittest import TestCase, main
from unittest.mock import patch

from code.hbefa_strategy.load_yeti_format_data import load_hbefa_yeti_format_data


class TestLoadYetiFormatDataFunctionForHbefaStrategy(TestCase):

    @patch("code.hbefa_strategy.load_yeti_format_data.load_hbefa_hot_yeti_format_data",
           return_value={"some": "return", "value": "for mocking"})
    def test_case_only_hot(self, mocked_load_function):

        actual_return_value = load_hbefa_yeti_format_data(
            only_hot=True, hot_test_arg1=1, cold_test_arg2="abc", test_arg3=7)

        self.assertEqual(actual_return_value, {"some": "return", "value": "for mocking"})
        mocked_load_function.assert_called_once_with(
            only_hot=True, test_arg1=1, cold_test_arg2="abc", test_arg3=7)

    @patch("code.hbefa_strategy.load_yeti_format_data.load_hbefa_hot_yeti_format_data",
           return_value={"some": "return", "value": "here"})
    @patch("code.hbefa_strategy.load_yeti_format_data.load_hbefa_cold_yeti_format_data",
           return_value={"another": "return", "parameter": "here"})
    def test_case_hot_and_cold_using_hbefa_cold_strategy(self, mocked_cold_load_function, mocked_hot_load_function):

        actual_return_value = load_hbefa_yeti_format_data(hot_test_arg1=1, cold_test_arg2="abc", test_arg3=9)

        self.assertEqual(actual_return_value, {"some": "return", "value": "here",
                                               "cold_another": "return", "cold_parameter": "here"})
        mocked_cold_load_function.assert_called_once_with(test_arg2="abc", test_arg3=9)
        mocked_hot_load_function.assert_called_once_with(test_arg1=1, test_arg3=9)

    @patch("code.hbefa_strategy.load_yeti_format_data.load_hbefa_hot_yeti_format_data",
           return_value={"some": "return", "value": "for mocking"})
    def test_case_hot_and_cold_using_arbitrary_cold_strategy(self, mocked_load_function):

        actual_return_value = load_hbefa_yeti_format_data(
            cold_strategy="tests.test_copert_strategy.MockStrategy.MockStrategy",
            cold_load_yeti_format_data_function="tests.helper.mock_load_data_function",
            test_arg1=1, cold_test_arg2="abc", hot_test_arg3=4#, output_folder="tests"
        )

        mocked_load_function.assert_called_once_with(test_arg1=1, test_arg3=4)#, output_folder='tests')
        self.assertEqual(actual_return_value,
                         {"some": "return", "value": "for mocking",
                          "cold_strategy": "tests.test_copert_strategy.MockStrategy.MockStrategy",
                          "cold_load_yeti_format_data_function": "tests.helper.mock_load_data_function",
                         # "cold_output_folder": "tests",
                          "cold_test_arg1": 1, "cold_test_arg2": "abc"
                          })


if __name__ == '__main__':
    main()
