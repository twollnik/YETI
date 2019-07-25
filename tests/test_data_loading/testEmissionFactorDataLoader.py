import os
from unittest import TestCase, main

import pandas as pd

from code.constants.enumerations import PollutantType
from code.data_loading.EmissionFactorDataLoader import EmissionFactorDataLoader
from tests.helpers_and_mocks import df_equal


class TestEmissionFactorDataLoader(TestCase):

    def setUp(self) -> None:

        if os.path.isfile("./tests/test_data/berlin_format_data/copert_emission_factor_data.csv"):
            self.init_path = "./tests"
        else:
            self.init_path = ".."

        self.loader = EmissionFactorDataLoader(
            fleet_comp_data=pd.read_csv(f"{self.init_path}/test_data/berlin_format_data/fleet_comp_data.csv"),
            vehicle_mapping_data=pd.read_csv(f"{self.init_path}/test_data/berlin_format_data/vehicle_emissions_category_mapping_data.csv"),
            ef_data=pd.read_csv(f"{self.init_path}/test_data/berlin_format_data/copert_emission_factor_data.csv"),
            nh3_ef_data=pd.read_csv(f"{self.init_path}/test_data/berlin_format_data/nh3_ef_data.csv"),
            nh3_mapping_data=pd.read_csv(f"{self.init_path}/test_data/berlin_format_data/nh3_mapping.csv")
        )

    def test_load_data(self):

        ef_data, missing_ef_data = self.loader.load_data()
        ef_data_expected = pd.read_csv(f"{self.init_path}/test_data/yeti_format_data/emission_factor_data.csv")

        self.assertEqual(sorted(list(ef_data_expected.columns)), sorted(list(ef_data.columns)))
        self.assertTrue(df_equal(ef_data, ef_data_expected))

    def test_load_speed_dependent_ef_data(self):

        speed_dependent_ef_data = self.loader.load_speed_dependent_ef_data()
        speed_dependent_ef_data_expected = pd.read_csv(f"{self.init_path}/test_data/other_data/speed_dependent_ef_data.csv")

        self.assertFalse(speed_dependent_ef_data_expected.empty)
        self.assertFalse(speed_dependent_ef_data.empty)

        self.assertTrue(df_equal(speed_dependent_ef_data, speed_dependent_ef_data_expected))

    def test_load_nh3_ef_data(self):

        nh3_ef_data = self.loader.load_nh3_ef_data()

        nh3_ef_data_expected = pd.DataFrame({
            "VehicleName": ["pc vehicle_a", "lcv vehicle_b"],
            "EF": [1, 2.5],
            "Pollutant": ["PollutantType.NH3", "PollutantType.NH3"]
        })

        self.assertTrue(df_equal(nh3_ef_data, nh3_ef_data_expected))

    def test_determine_missing_ef_data(self):

        ef_data = pd.DataFrame({
            "VehicleName": ["pc vehicle_a", "pc vehicle_a", "pc vehicle_b"],
            "Pollutant": [PollutantType.NOx, PollutantType.NH3, PollutantType.CO]
        })
        missing_ef_data_expected = pd.DataFrame({
            "Pollutant": [PollutantType.CO, PollutantType.VOC, PollutantType.PM_Exhaust, PollutantType.NOx,
                          PollutantType.CO, PollutantType.NH3, PollutantType.VOC, PollutantType.PM_Exhaust],
            "VehicleName": ["pc vehicle_a", "pc vehicle_a", "pc vehicle_a", "lcv vehicle_b",
                            "lcv vehicle_b", "lcv vehicle_b", "lcv vehicle_b", "lcv vehicle_b"]
        })
        missing_ef_data = self.loader.determine_missing_ef_data(ef_data)

        self.assertTrue(df_equal(missing_ef_data, missing_ef_data_expected))

    def test_use_nh3_tier2_ef_false(self):

        loader = EmissionFactorDataLoader(
            use_nh3_tier2_ef=False,
            fleet_comp_data=pd.read_csv(f"{self.init_path}/test_data/berlin_format_data/fleet_comp_data.csv"),
            vehicle_mapping_data=pd.read_csv(
                f"{self.init_path}/test_data/berlin_format_data/vehicle_emissions_category_mapping_data.csv"),
            ef_data=pd.read_csv(f"{self.init_path}/test_data/berlin_format_data/copert_emission_factor_data.csv"),
            nh3_ef_data=pd.read_csv(f"{self.init_path}/test_data/berlin_format_data/nh3_ef_data.csv"),
            nh3_mapping_data=pd.read_csv(f"{self.init_path}/test_data/berlin_format_data/nh3_mapping.csv")
        )
        ef_data, missing_ef_data = loader.load_data()

        self.assertEqual(len(ef_data), 11)
        self.assertTrue({"VehicleName", "Pollutant", "MinSpeed", "MaxSpeed", "Alpha", "Beta", "Gamma", "Delta",
                         "Epsilon", "Zita", "Hta", "Thita", "ReductionPerc", "Mode", "Slope", "Load"}.issubset(ef_data.columns))

        self.assertEqual(len(missing_ef_data), 5)


if __name__ == "__main__":
    main()
