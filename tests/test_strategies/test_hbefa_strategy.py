import pandas as pd
from unittest import TestCase, main

from code.hbefa_hot_strategy.HbefaHotStrategy import HbefaHotStrategy


class TestHbefaStrategy(TestCase):

    def test_calculate_emissions(self):

        vehicle_dict = {
            "vehA": "VehicleCategory.PC",
            "vehB": "VehicleCategory.LCV"
        }
        pollutant = "PollutantType.NOx"
        emission_factor_data = pd.DataFrame({
            "VehicleName": ["vehA", "vehA", "vehA", "vehA", "vehB", "vehB", "vehB", "vehB"],
            "Pollutant": ["PollutantType.NOx", "PollutantType.NOx", "PollutantType.NOx", "PollutantType.NOx",
                          "PollutantType.NOx", "PollutantType.NOx", "PollutantType.NOx", "PollutantType.NOx"],
            "TrafficSituation": ["URB/MW-City/100/Freeflow",
                                 "URB/MW-City/100/Heavy",
                                 "URB/MW-City/100/Satur.",
                                 "URB/MW-City/100/St+Go",
                                 "URB/MW-City/100/Freeflow",
                                 "URB/MW-City/100/Heavy",
                                 "URB/MW-City/100/Satur.",
                                 "URB/MW-City/100/St+Go",],
            "EF": [1, 2, 3, 4, 5, 6, 7, 8]
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
            "RoadType": "RoadType.MW_City",
            "AreaType": "AreaType.Urban",
            "MaxSpeed": 100
        }
        emissions_expected = {
            "vehA": 54,
            "vehB": 1300
        }

        strategy = HbefaHotStrategy()
        emissions_actual = strategy.calculate_emissions(
            row_dict, vehicle_dict, pollutant,
            emission_factor_data=emission_factor_data)

        self.assertEqual(emissions_expected, emissions_actual)

if __name__ == '__main__':
    main()