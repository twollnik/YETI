from unittest import TestCase, main
import pandas as pd

from code.data_loading.loader_utils import convert_dir_and_day_type
from code.constants.enumerations import DayType, Dir
from tests.helper import df_equal


class TestDataLoaderHelpers(TestCase):

    def test_convert_dir_and_day_type(self):

        df = pd.DataFrame({
            "XY": [1, 2, 3, 4],
            "Dir": ["R", Dir.L, "L", "R"],
            "DayType": [DayType.FRI, "1", "2", "3"]
        })

        expected_output = pd.DataFrame({
            "XY": [1, 2, 3, 4],
            "Dir": [Dir.R, Dir.L, Dir.L, Dir.R],
            "DayType": [DayType.FRI, DayType.MONtoTHU, DayType.FRI, DayType.SAT]
        })

        actual_output = convert_dir_and_day_type(df)

        self.assertTrue(df_equal(actual_output, expected_output))


if __name__ == "__main__":
    main()