from unittest import TestCase, main
from unittest.mock import patch

from code.copert_strategy.load_berlin_format_data import load_copert_berlin_format_data


class TestLoadBerlinFormatDataForCopertStrategy(TestCase):

    @patch("code.copert_strategy.load_berlin_format_data.load_copert_hot_berlin_format_data", return_value={"some": "return", "value": "for mocking"})
    def test_case_only_hot_emissions_should_be_calculated(self, mocked_copert_hot_load_function):

        actual_return_value = load_copert_berlin_format_data(only_hot=True, test_arg1=1, test_arg2="abc")

        self.assertEqual(actual_return_value, {"some": "return", "value": "for mocking"})
        mocked_copert_hot_load_function.assert_called_once_with(only_hot=True, test_arg1=1, test_arg2="abc")


if __name__ == '__main__':
    main()