import os
from unittest import TestCase, main

from code.copert_hot_strategy.load_yeti_format_data import load_copert_hot_yeti_format_data


class TestUseNTrafficDataRows(TestCase):

    def test_use_n_traffic_data_rows(self):

        if os.path.isfile("./tests/test_data/yeti_format_data/emission_factor_data.csv"):
            self.init_path = "./tests"
        else:
            self.init_path = ".."

        kwargs = {
            'yeti_format_emission_factors': f'{self.init_path}/test_data/yeti_format_data/emission_factor_data.csv',
            'yeti_format_los_speeds': f'{self.init_path}/test_data/yeti_format_data/los_speeds_data.csv',
            'yeti_format_vehicle_data': f'{self.init_path}/test_data/yeti_format_data/vehicle_data.csv',
            'yeti_format_link_data': f'{self.init_path}/test_data/yeti_format_data/link_data.csv',
            'yeti_format_traffic_data': f'{self.init_path}/test_data/yeti_format_data/traffic_data.csv',
            'use_n_traffic_data_rows': 2
        }

        data = load_copert_hot_yeti_format_data(**kwargs)

        self.assertEqual(2, len(data["traffic_data"]))


if __name__ == "__main__":
    main()