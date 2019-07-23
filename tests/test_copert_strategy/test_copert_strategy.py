import os
from unittest import TestCase, main
from unittest.mock import patch

from code.copert_strategy.CopertStrategy import CopertStrategy


class TestCopertStrategy(TestCase):

    def setUp(self) -> None:

        if os.path.isfile("./tests/test_copert_strategy/test_load_yeti_format_data.py"):
            self.init_path = "./tests/test_copert_strategy"
        else:
            self.init_path = "."

    @patch("code.copert_strategy.CopertStrategy.CopertHotStrategy.calculate_emissions",
           return_value={"poll": {"veh a": 2}})
    def test_only_hot_emissions(self, mock_calc_function):

        strategy = CopertStrategy()
        emis_actual = strategy.calculate_emissions(
            only_hot=True, traffic_and_link_data_row={"some": "data"}, vehicle_dict={"vehA": "catA"},
            pollutants=["pollA"], test_arg1="abc", hot_test_arg2=3, cold_test_arg3=True
        )

        self.assertEqual({"poll": {"veh a": 2}}, emis_actual)
        mock_calc_function.assert_called_once_with(
            {"some": "data"}, {"vehA": "catA"}, ["pollA"], only_hot=True,
            test_arg1="abc", hot_test_arg2=3, cold_test_arg3=True
        )

    @patch("code.copert_strategy.CopertStrategy.CopertColdStrategy.calculate_emissions",
           return_value={"poll_hot": {"some": "data"}, "poll_cold": {"some": "other data"}, "poll_total": {"some": "more data"}})
    def test_case_hot_and_cold_using_copert_cold_strategy(self, mock_calc_function):

        strategy = CopertStrategy()
        emis_actual = strategy.calculate_emissions(
            traffic_and_link_data_row={"some": "data"}, vehicle_dict={"vehA": "catA"},
            pollutants=["pollA"], test_arg1="abc", hot_test_arg2=3, cold_test_arg3=True
        )

        self.assertEqual(
            emis_actual,
            {"poll_hot": {"some": "data"}, "poll_cold": {"some": "other data"}, "poll_total": {"some": "more data"}}
        )
        mock_calc_function.assert_called_once_with(
            {"some": "data"}, {"vehA": "catA"}, ["pollA"],
            test_arg1="abc", hot_test_arg2=3, cold_test_arg3=True
        )

    @patch("code.copert_strategy.CopertStrategy.CopertHotStrategy.calculate_emissions",
           return_value={"poll": {"vehA": 4}})
    def test_case_hot_and_cold_using_arbitrary_cold_strategy(self, mock_calc_function):

        strategy = CopertStrategy()
        emis_actual = strategy.calculate_emissions(
            traffic_and_link_data_row={"some": "data"}, vehicle_dict={"vehA": "catA"}, pollutants=["poll"],
            cold_strategy="tests.test_copert_strategy.MockStrategy.MockStrategy", test_arg1="abc",
            hot_test_arg2=3, cold_test_arg3=True
        )

        self.assertEqual(
            emis_actual,
            {"hot_poll": {"vehA": 4}, "cold_poll": {"vehA": 100}}
        )
        mock_calc_function.assert_called_once_with(
            {"some": "data"}, {"vehA": "catA"}, ["poll"], test_arg1="abc", test_arg2=3)


if __name__ == '__main__':
    main()
