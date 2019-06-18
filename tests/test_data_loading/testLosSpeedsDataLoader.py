from unittest import TestCase, main
import pandas as pd
import os

from code.data_loading.LosSpeedsDataLoader import LosSpeedsDataLoader
from tests.helper import df_equal


class TestLosSpeedsDataLoader(TestCase):

    def test_load_data(self):

        if os.path.isfile("./tests/test_data/input_data/shape_data.csv"):
            init_path = "./tests"
        else:
            init_path = ".."

        los_speeds_data_no_speed_in_link_data = LosSpeedsDataLoader(
            link_data=pd.read_csv(f"{init_path}/test_data/input_data/shape_data.csv"),
            los_speeds_data=pd.read_csv(f"{init_path}/test_data/input_data/los_speed_data.csv")
        ).load_data()
        los_speeds_data_with_speed_in_link_data = LosSpeedsDataLoader(
            link_data=pd.read_csv(f"{init_path}/test_data/input_data/shape_data_with_speed.csv"),
            los_speeds_data=pd.read_csv(f"{init_path}/test_data/input_data/los_speed_data.csv")
        ).load_data()

        self.assertTrue(df_equal(los_speeds_data_no_speed_in_link_data, los_speeds_data_with_speed_in_link_data))

        los_speeds_data_expected = pd.read_csv(f"{init_path}/test_data/unified_data/los_speeds_data.csv")

        self.assertTrue(df_equal(los_speeds_data_no_speed_in_link_data, los_speeds_data_expected))


if __name__ == "__main__":
    main()
