from unittest import TestCase, main
from unittest.mock import patch

import numpy as np
import pandas as pd

from code.copert_hot_fixed_speed_strategy.CopertHotFixedSpeedStrategy import CopertHotFixedSpeedStrategy
from code.copert_hot_fixed_speed_strategy.load_berlin_format_data import load_copert_fixed_speed_berlin_format_data


class TestCopertHotFixedSpeedStrategy(TestCase):

    def test_calculate_emissions(self):

        vehicle_dict = {
            "vehA": "VehicleCategory.PC",
            "vehB": "VehicleCategory.LCV"
        }
        emission_factor_data = pd.DataFrame({
            "VehicleName": ["vehA", "vehB"],
            "Pollutant": ["PollutantType.NOx", "PollutantType.NOx"],
            "Slope": [0, np.nan],
            "Load": [0, np.nan],
            "MaxSpeed": [100, "120"],
            "MinSpeed": [10, "5"],
            "Alpha": [2, "2"],
            "Beta": [0.3, "0.8"],
            "Gamma": [2, "3"],
            "Delta": [7, "4"],
            "Epsilon": [0, "2"],
            "Zita": [1, "6"],
            "Hta": [4, "9"],
            "ReductionPerc": [0, "0.5"]
        })
        row_dict = {
            "vehA": 10,
            "vehB": 100,
            "Length": 1,
            "LinkID": "linkA",
            "LOS1Percentage": 0.5,
            "LOS2Percentage": 0.3,
            "LOS3Percentage": 0.1,
            "LOS4Percentage": 1,
            "Speed": 10
        }
        pollutants = ["PollutantType.NOx"]

        emissions_expected_speed_20 = {
            "vehA": 336.8125,
            "vehB": 44.090419806243276
        }
        strategy = CopertHotFixedSpeedStrategy()
        emissions_actual = strategy.calculate_emissions(
            row_dict, vehicle_dict, pollutants, emission_factor_data=emission_factor_data, v=20)
        self.assertEqual(emissions_expected_speed_20, emissions_actual["PollutantType.NOx"])

        emissions_expected_speed_10 = {
            "vehA": 146.92857142857142,
            "vehB": 39.29368029739777
        }
        strategy = CopertHotFixedSpeedStrategy()
        emissions_actual = strategy.calculate_emissions(
            row_dict, vehicle_dict, pollutants, emission_factor_data=emission_factor_data)
        self.assertEqual(emissions_expected_speed_10, emissions_actual["PollutantType.NOx"])

    @patch("code.copert_hot_fixed_speed_strategy.load_berlin_format_data.load_copert_hot_berlin_format_data",
           return_value={"some": "return", "value": "."})
    def test_load_berlin_format_data(self, mocked_copert_hot_load_function):

        return_value = load_copert_fixed_speed_berlin_format_data(arg1=4, arg4=7, cold_arg="abc", hot_arg=789)

        self.assertEqual({"some": "return", "value": "."}, return_value)
        mocked_copert_hot_load_function.assert_called_once_with(arg1=4, arg4=7, cold_arg="abc", hot_arg=789)

if __name__ == '__main__':
    main()