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
            test_arg1="abc", test_arg2=3, cold_test_arg3=True
        )

    @patch("code.copert_strategy.CopertStrategy.CopertHotFixedSpeedStrategy.calculate_emissions",
           return_value={"poll": {"veh a": 2}})
    def test_only_hot_emissions_using_fixed_speeds(self, mock_calc_function):

        strategy = CopertStrategy()
        emis_actual = strategy.calculate_emissions(
            fixed_speed=True,
            only_hot=True, traffic_and_link_data_row={"some": "data"}, vehicle_dict={"vehA": "catA"},
            pollutants=["pollA"], test_arg1="abc", hot_test_arg2=3, cold_test_arg3=True
        )

        self.assertEqual({"poll": {"veh a": 2}}, emis_actual)
        mock_calc_function.assert_called_once_with(
            {"some": "data"}, {"vehA": "catA"}, ["pollA"], only_hot=True,
            test_arg1="abc", test_arg2=3, cold_test_arg3=True, fixed_speed=True
        )

    @patch("code.copert_strategy.CopertStrategy.CopertColdStrategy.calculate_emissions",
           return_value={"poll": {"veh a": 200}})
    @patch("code.copert_strategy.CopertStrategy.CopertHotStrategy.calculate_emissions",
           return_value={"poll": {"veh a": 2}})
    def test_case_hot_and_cold_using_copert_cold_strategy(self, mock_hot_calc_function, mock_cold_calc_function):

        strategy = CopertStrategy()
        emis_actual = strategy.calculate_emissions(
            traffic_and_link_data_row={"some": "data"}, vehicle_dict={"vehA": "catA"},
            pollutants=["pollA"], test_arg1="abc", hot_test_arg2=3, cold_test_arg3=True
        )

        self.assertEqual(
            emis_actual,
            {"hot_poll": {"veh a": 2}, "cold_poll": {"veh a": 200}}
        )
        mock_hot_calc_function.assert_called_once_with(
            {"some": "data"}, {"vehA": "catA"}, ["pollA"],
            test_arg1="abc", test_arg2=3
        )
        mock_cold_calc_function.assert_called_once_with(
            {"some": "data"}, {"vehA": "catA"}, ["pollA"],
            test_arg1="abc", test_arg3=True, emissions_from_hot_strategy={"poll": {"veh a": 2}}
        )

    @patch("code.copert_strategy.CopertStrategy.CopertColdStrategy.calculate_emissions",
           return_value={"poll": {"cold": "emissions"}})
    @patch("code.copert_strategy.CopertStrategy.CopertHotFixedSpeedStrategy.calculate_emissions",
           return_value={"poll": {"hot": "emissions"}})
    def test_case_hot_and_cold_using_copert_cold_strategy_and_fixed_speeds(self, mock_hot_function, mock_cold_function):

        strategy = CopertStrategy()
        emis_actual = strategy.calculate_emissions(
            fixed_speed=True,
            traffic_and_link_data_row={"some": "data"}, vehicle_dict={"vehA": "catA"},
            pollutants=["pollA"], test_arg1="abc", hot_test_arg2=3, cold_test_arg3=True
        )

        self.assertEqual(
            emis_actual,
            {"hot_poll": {"hot": "emissions"}, "cold_poll": {"cold": "emissions"}}
        )
        mock_cold_function.assert_called_once_with(
            {"some": "data"}, {"vehA": "catA"}, ["pollA"],
            test_arg1="abc", test_arg3=True, fixed_speed=True,
            emissions_from_hot_strategy={"poll": {"hot": "emissions"}}
        )
        mock_hot_function.assert_called_once_with(
            {"some": "data"}, {"vehA": "catA"}, ["pollA"],
            test_arg1="abc", test_arg2=3, fixed_speed=True,
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
