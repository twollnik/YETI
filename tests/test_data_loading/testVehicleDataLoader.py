from unittest import TestCase, main
import pandas as pd
import os

from code.data_loading.VehicleDataLoader import VehicleDataLoader
from tests.helper import df_equal


class TestVehicleDataLoader(TestCase):

    def test_load_data(self):

        if os.path.isfile("./tests/test_data/input_data/fleet_comp_data.csv"):
            init_path = "./tests"
        else:
            init_path = ".."

        vehicle_data = VehicleDataLoader(
            fleet_comp_data=pd.read_csv(f"{init_path}/test_data/input_data/fleet_comp_data.csv")
        ).load_data()

        vehicle_data_expected = pd.read_csv(f"{init_path}/test_data/unified_data/vehicle_data.csv")

        self.assertTrue(df_equal(vehicle_data, vehicle_data_expected))


if __name__ == "__main__":
    main()
