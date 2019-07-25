import os
from unittest import TestCase, main

import pandas as pd

from code.data_loading.LinkDataLoader import LinkDataLoader
from tests.helper import df_equal


class TestLinkDataLoader(TestCase):

    def test_link_data_loader(self) -> None:

        if os.path.isfile("./tests/test_data/berlin_format_data/shape_data.csv"):
            self.init_path = "./tests"
        else:
            self.init_path = ".."

        link_data = LinkDataLoader(
            link_data=pd.read_csv(f"{self.init_path}/test_data/berlin_format_data/shape_data.csv")
        ).load_data()

        link_data_with_speed = LinkDataLoader(
            link_data=pd.read_csv(f"{self.init_path}/test_data/berlin_format_data/shape_data_with_speed.csv")
        ).load_data()

        link_data_expected = pd.read_csv(f"{self.init_path}/test_data/yeti_format_data/link_data.csv")
        link_data_with_speed_expected = pd.read_csv(f"{self.init_path}/test_data/yeti_format_data/link_data_with_speed.csv")

        self.assertTrue(df_equal(link_data, link_data_expected))
        self.assertTrue(df_equal(link_data_with_speed, link_data_with_speed_expected))


if __name__ == "__main__":
    main()
