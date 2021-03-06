from unittest import TestCase, main
from unittest.mock import patch

from code.hbefa_strategy.HbefaStrategy import HbefaStrategy


class TestHbefaStrategy(TestCase):

    @patch("code.hbefa_strategy.HbefaStrategy.HbefaHotStrategy.calculate_emissions",
           return_value={"poll": {"veh a": 2}})
    def test_only_hot_emissions(self, mock_calc_function):

        strategy = HbefaStrategy()
        emis_actual = strategy.calculate_emissions(
            only_hot=True, traffic_and_link_data_row={"some": "data"}, vehicle_dict={"vehA": "catA"},
            pollutants=["pollA"], test_arg1="abc", hot_test_arg2=3, cold_test_arg3=True
        )

        self.assertEqual({"poll": {"veh a": 2}}, emis_actual)
        mock_calc_function.assert_called_once_with(
            {"some": "data"}, {"vehA": "catA"}, ["pollA"], only_hot=True,
            test_arg1="abc", test_arg2=3, cold_test_arg3=True
        )

    @patch("code.hbefa_strategy.HbefaStrategy.HbefaHotStrategy.calculate_emissions",
           return_value={"poll_a": {"some": "data"}, "poll_b": {"some": "other data"}})
    @patch("code.hbefa_strategy.HbefaStrategy.HbefaColdStrategy.calculate_emissions",
           return_value={"poll_a": {"hello": "darkness"}, "poll_b": {"my old": "friend"}})
    def test_case_hot_and_cold_using_hbefa_cold_strategy(self, mock_cold_function, mock_hot_function):

        strategy = HbefaStrategy()
        emis_actual = strategy.calculate_emissions(
            traffic_and_link_data_row={"some": "data"}, vehicle_dict={"vehA": "catA"},
            pollutants=["pollA"], test_arg1="abc", hot_test_arg2=3, cold_test_arg3=True
        )

        self.assertEqual(
            emis_actual,
            {"hot_poll_a": {"some": "data"}, "hot_poll_b": {"some": "other data"},
             "cold_poll_a": {"hello": "darkness"}, "cold_poll_b": {"my old": "friend"}}
        )
        mock_cold_function.assert_called_once_with(
            {"some": "data"}, {"vehA": "catA"}, ["pollA"],
            test_arg1="abc", test_arg3=True, emissions_from_hot_strategy={"poll_a": {"some": "data"}, "poll_b": {"some": "other data"}}
        )
        mock_hot_function.assert_called_once_with(
            {"some": "data"}, {"vehA": "catA"}, ["pollA"],
            test_arg1="abc", test_arg2=3
        )

    @patch("code.hbefa_strategy.HbefaStrategy.HbefaHotStrategy.calculate_emissions",
           return_value={"poll": {"vehA": 4}})
    def test_case_hot_and_cold_using_arbitrary_cold_strategy(self, mock_calc_function):

        strategy = HbefaStrategy()
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
