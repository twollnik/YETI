from unittest import TestCase, main
import os

from code.copert_hot_strategy.load_unified_data import load_copert_unified_data


class TestUseNTrafficDataRows(TestCase):

    def test_use_n_traffic_data_rows(self):

        if os.path.isfile("./tests/test_data/unified_data/emission_factor_data.csv"):
            self.init_path = "./tests"
        else:
            self.init_path = ".."

        kwargs = {
            'unified_emission_factors': f'{self.init_path}/test_data/unified_data/emission_factor_data.csv',
            'unified_los_speeds': f'{self.init_path}/test_data/unified_data/los_speeds_data.csv',
            'unified_vehicle_data': f'{self.init_path}/test_data/unified_data/vehicle_data.csv',
            'unified_link_data': f'{self.init_path}/test_data/unified_data/link_data.csv',
            'unified_traffic_data': f'{self.init_path}/test_data/unified_data/traffic_data.csv',
            'use_n_traffic_data_rows': 2
        }

        data = load_copert_unified_data(**kwargs)

        self.assertEqual(2, len(data["traffic_data"]))


if __name__ == "__main__":
    main()