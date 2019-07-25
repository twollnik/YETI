from unittest import TestCase, main
from unittest.mock import MagicMock

import numpy as np
import pandas as pd

from code.copert_cold_strategy.CopertColdStrategy import CopertColdStrategy
from code.copert_hot_fixed_speed_strategy.CopertHotFixedSpeedStrategy import CopertHotFixedSpeedStrategy
from code.copert_hot_strategy.CopertHotStrategy import CopertHotStrategy


class TestCopertColdStrategy(TestCase):

    def setUp(self) -> None:
        self.strategy = CopertColdStrategy()

        self.veh_mapping_no_index_set = pd.DataFrame({
            "VehCat": ["Passenger Cars", "Passenger Cars", "Light Commercial Vehicles", "Passenger Cars", "Light Commercial Vehicles"],
            "Fuel": [  "Petrol",         "Petrol",         "Petrol",                    "Petrol",         "Petrol"],
            "VehSegment": ["Mini",       "Mini",           "Small",                     "Large-SUV-Executive", "Small"],
            "EuroStandard": ["Euro 1",   "Euro 3",         "Euro 4",                    "Euro 1",          "Euro 1"],
            "Technology": [np.nan,       "XYZ",            np.nan,                      np.nan,            np.nan],
            "VehName": ["vehA",          "vehB",           "vehC",                      "vehD",            "vehE"]
        })
        self.veh_mapping = self.veh_mapping_no_index_set.set_index("VehName")
        self.cold_ef_table = pd.DataFrame({
            "Pollutant": [  "CO",   "NOx",  "NOx",  "NOx",  "CO",    "CO",    "CO",     "NOx",      "NOx",   "CO"],
            "VehSegment": [ "Mini", "Mini", "Mini", "Mini", "Small", "Small", "Small",  "Small",    "Large-SUV-Executive", "Large-SUV-Executive"],
            "MinSpeed": [   5,      5,      26,     5,      5,      26,       5,        5,          5,      5],
            "MaxSpeed": [   25,     25,     45,     45,     25,     45,       45,       45,         45,     45],
            "MinTemp": [    -20,    -20,    -20,    15,     -20,    -20,      15,       -10,        -10,    -10],
            "MaxTemp": [    15,     15,     15,     100,    15,     15,       100,      100,        100,    100],
            "A": [          10,     1,      2,      3,      4,      5,        6,        3,          3,      3],
            "B": [          20,     4,      5,      6,      7,      8,        9,        3,          3,      3],
            "C": [          30,     7,      8,      9,      10,     11,       12,       3,          3,      3]
        })
        self.vehicle_dict = {
            "vehA": "VehicleCategory.PC",
            "vehB": "VehicleCategory.LCV"
        }
        self.pollutant = "PollutantType.NOx"
        self.pollutants = ["PollutantType.NOx"]
        self.los_speeds_data = pd.DataFrame({
            "LinkID": ["linkA", "linkA"],
            "VehicleCategory": ["VehicleCategory.PC", "VehicleCategory.LCV"],
            "LOS1Speed": [5, 10],
            "LOS2Speed": [20, 20],
            "LOS3Speed": [30, 40],
            "LOS4Speed": [50, 60]
        })
        self.emission_factor_data = pd.DataFrame({
            "VehicleName": ["vehA", "vehB"],
            "Pollutant": ["PollutantType.NOx", "PollutantType.NOx"],
            "Slope": [0, np.nan],
            "Load": [0, np.nan],
            "MaxSpeed": [100, 120],
            "MinSpeed": [10, 5],
            "Alpha": [2, 2],
            "Beta": [0.3, 0.8],
            "Gamma": [2, 3],
            "Delta": [7, 4],
            "Epsilon": [0, 2],
            "Zita": [1, 6],
            "Hta": [4, 9],
            "ReductionPerc": [0, 0.5]
        })
        self.row_dict = {
            "vehA": 10,
            "vehB": 100,
            "vehC": 5,
            "Length": 1,
            "LinkID": "linkA",
            "LOS1Percentage": 0.5,
            "LOS2Percentage": 0.3,
            "LOS3Percentage": 0.1,
            "LOS4Percentage": 1,
            "RoadType": "abc",
            "AreaType": "cde"
        }

        self.strategy.los_speeds_dict = self.los_speeds_data.set_index(["LinkID", "VehicleCategory"]).to_dict(orient="index")
        self.strategy.veh_mapping = self.veh_mapping
        self.strategy.initialize_cold_ef_table(self.cold_ef_table)
        self.strategy.veh_mapping = self.veh_mapping
        self.strategy.los_speeds_data = self.los_speeds_data
        self.strategy.hot_emission_factor_data = self.emission_factor_data
        self.strategy.vehicle_dict = self.vehicle_dict
        self.strategy.row = self.row_dict
        self.strategy.cold_ef_table = self.cold_ef_table
        self.strategy.initialize_hot_strategy()

    def test_calculate_emissions(self):

        strategy = CopertColdStrategy()
        strategy.hot_ef_dict = {"vehD": 5}
        emissions1 = strategy.calculate_emissions(
            traffic_and_link_data_row=self.row_dict,
            vehicle_dict=self.vehicle_dict,
            pollutants=self.pollutants,
            yeti_format_cold_ef_table=self.cold_ef_table,
            yeti_format_los_speeds=self.los_speeds_data,
            yeti_format_vehicle_mapping=self.veh_mapping_no_index_set,
            yeti_format_emission_factors=self.emission_factor_data,
            ltrip=7,
            temperature=10,
            emissions_from_hot_strategy={f"{self.pollutant}": {"vehA": 5, "vehB": 7}}
        )
        emissions2 = strategy.calculate_emissions(
            traffic_and_link_data_row=self.row_dict,
            vehicle_dict=self.vehicle_dict,
            pollutants=self.pollutants,
            emissions_from_hot_strategy={f"{self.pollutant}": {"vehA": 5, "vehB": 7}}
        )

        self.assertTrue(all(item in emissions1 for item in [f"{self.pollutant}_hot", f"{self.pollutant}_cold", f"{self.pollutant}_total"]))
        self.assertTrue(all(item in emissions1[f"{self.pollutant}_hot"] for item in ["vehA", "vehB"]))
        self.assertTrue(all(item in emissions1[f"{self.pollutant}_cold"] for item in ["vehA", "vehB"]))
        self.assertTrue(all(item in emissions1[f"{self.pollutant}_total"] for item in ["vehA", "vehB"]))

        self.assertEqual(emissions1, emissions2)

    def test_configure_hot_strategy_hot_strategy_given(self):

        strategy = CopertColdStrategy()

        strategy.store_data_in_attributes = MagicMock()
        strategy.split_vehicles_into_groups = MagicMock()

        strategy.initialize_if_necessary({}, hot_strategy="code.copert_hot_fixed_speed_strategy.CopertHotFixedSpeedStrategy.CopertHotFixedSpeedStrategy")

        self.assertIsInstance(strategy.hot_strategy, CopertHotFixedSpeedStrategy)

    def test_configure_hot_strategy_no_hot_strategy_given(self):

        strategy = CopertColdStrategy()

        strategy.store_data_in_attributes = MagicMock()
        strategy.split_vehicles_into_groups = MagicMock()

        strategy.initialize_if_necessary({})

        self.assertIsInstance(strategy.hot_strategy, CopertHotStrategy)

    def test_calculate_emissions_with_cng_and_lcv(self):

        strategy = CopertColdStrategy()
        strategy.hot_ef_dict = {"vehA": 5, "vehD": 1}

        veh_mapping_no_index_set = pd.DataFrame({
            "VehCat": ["Passenger Cars", "Passenger Cars", "Passenger Cars", "Passenger Cars"],
            "Fuel": [  "Petrol",         "CNG bi-fuel",    "LPG",            "Petrol"],
            "VehSegment": ["Mini",       "Mini",           "Small",          "Small"],
            "EuroStandard": ["Euro 1",   "Euro 3",         "ECE 15/04",      "ECE 15/04"],
            "Technology": [np.nan,       "XYZ",            np.nan,           np.nan],
            "VehName": ["vehA",          "vehB",           "vehC",           "vehD"]
        })

        emissions1 = strategy.calculate_emissions(
            traffic_and_link_data_row=self.row_dict,
            vehicle_dict=self.vehicle_dict,
            pollutants=self.pollutants,
            yeti_format_cold_ef_table=self.cold_ef_table,
            yeti_format_los_speeds=self.los_speeds_data,
            yeti_format_vehicle_mapping=veh_mapping_no_index_set,
            yeti_format_emission_factors=self.emission_factor_data,
            ltrip=7,
            temperature=10,
            emissions_from_hot_strategy={f"{self.pollutant}": {"vehA": 5, "vehB": 7}}
        )
        emissions2 = strategy.calculate_emissions(
            traffic_and_link_data_row=self.row_dict,
            vehicle_dict=self.vehicle_dict,
            pollutants=self.pollutants,
            emissions_from_hot_strategy={f"{self.pollutant}": {"vehA": 5, "vehB": 7}}
        )

        self.assertTrue(all(item in emissions1 for item in [f"{self.pollutant}_hot", f"{self.pollutant}_cold", f"{self.pollutant}_total"]))
        self.assertTrue(all(item in emissions1[f"{self.pollutant}_hot"] for item in ["vehA", "vehB"]))
        self.assertTrue(all(item in emissions1[f"{self.pollutant}_cold"] for item in ["vehA", "vehB"]))
        self.assertTrue(all(item in emissions1[f"{self.pollutant}_total"] for item in ["vehA", "vehB"]))

        self.assertEqual(emissions1, emissions2)

    def test_calculate_cold_emissions_diesel_lcv(self):

        self.strategy.hot_ef_dict = {'vehA': 5}
        self.strategy.temperature = 7
        self.strategy.ltrip = 9

        self.assertAlmostEqual(
            self.strategy.calculate_cold_emissions_diesel_lcv("PollutantType.CO", "vehA"),
            12.9176625
        )

    def test_calculate_cold_emissions_petrol_lcv_euro(self):

        self.strategy.hot_ef_dict = {"vehE": 4}
        self.strategy.temperature = 5
        self.strategy.ltrip = 12
        self.strategy.vehicle_dict = {"vehC": "VehicleCategory.LCV"}

        self.assertAlmostEqual(
            self.strategy.calculate_cold_emissions_petrol_lcv_euro("PollutantType.CO", "vehC"),
            68.684112
        )

    def test_calculate_cold_emissions_petrol_lcv_pre_euro(self):

        self.strategy.hot_ef_dict = {"vehA": 4}
        self.strategy.temperature = 5
        self.strategy.ltrip = 12
        emissions_actual = self.strategy.calculate_cold_emissions_petrol_lcv_pre_euro("PollutantType.NOx", "vehA")

        emissions_expected = 1.39216
        self.assertAlmostEqual(emissions_expected, emissions_actual)


    def test_get_hot_cold_quotient_petrol_lcv_pre_euro(self):

        strategy = CopertColdStrategy()
        strategy.temperature = 10

        self.assertAlmostEqual(strategy.get_hot_cold_quotient_petrol_lcv_pre_euro("PollutantType.NOx"), 1.08)
        self.assertAlmostEqual(strategy.get_hot_cold_quotient_petrol_lcv_pre_euro("NOx"), 1.08)
        self.assertAlmostEqual(strategy.get_hot_cold_quotient_petrol_lcv_pre_euro("PollutantType.CO"), 2.8)
        self.assertAlmostEqual(strategy.get_hot_cold_quotient_petrol_lcv_pre_euro("CO"), 2.8)
        self.assertAlmostEqual(strategy.get_hot_cold_quotient_petrol_lcv_pre_euro("PollutantType.VOC"), 2.2)
        self.assertAlmostEqual(strategy.get_hot_cold_quotient_petrol_lcv_pre_euro("VOC"), 2.2)

        self.assertRaises(RuntimeError, strategy.get_hot_cold_quotient_petrol_lcv_pre_euro, "PollutantType.XYZ")

    def test_calculate_emissions_for_link_that_should_be_excluded(self):

        strategy = CopertColdStrategy()
        emissions = strategy.calculate_emissions(
            traffic_and_link_data_row={**self.row_dict, "RoadType": "RoadType.MW_City", "AreaType": "AreaType.Urban"},
            vehicle_dict=self.vehicle_dict,
            pollutants=self.pollutants,
            yeti_format_cold_ef_table=self.cold_ef_table,
            yeti_format_los_speeds=self.los_speeds_data,
            yeti_format_vehicle_mapping=self.veh_mapping_no_index_set,
            ltrip=7,
            temperature=10,
            exclude_road_types=["RoadType.MW_City"],
            exclude_aarea_types=["AreaType.Urban"],
            emissions_from_hot_strategy={f"{self.pollutant}": {"vehA": 5, "vehB": 7}}
        )

        self.assertTrue(all(item in emissions for item in [f"{self.pollutant}_hot", f"{self.pollutant}_cold", f"{self.pollutant}_total"]))
        self.assertTrue(all(emissions[f"{self.pollutant}_cold"][item] == 0 for item in ["vehA", "vehB"]))
        self.assertEqual(emissions[f"{self.pollutant}_hot"], emissions[f"{self.pollutant}_total"])

    def test_zero_emissions_for_all_vehicles(self):

        self.assertEqual(
            {"vehA": 0, "vehB": 0},
            self.strategy.zero_emissions_for_all_vehicles()
        )

    def test_should_exclude_link_from_cold_emission_calculation(self):

        strategy = CopertColdStrategy()

        strategy.row = {"RoadType": "a", "AreaType": "rur"}
        self.assertTrue(
            strategy.should_exclude_link_from_cold_emission_calculation(exclude_road_types=["a", "b"]))

        strategy.row = {"RoadType": "a", "AreaType": "urb"}
        self.assertTrue(
            strategy.should_exclude_link_from_cold_emission_calculation(exclude_area_types=["urb"]))

        strategy.row = {"RoadType": "a", "AreaType": "rur"}
        self.assertTrue(
            strategy.should_exclude_link_from_cold_emission_calculation(
                exclude_road_types=["a", "b"], exclude_area_types=["b"]))

        strategy.row = {"RoadType": "a", "AreaType": "urb"}
        self.assertTrue(
            strategy.should_exclude_link_from_cold_emission_calculation(
                exclude_road_types=["a", "b"], exclude_area_types=["urb"]))

        strategy.row = {"RoadType": "c", "AreaType": "rur"}
        self.assertFalse(
            strategy.should_exclude_link_from_cold_emission_calculation(
                exclude_road_types=["a", "b"], exclude_area_types=["urb"], RoadType="c", AreaType="rur"))

        strategy.row = {"RoadType": "c", "AreaType": "rur"}
        self.assertFalse(
            strategy.should_exclude_link_from_cold_emission_calculation(exclude_road_types=["a", "b"]))

        strategy.row = {"RoadType": "c", "AreaType": "x"}
        self.assertFalse(
            strategy.should_exclude_link_from_cold_emission_calculation(exclude_area_types=["a", "b"]))

    def test_join_emissions_into_one_dict(self):

        expected = {
            'Poll_hot': {'a': 1},
            'Poll_cold': {'b': 2},
            'Poll_total': {'c': 3}
        }
        self.strategy.add_emissions_to_assembly_attribute("Poll", {'a': 1}, {'b': 2}, {'c': 3})
        self.assertEqual(expected, self.strategy.emissions)

    def test_calculate_cold_emissions(self):

        hot_ef_dict = {
            "vehA": 1, "vehB": 2, "vehC": 3, "vehD": 4, "vehE": 5
        }
        strategy = CopertColdStrategy()
        strategy.vehicles_pc_petrol_pre_euro = ["vehA"]
        strategy.vehicles_pc_petrol_euro = ["vehB"]
        strategy.vehicles_pc_diesel = ["vehC"]
        strategy.vehicles_lcv_petrol_pre_euro = ["vehD"]
        strategy.vehicles_other = ["vehE"]
        strategy.temperature = 10
        strategy.ltrip = 2
        strategy.row = {
            "Length": 4, "vehA": 5, "vehB": 6, "vehC": 7, "vehD": 10, "LinkID": "linkA",
            "LOS1Percentage": 0.5, "LOS2Percentage": 0.2, "LOS3Percentage": 0.1, "LOS4Percentage": 0
        }
        strategy.vehicle_dict = {
            "vehA": "VehicleCategory.PC",
            "vehB": "VehicleCategory.PC",
            "vehC": "VehicleCategory.PC",
            "vehD": "VehicleCategory.LCV",
            "vehE": "VehicleCategory.HDV"
        }
        strategy.los_speeds_dict = {
            ("linkA", "VehicleCategory.PC"): {"LOS1Speed": 5, "LOS2Speed": 20, "LOS3Speed": 40, "LOS4Speed": 50}
        }
        strategy.veh_mapping = pd.DataFrame({
            "VehName": [    "vehA",     "vehB",     "vehC",     "vehD",     "vehE"],
            "EuroStandard": ["ECE",     "Euro 1",   "Euro 1",   "ECE",      "XYZ"],
            "VehCat": ["VehicleCategory.PC", "VehicleCategory.PC", "VehicleCategory.PC", "VehicleCategory.LCV", "XYZ"],
            "Fuel": [       "Petrol",   "Petrol",   "Diesel",   "Petrol",   "Petrol"],
            "VehSegment": [ "Small",    "Small",    "Small",    "Small",    "Small"]
        }).set_index("VehName")
        strategy.cold_ef_table = pd.DataFrame({
            "Pollutant": ["CO", "NOx", "NOx", "NOx"],
            "VehSegment": ["Small", "Small", "Small", "Small"],
            "MinSpeed": [5, 5, 26, 5],
            "MaxSpeed": [25, 25, 45, 45],
            "MinTemp": [-20, -20, -25, 15],
            "MaxTemp": [15, 15, 15, 100],
            "A": [10, 1, 2, 3],
            "B": [20, 4, 5, 6],
            "C": [30, 7, 8, 9]
        })

        emissions_expected = {
            "vehA": 0.810879999,
            "vehB": 1274.70336,
            "vehC": 7.23710399,
            "vehD": 6.4870399999,
            "vehE": 0
        }
        emissions_actual = strategy.calculate_cold_emissions("PollutantType.NOx", hot_ef_dict)

        self.assertEqual(list(emissions_actual.keys()), ["vehA", "vehB", "vehC", "vehD", "vehE"])
        for veh in ["vehA", "vehB", "vehC", "vehD", "vehE"]:
            self.assertAlmostEqual(emissions_actual[veh], emissions_expected[veh])

    def test_calculate_cold_emissions_lpg_pc_euro(self):

        strategy = CopertColdStrategy()
        strategy.ltrip = 10
        strategy.temperature = 10
        strategy.row = {
            "vehA": 5,
            "Length": 7,
            "LinkID": "linkA",
            "LOS1Percentage": 0.3,
            "LOS2Percentage": 0.5,
            "LOS3Percentage": 0.2,
            "LOS4Percentage": 0
        }
        strategy.hot_ef_dict = {
            "vehB": 1.5
        }
        strategy.veh_mapping = pd.DataFrame({
            "VehCat": ["Passenger Cars", "Passenger Cars"],
            "Fuel": ["Petrol", "Petrol"],
            "VehSegment": ["Mini", "Mini"],
            "EuroStandard": ["Euro 2", "Euro 1"],
            "Technology": [np.nan, np.nan],
            "VehName": ["vehA", "vehB"]
        }).set_index("VehName")
        strategy.cold_ef_table = pd.DataFrame({
            "Pollutant": ["NOx", "NOx", "NOx"],
            "VehSegment": ["Mini", "Mini", "Mini"],
            "MinSpeed": [5, 25, 5],
            "MaxSpeed": [25, 45, 45],
            "MinTemp": [-20, -20, 15],
            "MaxTemp": [15, 15, np.nan],
            "A": [10, 1, 2],
            "B": [20, 4, 5],
            "C": [30, 7, 8]
        })
        strategy.los_speeds_dict = {
            ("linkA", "VehicleCategory.PC"): {
                "LOS1Speed": 5,
                "LOS2Speed": 20,
                "LOS3Speed": 30,
                "LOS4Speed": 50
            }
        }
        strategy.vehicle_dict = {"vehA": "VehicleCategory.PC"}
        strategy.vehicles_pc_lpg_euro = ["vehA"]

        emissions_expected = 3956.737679999
        emissions_actual = strategy.calculate_cold_emissions_lpg_pc_euro("PollutantType.NOx", "vehA")

        self.assertAlmostEqual(emissions_actual, emissions_expected)

    def test_calculate_cold_emissions_for_lpg_pc_pre_euro(self):

        strategy = CopertColdStrategy()
        strategy.ltrip = 10
        strategy.temperature = 10
        strategy.vehicles_pc_lpg_pre_euro = ["vehA"]
        strategy.row = {
            "vehA": 5,
            "Length": 7
        }
        strategy.hot_ef_dict = {
            "vehB": 1.5
        }
        strategy.veh_mapping = pd.DataFrame({
            "VehCat": ["Passenger Cars", "Passenger Cars"],
            "Fuel": ["LPG", "Petrol"],
            "VehSegment": ["Mini", "Mini"],
            "EuroStandard": ["Conventional", "Conventional"],
            "Technology": [np.nan, np.nan],
            "VehName": ["vehA", "vehB"]
        }).set_index("VehName")
        emissions_expected = 30.8616
        emissions_actual = strategy.calculate_cold_emissions_lpg_pc_pre_euro("PollutantType.CO", "vehA")

        self.assertAlmostEqual(emissions_expected, emissions_actual)

    def test_get_cold_hot_quotient_lpg_pre_euro(self):

        strategy = CopertColdStrategy()

        strategy.temperature = -5
        self.assertAlmostEqual(strategy.get_cold_hot_quotient_lpg_pc_pre_euro("PollutantType.NOx"), 1.01)
        strategy.temperature = 10
        self.assertAlmostEqual(strategy.get_cold_hot_quotient_lpg_pc_pre_euro("PollutantType.CO"), 2.76)
        strategy.temperature = 20
        self.assertAlmostEqual(strategy.get_cold_hot_quotient_lpg_pc_pre_euro("PollutantType.VOC"), 1.04)
        strategy.temperature = 30
        self.assertAlmostEqual(strategy.get_cold_hot_quotient_lpg_pc_pre_euro("PollutantType.VOC"), 0.5)

    def test_calculate_cold_emissions_for_diesel_pc(self):

        strategy = CopertColdStrategy()
        strategy.vehicles_pc_diesel = ["vehA", "vehB"]
        strategy.hot_ef_dict = {"vehA": 0.3, "vehB": 2}
        strategy.temperature = 5
        strategy.ltrip = 9
        strategy.row = {"Length": 4, "vehA": 6, "vehB": 12}

        emissions_expected = {"vehA": 0.6547617, "vehB": 8.730156}
        emissions_actual = strategy.calculate_cold_emissions_for_diesel_pc_vehicles("PollutantType.NOx")

        self.assertEqual(list(emissions_actual.keys()), ["vehA", "vehB"])
        for veh in ["vehA", "vehB"]:
            self.assertAlmostEqual(emissions_actual[veh], emissions_expected[veh])

    def test_calculate_cold_emissions_for_petrol_pc_euro(self):

        strategy = CopertColdStrategy()
        strategy.hot_ef_dict = {"vehA": 2, "vehB": 5, "vehC": 7}
        strategy.ltrip = 10
        strategy.temperature = 20
        strategy.row = {
            "Length": 10,
            "vehA": 3,
            "vehB": 6,
            "vehC": 8,
            "LinkID": "linkA",
            "LOS1Percentage": 0.5,
            "LOS2Percentage": 0.2,
            "LOS3Percentage": 0.1,
            "LOS4Percentage": 0
        }
        strategy.vehicles_pc_petrol_euro = ["vehA", "vehB"]
        strategy.los_speeds_dict = {
            ("linkA", "VehicleCategory.PC"): {"LOS1Speed": 5, "LOS2Speed": 20, "LOS3Speed": 40, "LOS4Speed": 50}
        }
        strategy.vehicle_dict = {"vehA": "VehicleCategory.PC", "vehB": "VehicleCategory.PC", "vehC": "VehicleCategory.XYZ"}
        strategy.veh_mapping = pd.DataFrame({
            "VehName": ["vehA", "vehB", "vehC"],
            "EuroStandard": ["Euro 1", "Euro 4", "Conventional"],
            "VehCat": ["VehicleCategory.PC", "VehicleCategory.PC", "VehicleCategory.PC"],
            "Fuel": ["Petrol", "Petrol", "Petrol"],
            "VehSegment": ["Small", "Small", "Mini"]
        }).set_index("VehName")
        strategy.cold_ef_table = pd.DataFrame({
            "Pollutant": ["CO", "NOx", "NOx", "NOx"],
            "VehSegment": ["Small", "Small", "Small", "Small"],
            "MinSpeed": [5, 5, 26, 5],
            "MaxSpeed": [25, 25, 45, 45],
            "MinTemp": [-20, -20, -25, 15],
            "MaxTemp": [15, 15, 15, 100],
            "A": [10, 1, 2, 3],
            "B": [20, 4, 5, 6],
            "C": [30, 7, 8, 9]
        })

        emissions_expected = {
            "vehA": 2210.1534,
            "vehB": 795.655223999
        }
        emissions_actual = strategy.calculate_cold_emissions_for_petrol_pc_euro_vehicles("PollutantType.NOx")
        self.assertEqual(list(emissions_actual.keys()), ["vehA", "vehB"])
        for veh in ["vehA", "vehB"]:
            self.assertAlmostEqual(emissions_actual[veh], emissions_expected[veh])

    def test_calculate_cold_emissions_for_petrol_pc_pre_euro_vehicles(self):

        strategy = CopertColdStrategy()
        strategy.hot_ef_dict = {"vehA": 2, "vehB": 5, "vehC": 7}
        strategy.ltrip = 10
        strategy.temperature = 20
        strategy.row = {"Length": 10, "vehA": 3, "vehB": 6, "vehC": 8}
        strategy.vehicles_pc_petrol_pre_euro = ["vehA", "vehB"]

        emissions_expected = {
            "vehA": 0.33012,
            "vehB": 1.6506
        }
        emissions_actual = strategy.calculate_cold_emissions_for_petrol_pc_pre_euro_vehicles("PollutantType.NOx")
        self.assertEqual(list(emissions_actual.keys()), ["vehA", "vehB"])
        for veh in ["vehA", "vehB"]:
            self.assertAlmostEqual(emissions_actual[veh], emissions_expected[veh])


    def test_calculate_cold_emissions_for_other_vehicles(self):

        strategy = CopertColdStrategy()
        strategy.vehicles_other = ["vehA", "vehB", "vehC"]
        self.assertEqual(
            strategy.calculate_cold_emissions_for_other_vehicles(),
            {"vehA": 0, "vehB": 0, "vehC": 0}
        )

    def test_calculate_total_emissions(self):

        hot_emissions = {
            "vehA": 5,
            "vehB": 10
        }
        cold_emissions = {
            "vehB": 8,
            "vehA": 2
        }
        total_emissions_expected = {
            "vehA": 7,
            "vehB": 18
        }
        strategy = CopertColdStrategy()
        strategy.vehicle_dict = {"vehA": None, "vehB": None}

        total_emissions_actual = strategy.calculate_total_emissions(hot_emissions, cold_emissions)
        self.assertEqual(total_emissions_expected, total_emissions_actual)

        strategy.vehicle_dict = {"vehA": None, "vehB": None, "vehC": None}
        self.assertRaises(KeyError, strategy.calculate_total_emissions, hot_emissions, cold_emissions)

    def test_split_vehicles_into_groups(self):

        vehicle_dict = {
            "vehA": "VehicleCategory.PC",
            "vehB": "VehicleCategory.PC",
            "vehC": "VehicleCategory.PC",
            "vehD": "VehicleCategory.PC",
            "vehE": "VehicleCategory.PC",
            "vehF": "VehicleCategory.PC",
            "vehG": "VehicleCategory.LCV",
            "vehH": "VehicleCategory.LCV",
            "vehI": "VehicleCategory.LCV",
            "vehJ": "VehicleCategory.HDV"
        }
        vehicle_mapping = pd.DataFrame({
            "Fuel":         ["Petrol",   "Petrol",   "Diesel",  "LPG",       "LPG",      "CNG",     "Petrol",       "Petrol",   "Diesel",   "SomeFuel", ],
            "EuroStandard": ["ECE 15/04","Euro 2",   "Euro 1",  "Euro 3",    "ECE",      "Euro 5",  "Conventional", "Euro 6",   "Euro 4",   "SomeEuro"],
            "VehName":      ["vehA",     "vehB",     "vehC",    "vehD",      "vehE",     "vehF",    "vehG",         "vehH",     "vehI",     "vehJ"]
        })
        self.strategy.veh_mapping = vehicle_mapping.set_index("VehName")
        self.strategy.split_vehicles_into_groups(vehicle_dict)

        self.assertEqual(self.strategy.vehicles_pc_petrol_pre_euro, ["vehA"])
        self.assertEqual(self.strategy.vehicles_pc_petrol_euro, ["vehB"])
        self.assertEqual(self.strategy.vehicles_pc_diesel, ["vehC"])
        self.assertEqual(self.strategy.vehicles_pc_lpg_euro, ["vehD"])
        self.assertEqual(self.strategy.vehicles_pc_lpg_pre_euro, ["vehE"])
        self.assertEqual(self.strategy.vehicles_pc_cng, ["vehF"])
        self.assertEqual(self.strategy.vehicles_lcv_petrol_pre_euro, ["vehG"])
        self.assertEqual(self.strategy.vehicles_lcv_petrol_euro, ["vehH"])
        self.assertEqual(self.strategy.vehicles_lcv_diesel, ["vehI"])
        self.assertEqual(self.strategy.vehicles_other, ["vehJ"])

    def test_calculate_cold_emissions_diesel_pc(self):

        self.strategy.ltrip = 0.5
        self.strategy.temperature = 10
        self.strategy.hot_ef_dict = {"vehA": 10, "vehB": 50}
        self.strategy.row = {"vehA": 20, "Length": 10}
        emissions_actual = self.strategy.calculate_cold_emissions_diesel_pc(
            pollutant="PollutantType.NOx", vehicle_name="vehA"
        )
        emissions_expected = 183.328
        self.assertAlmostEqual(emissions_actual, emissions_expected)

    def test_calculate_cold_hot_quotient_diesel_pc_all_euro(self):

        self.strategy.temperature = 5
        self.assertAlmostEqual(self.strategy.get_cold_hot_quotient_for_diesel_vehicle("PollutantType.CO"), 1.75)
        self.strategy.temperature = 7
        self.assertAlmostEqual(self.strategy.get_cold_hot_quotient_for_diesel_vehicle("PollutantType.NOx"), 1.209)
        self.strategy.temperature = 9
        self.assertAlmostEqual(self.strategy.get_cold_hot_quotient_for_diesel_vehicle("PollutantType.VOC"), 2.29)
        self.strategy.temperature = 11
        self.assertAlmostEqual(self.strategy.get_cold_hot_quotient_for_diesel_vehicle("PollutantType.PM"), 2)
        self.strategy.temperature = 30
        self.assertAlmostEqual(self.strategy.get_cold_hot_quotient_for_diesel_vehicle("PollutantType.VOC"), 0.5)
        self.strategy.temperature = 27
        self.assertAlmostEqual(self.strategy.get_cold_hot_quotient_for_diesel_vehicle("PollutantType.PM"), 0.5)

        self.assertRaises(RuntimeError, self.strategy.get_cold_hot_quotient_for_diesel_vehicle, "PollutantType.XYZ")

    def test_calculate_cold_emissions_petrol_pc_past_euro1(self):

        vehicle_dict = {
            "vehA": "VehicleCategory.PC",
            "vehB": "VehicleCategory.PC"
        }
        pollutant = "PollutantType.NOx"
        los_speeds_data = pd.DataFrame({
            "LinkID": ["linkA", "linkA"],
            "VehicleCategory": ["VehicleCategory.PC", "VehicleCategory.LCV"],
            "LOS1Speed": [5, 10],
            "LOS2Speed": [20, 20],
            "LOS3Speed": [30, 40],
            "LOS4Speed": [50, 60]
        })
        self.strategy.hot_ef_dict = {"vehA": 10, "vehB": 50}
        self.strategy.ltrip = 7
        self.strategy.temperature = 10
        self.strategy.row = {
            "LinkID": "linkA",
            "vehB": 20,
            "Length": 10,
            "LOS1Percentage": 0.5,
            "LOS2Percentage": 0.3,
            "LOS3Percentage": 0.1,
            "LOS4Percentage": 1
        }
        self.strategy.vehicle_dict = vehicle_dict
        self.strategy.los_speeds_dict = los_speeds_data.set_index(["LinkID", "VehicleCategory"]).to_dict(orient="index")
        emissions_actual = self.strategy.calculate_cold_emissions_petrol_pc_euro(
            pollutant=pollutant, vehicle_name="vehB"
        )
        emissions_expected = 14548.22399999
        self.assertAlmostEqual(emissions_actual, emissions_expected)

    def test_calculate_cold_emissions_petrol_pc_past_euro1_for_speed(self):

        self.strategy.hot_ef_dict = {"vehA": 10, "vehB": 5000}
        self.strategy.ltrip = 7
        self.strategy.temperature = 10
        self.strategy.row = {"Length": 10, "vehB": 20}
        self.strategy.vehicle_dict = {
            "vehA": "VehicleCategory.PC",
            "vehB": "VehicleCategory.PC"
        }
        emissions_actual = self.strategy.calculate_cold_emissions_petrol_pc_past_euro1_for_speed(
            pollutant="PollutantType.NOx", vehicle_name="vehB", speed=20
        )
        emissions_expected = 16845.312
        self.assertAlmostEqual(emissions_actual, emissions_expected)

    def test_get_euro1_hot_ef(self):

        veh_name = "vehB"
        self.strategy.hot_ef_dict = {"vehA": 10, "vehB": 5000}

        hot_ef_expected = 10
        hot_ef_actual = self.strategy.get_euro1_hot_ef(veh_name)
        self.assertEqual(hot_ef_expected, hot_ef_actual)

    def test_get_cold_hot_qotient_ABC_method(self):

        self.strategy.temperature = 0
        q1 = self.strategy.get_cold_hot_quotient_ABC_method("vehA", "NOx", 10)
        self.strategy.temperature = 10
        self.strategy.ABC_dict = None
        q2 = self.strategy.get_cold_hot_quotient_ABC_method("vehA", "PollutantType.NOx", 20)
        self.strategy.temperature = 20
        self.strategy.ABC_dict = None
        q3 = self.strategy.get_cold_hot_quotient_ABC_method("vehA", "NOx", 30)
        self.strategy.temperature = 15
        self.strategy.ABC_dict = None
        q6 = self.strategy.get_cold_hot_quotient_ABC_method("vehA", "PollutantType.NOx", 26)
        self.strategy.temperature = -10
        self.strategy.ABC_dict = None
        q7 = self.strategy.get_cold_hot_quotient_ABC_method("vehA", "NOx", 40)

        self.assertAlmostEqual(q1, 17)
        self.assertAlmostEqual(q2, 67)
        self.assertAlmostEqual(q3, 219)
        self.assertAlmostEqual(q6, 135)
        self.assertAlmostEqual(q7, 38)

        self.strategy.temperature = 30
        self.strategy.ABC_dict = None
        self.assertRaises(RuntimeError, self.strategy.get_cold_hot_quotient_ABC_method, "vehA", "PollutantType.NOx", 50)

    def test_get_beta_correction_factor(self):

        self.strategy.veh_mapping = pd.DataFrame({
            "VehicleName": ["vehA", "vehB", "vehC", "vehD", "vehE"],
            "EuroStandard": ["Euro 1", "Euro 2", "Euro 4", "Euro 6", "PreEuro"]
        }).set_index("VehicleName")
        self.strategy.vehicle_dict = {
            "vehA": "VehicleCategory.PC",
            "vehB": "VehicleCategory.PC",
            "vehC": "VehicleCategory.LCV",
            "vehD": "VehicleCategory.LCV"
        }

        self.assertEqual(
            self.strategy.get_beta_correction_factor("vehA", "PollutantType.CO"),
            1
        )
        self.assertEqual(
            self.strategy.get_beta_correction_factor("vehB", "PollutantType.NOx"),
            0.72
        )
        self.assertEqual(
            self.strategy.get_beta_correction_factor("vehC", "PollutantType.VOC"),
            0.18
        )
        self.assertEqual(
            self.strategy.get_beta_correction_factor("vehD", "PollutantType.CO"),
            0.18
        )
        self.assertRaises(
            RuntimeError,
            self.strategy.get_beta_correction_factor, "vehA", "PollutantType.NH3"
        )
        self.assertRaises(
            KeyError,
            self.strategy.get_beta_correction_factor, "vehE", "PollutantType.CO"
        )

    def test_calc_cold_emissions_petrol_pc_pre_euro(self):

        emis_expected = 52.556
        self.strategy.hot_ef_dict = {"vehA": 4}
        self.strategy.ltrip = 7
        self.strategy.temperature = 0
        self.strategy.row = {"vehA": 20, "Length":10}
        emis_actual = self.strategy.calculate_cold_emissions_petrol_pc_pre_euro(
            pollutant="PollutantType.NOx", vehicle_name="vehA"
        )
        self.assertAlmostEqual(emis_actual, emis_expected)

        emis_expected = 1013.58
        emis_actual = self.strategy.calculate_cold_emissions_petrol_pc_pre_euro(
            pollutant="PollutantType.CO", vehicle_name="vehA"
        )
        self.assertAlmostEqual(emis_actual, emis_expected)

        emis_expected = 675.72
        emis_actual = self.strategy.calculate_cold_emissions_petrol_pc_pre_euro(
            pollutant="PollutantType.VOC", vehicle_name="vehA"
        )
        self.assertAlmostEqual(emis_actual, emis_expected)

        self.assertRaises(
            RuntimeError,
            self.strategy.calculate_cold_emissions_petrol_pc_pre_euro,
            pollutant="lajoöef", vehicle_name="vehA"
        )

    def test_calculate_cold_emissions_cng_pc(self):

        strategy = CopertColdStrategy()
        strategy.ltrip = 10
        strategy.temperature = 10
        strategy.row = {
            "vehA": 5,
            "Length": 7,
            "LinkID": "linkA",
            "LOS1Percentage": 0.3,
            "LOS2Percentage": 0.5,
            "LOS3Percentage": 0.2,
            "LOS4Percentage": 0
        }
        strategy.hot_ef_dict = {
            "vehB": 1.5
        }
        strategy.veh_mapping = pd.DataFrame({
            "VehCat": ["Passenger Cars", "Passenger Cars"],
            "Fuel": ["CNG bi-fuel", "Petrol"],
            "VehSegment": ["Mini", "Mini"],
            "EuroStandard": ["Euro 2", "Euro 1"],
            "Technology": [np.nan, np.nan],
            "VehName": ["vehA", "vehB"]
        }).set_index("VehName")
        strategy.cold_ef_table = pd.DataFrame({
            "Pollutant": ["CO", "CO", "CO"],
            "VehSegment": ["Mini", "Mini", "Mini"],
            "MinSpeed": [5, 25, 5],
            "MaxSpeed": [25, 45, 45],
            "MinTemp": [-20, -20, 15],
            "MaxTemp": [15, 15, np.nan],
            "A": [10, 1, 2],
            "B": [20, 4, 5],
            "C": [30, 7, 8]
        })
        strategy.los_speeds_dict = {
            ("linkA", "VehicleCategory.PC"): {
                "LOS1Speed": 5,
                "LOS2Speed": 20,
                "LOS3Speed": 30,
                "LOS4Speed": 50
            }
        }
        strategy.vehicle_dict = {"vehA": "VehicleCategory.PC"}

        emissions_expected = 5495.468999986
        emissions_actual = strategy.calculate_cold_emissions_cng_pc("PollutantType.CO", "vehA")

        self.assertAlmostEqual(emissions_expected, emissions_actual)

    def test_get_cold_hot_quotient_ABC_method_for_cng(self):

        strategy = CopertColdStrategy()
        strategy.get_cold_hot_quotient_ABC_method = MagicMock()
        strategy.temperature = 10

        self.assertEqual(
            strategy.get_cold_hot_quotient_ABC_method_for_cng("vehA", "PollutantType.VOC", 30),
            0.212969 * 30 + -0.25526 * 10 + 3.339635
        )

        strategy.get_cold_hot_quotient_ABC_method_for_cng("vehA", "poll", 60)
        strategy.get_cold_hot_quotient_ABC_method.assert_called_once()

    def test_get_cold_hot_quotient_petrol_pc_pre_euro(self):

        self.strategy.temperature = 10
        self.assertAlmostEqual(
            self.strategy.get_cold_hot_quotient_petrol_pc_pre_euro("PollutantType.CO"),
            2.8
        )
        self.assertAlmostEqual(
            self.strategy.get_cold_hot_quotient_petrol_pc_pre_euro("PollutantType.NOx"),
            1.08
        )
        self.assertAlmostEqual(
            self.strategy.get_cold_hot_quotient_petrol_pc_pre_euro("PollutantType.VOC"),
            2.2
        )
        self.assertRaises(
            RuntimeError,
            self.strategy.get_cold_hot_quotient_petrol_pc_pre_euro,"PollutantType.XYZ"
        )

    def test_cold_emissions_formula(self):
        self.assertEqual(
            self.strategy.cold_emissions_formula(
                ltrip=0.5, temp=10, beta_correction_factor=5, num_cars=20, link_length=3,
                ef_hot=1.5, cold_hot_quotient=2),
            242.64
        )
        self.assertEqual(
            self.strategy.cold_emissions_formula(
                ltrip=0.5, temp=10, beta_correction_factor=5, num_cars=20, link_length=3,
                ef_hot=1.5, cold_hot_quotient=0.5),
            0
        )

    def test_calculate_beta(self):

        self.assertEqual(
            self.strategy.calculate_beta(ltrip=0.5, temp=10),
            0.5392
        )
        self.assertAlmostEqual(
            self.strategy.calculate_beta(ltrip=7, temp=0),
            0.46925
        )


if __name__ == '__main__':
    main()