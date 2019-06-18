from unittest import TestCase, main
import os
import pandas as pd

from code.data_loading.TrafficDataLoader import TrafficDataLoader
from tests.helper import df_equal


class TestTrafficDataLoader(TestCase):

    def test_load_data(self):

        if os.path.isfile("./tests/test_data/input_data/traffic_data.csv"):
            init_path = "./tests"
        else:
            init_path = ".."

        traffic_data = TrafficDataLoader(
            fleet_comp_data=pd.read_csv(f"{init_path}/test_data/input_data/fleet_comp_data.csv"),
            link_data=pd.read_csv(f"{init_path}/test_data/input_data/shape_data.csv"),
            traffic_count_data=pd.read_csv(f"{init_path}/test_data/input_data/traffic_data.csv")
        ).load_data()

        traffic_data_expected = pd.read_csv(f"{init_path}/test_data/unified_data/traffic_data.csv")

        self.assertTrue(df_equal(traffic_data, traffic_data_expected))


if __name__ == "__main__":
    main()
