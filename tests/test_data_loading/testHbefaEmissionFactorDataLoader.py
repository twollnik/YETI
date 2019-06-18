from unittest import TestCase, main
import os
import pandas as pd

from code.data_loading.EmissionFactorDataLoader import HbefaEmissionFactorDataLoader
from tests.helper import df_equal


class testHbefaEmissionFactorDataLoader(TestCase):

    def test_load_data(self):

        if os.path.isfile("./tests/test_data/input_data/hbefa_ef_data.csv"):
            init_path = "./tests"
        else:
            init_path = ".."


        unified_hbefa_ef_data, _ = HbefaEmissionFactorDataLoader(
            ef_data=pd.read_csv(f"{init_path}/test_data/input_data/hbefa_ef_data.csv")
        ).load_data()

        unified_hbefa_ef_data_expected = pd.read_csv(f"{init_path}/test_data/unified_data/hbefa_ef_data.csv")

        self.assertTrue(df_equal(unified_hbefa_ef_data, unified_hbefa_ef_data_expected))


if __name__ == '__main__':
    main()
