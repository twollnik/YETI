import logging
from unittest import main, TestCase
from unittest.mock import MagicMock

from code.copert_cold_strategy.validate import check_if_hot_strategy_path_is_valid


class TestScriptHelpers(TestCase):

    def test_check_if_hot_strategy_path_is_valid_for_valid_path(self):

        logging.warning = MagicMock()

        check_if_hot_strategy_path_is_valid(hot_strategy="code.copert_hot_strategy.CopertHotStrategy.CopertHotStrategy")

        logging.warning.assert_not_called()

    def test_check_if_hot_strategy_path_is_valid_for_invalid_path(self):

        logging.warning = MagicMock()

        check_if_hot_strategy_path_is_valid(hot_strategy="some.invalid.path")

        logging.warning.assert_called_once()


if __name__ == '__main__':
    main()