from unittest import TestCase, main
import pandas as pd
import os
import shutil

from tests.helper import df_equal
from code.StrategyInvoker import StrategyInvoker
from code.copert_hot_strategy.CopertHotStrategy import CopertHotStrategy


class TestUnifiedDataToEmissions(TestCase):

    def test_unified_data_to_emissions(self):

        if os.path.isfile("./tests/test_data/unified_data/emission_factor_data.csv"):
            self.init_path = "./tests"
        else:
            self.init_path = "."

        emissions_file = StrategyInvoker().calculate_and_save_emissions(
            save_interval_in_rows=2,
            emissions_output_folder="temp",
            pollutant="PollutantType.NOx",
            emission_calculation_function=CopertHotStrategy().calculate_emissions,
            calculate_emissions=CopertHotStrategy().calculate_emissions,
            link_data=pd.read_csv(f"{self.init_path}/test_data/unified_data/link_data.csv"),
            traffic_data=pd.read_csv(f"{self.init_path}/test_data/unified_data/traffic_data.csv"),
            vehicle_data=pd.read_csv(f"{self.init_path}/test_data/unified_data/vehicle_data.csv"),
            emission_factor_data=pd.read_csv(f"{self.init_path}/test_data/unified_data/emission_factor_data.csv"),
            los_speeds_data=pd.read_csv(f"{self.init_path}/test_data/unified_data/los_speeds_data.csv")
        )

        emissions_actual = pd.read_csv(emissions_file)
        shutil.rmtree("temp")
        emissions_expected = pd.read_csv(f'{self.init_path}/test_data/emissions_expected.csv')

        self.assertEqual(len(emissions_expected), len(emissions_actual))

        emissions_actual = emissions_actual.round(5)
        emissions_expected = emissions_expected.round(5)

        self.assertTrue(df_equal(emissions_actual, emissions_expected))


if __name__ == '__main__':
    main()
