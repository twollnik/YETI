import os
import shutil
from unittest import TestCase, main

import pandas as pd

from code.StrategyInvoker import StrategyInvoker
from code.copert_strategy.CopertStrategy import CopertStrategy
from tests.helpers_and_mocks import df_equal


class TestYetiFormatDataToEmissions(TestCase):

    def setUp(self) -> None:

        if os.path.isfile("./tests/test_data/yeti_format_data/emission_factor_data.csv"):
            self.init_path = "./tests"
        else:
            self.init_path = "."

    def test_yeti_format_data_to_emissions(self):

        StrategyInvoker().calculate_and_save_emissions(
            save_interval_in_rows=2,
            emissions_output_folder="temp",
            pollutants=["PollutantType.NOx"],
            Strategy=CopertStrategy,
            only_hot=True,
            link_data=pd.read_csv(f"{self.init_path}/test_data/yeti_format_data/link_data.csv"),
            traffic_data=pd.read_csv(f"{self.init_path}/test_data/yeti_format_data/traffic_data.csv"),
            vehicle_data=pd.read_csv(f"{self.init_path}/test_data/yeti_format_data/vehicle_data.csv"),
            emission_factor_data=pd.read_csv(f"{self.init_path}/test_data/yeti_format_data/emission_factor_data.csv"),
            los_speeds_data=pd.read_csv(f"{self.init_path}/test_data/yeti_format_data/los_speeds_data.csv")
        )

        emissions_actual = pd.read_csv("temp/PollutantType.NOx_emissions.csv")
        shutil.rmtree("temp")
        emissions_expected = pd.read_csv(f'{self.init_path}/test_data/emissions_expected.csv')

        self.assertEqual(len(emissions_expected), len(emissions_actual))

        emissions_actual = emissions_actual.round(5)
        emissions_expected = emissions_expected.round(5)

        self.assertTrue(df_equal(emissions_actual, emissions_expected))


if __name__ == '__main__':
    main()
