"""
Test the script calc_average_daily_emissions.py.
The emissions data in tests/test_data/emissions_data_for_testing.csv is used to do this testing.
"""

from unittest import TestCase, main
import os

from calc_average_daily_emissions import calc_avg_daily_emissions


class TestCalcAvgDailyEmissions(TestCase):

    def test_script(self):

        if os.path.isfile("tests/test_data/emissions_data_for_testing.csv"):
            path_prefix = "."
        else:
            path_prefix = ".."

        avg_daiy_emissions = calc_avg_daily_emissions(f"{path_prefix}/tests/test_data/emissions_data_for_testing.csv")
        self.assertEqual(avg_daiy_emissions, 4391.283455942606)


if __name__ == "__main__":
    main()
