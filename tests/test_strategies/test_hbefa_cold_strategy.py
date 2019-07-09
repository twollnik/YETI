import pandas as pd
from unittest import TestCase, main
from unittest.mock import MagicMock
from collections import defaultdict

from code.hbefa_cold_strategy.HbefaColdStrategy import HbefaColdStrategy


class TestHbefaColdStrategy(TestCase):

    def test_calculate_emissions(self):

        strategy = HbefaColdStrategy()
        cold_starts_data = pd.DataFrame({
            "Pollutant": ["PollutantType.NOx", "PollutantType.NOx", "PollutantType.CO", "PollutantType.CO"],
            "VehicleName": ["veh a", "veh b", "veh a", "veh b"],
            "EmissionsPerStart": [1, 2, 3, 4]
        })
        cold_starts_and_link_data_row = {
            "veh a": 10,
            "veh b": 20
        }
        vehicle_dict = {"veh a": "some category", "veh b": "some other category"}
        pollutants = ["PollutantType.NOx", "PollutantType.CO"]

        emissions_actual = strategy.calculate_emissions(
            cold_starts_and_link_data_row, vehicle_dict, pollutants, cold_starts_data=cold_starts_data)

        emissions_expected = {
            "PollutantType.NOx": {
                "veh a": 10,
                "veh b": 40
            },
            "PollutantType.CO": {
                "veh a": 30,
                "veh b": 80
            }
        }

        self.assertEqual(emissions_expected, emissions_actual)

    def test_initialize_if_necessary_case_is_necessary(self):

        strategy = HbefaColdStrategy()
        cold_starts_data = pd.DataFrame({
            "Pollutant": ["PollutantType.NOx", "PollutantType.NOx"],
            "VehicleName": ["veh a", "veh b"],
            "EmissionsPerStart": [1, 2]
        })
        strategy.initialize_if_necessary(cold_starts_data=cold_starts_data)

        self.assertEqual(strategy.cold_start_ef_for_vehicle_and_pollutant[("veh a", "PollutantType.NOx")], 1)
        self.assertEqual(strategy.cold_start_ef_for_vehicle_and_pollutant[("veh b", "PollutantType.NOx")], 2)

    def test_initialize_if_necessary_case_is_not_necessary(self):

        strategy = HbefaColdStrategy()
        strategy.initialize = MagicMock()
        strategy.cold_start_ef_for_vehicle_and_pollutant = defaultdict(dict, {("A", "B"): 3})

        strategy.initialize_if_necessary()

        strategy.initialize.assert_not_called()

    def test_calculate_emissions_for_vehicle(self):

        strategy = HbefaColdStrategy()
        strategy.cold_start_ef_for_vehicle_and_pollutant = {("veh a", "poll a"): 4}

        strategy.calculate_emissions_for_vehicle(
            cold_starts_and_link_data_row={"veh a": 10},
            vehicle_name="veh a",
            pollutant="poll a"
        )
        emissions_actual = strategy.emissions["poll a"]["veh a"]

        emissions_expected = 40

        self.assertEqual(emissions_expected, emissions_actual)


if __name__ == '__main__':
    main()