from unittest import TestCase, main
import os
import sys
import pandas as pd

from tests.test_script.testScript import execfile
from tests.helper import df_equal


class AcceptanceTestCopertHot(TestCase):

    def setUp(self) -> None:

        self.old_dir = os.getcwd()
        if "tests" in os.getcwd():
            os.chdir("../..")

    def tearDown(self) -> None:

        os.chdir(self.old_dir)

    def test(self):

        sys.argv = f"run_yeti.py -c tests/test_data/acceptance_test_data/acceptance_test_config.yaml".split()
        execfile(f"run_yeti.py")

        emissions_actual = pd.read_csv("tests/test_acceptance_tests/output/PollutantType.NOx_emissions.csv")
        emissions_expected = pd.read_csv("tests/test_data/acceptance_test_data/EMoutput_artificialdata.csv")

        emissions_actual = emissions_actual.sort_values(by=["LinkID", "Dir", "DayType", "Hour"])
        emissions_expected = emissions_expected.sort_values(by=["LinkID", "Dir", "DayType", "Hour"])

        emissions_expected = emissions_expected.round(3)
        emissions_actual = emissions_actual.round(3)

        self.assertTrue(df_equal(emissions_actual, emissions_expected))


if __name__ == '__main__':
    main()
