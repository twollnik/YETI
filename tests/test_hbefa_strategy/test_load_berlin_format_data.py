from unittest import TestCase, main
from unittest.mock import patch

from code.hbefa_strategy.load_berlin_format_data import load_hbefa_berlin_format_data


class TestLoadBerlinFormatDataForHbefaStrategy(TestCase):

    @patch("code.hbefa_strategy.load_berlin_format_data.load_hbefa_hot_berlin_format_data",
           return_value={"some": "return", "value": "here"})
    def test_only_hot(self, mocked_load_function):

        val = load_hbefa_berlin_format_data(only_hot=True, arg1=1, hot_arg2="abc", cold_arg3=7)

        self.assertEqual(val, {"some": "return", "value": "here"})
        mocked_load_function.assert_called_once_with(only_hot=True, arg1=1, hot_arg2="abc", cold_arg3=7)

    @patch("code.hbefa_strategy.load_berlin_format_data.load_hbefa_hot_berlin_format_data",
           return_value={"some": "return", "value": "here"})
    @patch("code.hbefa_strategy.load_berlin_format_data.load_hbefa_cold_berlin_format_data",
           return_value={"another": "return", "parameter": "here"})
    def test_hot_and_cold(self, mocked_cold_load_function, mocked_hot_load_function):

        val = load_hbefa_berlin_format_data(arg1=1, hot_arg2="abc", cold_arg3=7)

        self.assertEqual(val,{"hot_some": "return", "hot_value": "here",
                              "cold_another": "return", "cold_parameter": "here"})
        mocked_cold_load_function.assert_called_once_with(arg1=1, arg3=7)
        mocked_hot_load_function.assert_called_once_with(arg1=1, arg2="abc")


if __name__ == '__main__':
    main()
