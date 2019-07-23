from unittest import TestCase, main
from unittest.mock import patch

from code.copert_strategy.load_yeti_format_data import load_copert_yeti_format_data


class TestLoadYetiFormatDataForCopertStrategy(TestCase):

    @patch("code.copert_strategy.load_yeti_format_data.load_copert_yeti_format_data",
           return_value={"some": "return", "value": "for mocking"})
    def test_case_only_hot(self, mocked_copert_hot_load_function):

        actual_return_value = load_copert_yeti_format_data(
            only_hot=True, hot_test_arg1=1, cold_test_arg2="abc", test_arg3=7)

        self.assertEqual(actual_return_value, {"some": "return", "value": "for mocking"})
        mocked_copert_hot_load_function.assert_called_once_with(
            only_hot=True, hot_test_arg1=1, cold_test_arg2="abc", test_arg3=7)


if __name__ == '__main__':
    main()