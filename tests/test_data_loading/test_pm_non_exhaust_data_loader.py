import os
from unittest import TestCase, main

from code.data_loading.PMNonExhaustDataLoader import PMNonExhaustDataLoader
from code.pm_non_exhaust_strategy.load_yeti_format_data import load_pm_non_exhaust_yeti_format_data
from tests.helpers_and_mocks import df_equal


class TestPMNonExhaustDataLoader(TestCase):

    def test_load_data(self):

        if os.path.isfile("./tests/test_data/berlin_format_data/shape_data.csv"):
            self.init_path = "./tests"
        else:
            self.init_path = ".."

        loader = PMNonExhaustDataLoader(
            link_data_file=f'{self.init_path}/test_data/berlin_format_data/shape_data.csv',
            fleet_comp_file=f'{self.init_path}/test_data/berlin_format_data/fleet_comp_data.csv',
            los_speeds_file=f'{self.init_path}/test_data/berlin_format_data/los_speed_data.csv',
            traffic_data_file=f'{self.init_path}/test_data/berlin_format_data/traffic_data.csv'
        )
        (link_data, vehicle_data, traffic_data, los_speeds_data, _, _) = loader.load_data()

        expected_data = load_pm_non_exhaust_yeti_format_data(
            yeti_format_los_speeds=f'{self.init_path}/test_data/yeti_format_data/los_speeds_data.csv',
            yeti_format_vehicle_data=f'{self.init_path}/test_data/yeti_format_data/vehicle_data.csv',
            yeti_format_link_data=f'{self.init_path}/test_data/yeti_format_data/link_data.csv',
            yeti_format_traffic_data=f'{self.init_path}/test_data/yeti_format_data/traffic_data.csv'
        )

        self.assertTrue(df_equal(link_data, expected_data["link_data"].round(5)))
        self.assertTrue(df_equal(vehicle_data, expected_data["vehicle_data"]))
        self.assertTrue(df_equal(traffic_data, expected_data["traffic_data"]))
        self.assertTrue(df_equal(los_speeds_data, expected_data["los_speeds_data"]))


if __name__ == '__main__':
    main()