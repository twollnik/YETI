from unittest import TestCase, main
import os
import pandas as pd
import shutil

from code.StrategyInvoker import StrategyInvoker
from code.copert_hot_fixed_speed_strategy.CopertHotFixedSpeedStrategy import CopertHotFixedSpeedStrategy


class TestSpeed(TestCase):

    def setUp(self):
        if os.path.isfile("./tests/test_data/unified_data/emission_factor_data.csv"):
            self.init_path = "./tests"
        else:
            self.init_path = "."

    def test_from_unified_data(self):

        emission_factor_data = pd.read_csv(f"{self.init_path}/test_data/unified_data/emission_factor_data.csv")
        los_speeds_data = pd.read_csv(f"{self.init_path}/test_data/unified_data/los_speeds_data.csv")
        vehicle_data = pd.read_csv(f"{self.init_path}/test_data/unified_data/vehicle_data.csv")
        link_data = pd.read_csv(f"{self.init_path}/test_data/unified_data/link_data_with_speed.csv")
        traffic_data = pd.read_csv(f"{self.init_path}/test_data/unified_data/traffic_data.csv")

        emissions_file = StrategyInvoker().calculate_and_save_emissions(
            emissions_output_folder="temp",
            pollutant="PollutantType.NOx",
            emission_calculation_function=CopertHotFixedSpeedStrategy().calculate_emissions,
            link_data=link_data,
            traffic_data=traffic_data,
            vehicle_data=vehicle_data,
            emission_factor_data=emission_factor_data,
            los_speeds_data=los_speeds_data
        )

        emissions_actual = pd.read_csv(emissions_file)
        shutil.rmtree("temp")

        self.assertEqual(len(emissions_actual), 288)
        for val in emissions_actual[["pc vehicle_a", "lcv vehicle_b"]].values.flatten():
            self.assertTrue(val >= 0)


if __name__ == "__main__":
    main()
