from unittest import TestCase, main
import pandas as pd
import os

from tests.helper import df_equal
from code.data_loading.PMNonExhaustDataLoader import PMNonExhaustDataLoader
from code.pm_non_exhaust_strategy.load_unified_data import load_pm_non_exhaust_unified_data


class TestPMNonExhaustDataLoader(TestCase):

    def test_load_data(self):

        if os.path.isfile("./tests/test_data/input_data/shape_data.csv"):
            self.init_path = "./tests"
        else:
            self.init_path = ".."

        loader = PMNonExhaustDataLoader(
            link_data_file=f'{self.init_path}/test_data/input_data/shape_data.csv',
            fleet_comp_file=f'{self.init_path}/test_data/input_data/fleet_comp_data.csv',
            los_speeds_file=f'{self.init_path}/test_data/input_data/los_speed_data.csv',
            traffic_data_file=f'{self.init_path}/test_data/input_data/traffic_data.csv'
        )
        (link_data, vehicle_data, traffic_data, los_speeds_data, _, _) = loader.load_data()

        expected_data = load_pm_non_exhaust_unified_data(
            unified_los_speeds=f'{self.init_path}/test_data/unified_data/los_speeds_data.csv',
            unified_vehicle_data=f'{self.init_path}/test_data/unified_data/vehicle_data.csv',
            unified_link_data=f'{self.init_path}/test_data/unified_data/link_data.csv',
            unified_traffic_data=f'{self.init_path}/test_data/unified_data/traffic_data.csv'
        )

        self.assertTrue(df_equal(link_data, expected_data["link_data"].round(5)))
        self.assertTrue(df_equal(vehicle_data, expected_data["vehicle_data"]))
        self.assertTrue(df_equal(traffic_data, expected_data["traffic_data"]))
        self.assertTrue(df_equal(los_speeds_data, expected_data["los_speeds_data"]))


if __name__ == '__main__':
    main()