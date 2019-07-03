import numpy as np
import pandas as pd
from unittest import TestCase, main

from code.copert_hot_strategy.CopertHotStrategy import CopertHotStrategy


class TestCopertHotStrategy(TestCase):

    def test_calculate_emissions(self):

        vehicle_dict = {
            "vehA": "VehicleCategory.PC",
            "vehB": "VehicleCategory.LCV"
        }
        los_speeds_data = pd.DataFrame({
            "LinkID": ["linkA", "linkA"],
            "VehicleCategory": ["VehicleCategory.PC", "VehicleCategory.LCV"],
            "LOS1Speed": [5, 10],
            "LOS2Speed": [20, 20],
            "LOS3Speed": [30, 40],
            "LOS4Speed": [50, 60]
        })
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
            "LOS4Percentage": 1
        }
        emissions_expected = {
            "vehA": 1156.8796043417367,
            "vehB": 85.46364280124679
        }

        strategy = CopertHotStrategy()
        emissions_actual = strategy.calculate_emissions(
            row_dict, vehicle_dict, ["PollutantType.NOx"], los_speeds_data=los_speeds_data,
            emission_factor_data=emission_factor_data)

        self.assertEqual(emissions_expected, emissions_actual["PollutantType.NOx"])

if __name__ == '__main__':
    main()