from unittest import TestCase, main
import pandas as pd
import numpy as np

from code.pm_non_exhaust_strategy.PMNonExhaustStrategy import PMNonExhaustStrategy


class TestPMNonExhaustStrategy(TestCase):

    def test_calculate_emissions(self):

        strategy = PMNonExhaustStrategy()
        vehicle_dict = {
            "vehA": "VehicleCategory.PC",
            "vehB": "VehicleCategory.LCV",
            "vehC": "VehicleCategory.HDV"
        }
        los_speeds_data = pd.DataFrame({
            "LinkID": ["linkA", "linkA", "linkA"],
            "VehicleCategory": ["VehicleCategory.PC", "VehicleCategory.LCV", "VehicleCategory.HDV"],
            "LOS1Speed": [5, 10, 7],
            "LOS2Speed": [20, 20, 15],
            "LOS3Speed": [40, 30, 25],
            "LOS4Speed": [50, 40, 40]
        })
        row = {
            "LinkID": "linkA",
            "Length": 12,
            "vehA": 5,
            "vehB": 7,
            "vehC": 0.7,
            "LOS1Percentage": 0.4,
            "LOS2Percentage": 0.1,
            "LOS3Percentage": 0.6,
            "LOS4Percentage": 1
        }
        vehicle_data = pd.DataFrame({
            "VehicleName": ["vehA", "vehB", "vehC"],
            "NumberOfAxles": [np.nan, np.nan, 3]
        })
        load_factor = 0.5

        emissions_expected = {
            "TSP" : {
                "vehA": 4.16852808,
                "vehB": 8.85105984,
                "vehC": 2.429652102149999
            },
            "PM10": {
                "vehA": 2.964643848,
                "vehB": 6.494374152,
                "vehC": 1.7605394407229993
            },
            "PM25": {
                "vehA": 1.5720822936,
                "vehB": 3.4250447448,
                "vehC": 0.8957527108424996
            }
        }
        emissions_actual = strategy.calculate_emissions(
            row, vehicle_dict, "", load_factor=load_factor, los_speeds_data=los_speeds_data, vehicle_data=vehicle_data)

        self.assertAlmostEqual(emissions_actual["TSP"]["vehA"], emissions_expected["TSP"]["vehA"])
        self.assertAlmostEqual(emissions_actual["PM10"]["vehA"], emissions_expected["PM10"]["vehA"])
        self.assertAlmostEqual(emissions_actual["PM25"]["vehA"], emissions_expected["PM25"]["vehA"])

        self.assertAlmostEqual(emissions_actual["TSP"]["vehB"], emissions_expected["TSP"]["vehB"])
        self.assertAlmostEqual(emissions_actual["PM10"]["vehB"], emissions_expected["PM10"]["vehB"])
        self.assertAlmostEqual(emissions_actual["PM25"]["vehB"], emissions_expected["PM25"]["vehB"])

        self.assertAlmostEqual(emissions_actual["TSP"]["vehC"], emissions_expected["TSP"]["vehC"])
        self.assertAlmostEqual(emissions_actual["PM10"]["vehC"], emissions_expected["PM10"]["vehC"])
        self.assertAlmostEqual(emissions_actual["PM25"]["vehC"], emissions_expected["PM25"]["vehC"])

    def test_reformat_emissions_to_right_output_format(self):

        strategy = PMNonExhaustStrategy()
        emissions_raw = {
            "vehA": (1,2,3),
            "vehB": (4,5,6)
        }
        emissions_reformatted_expected = {
            "TSP": {
                "vehA": 1,
                "vehB": 4
            },
            "PM10": {
                "vehA": 2,
                "vehB": 5
            },
            "PM25": {
                "vehA": 3,
                "vehB": 6
            }
        }
        self.assertEqual(strategy.reformat_emissions_to_right_output_format(emissions_raw), emissions_reformatted_expected)

    def test_initialize_number_of_axles_per_vehicle_dict(self):

        vehicle_data = pd.DataFrame({
            "VehicleName": ["vehA", "vehB"],
            "NumberOfAxles": [4, np.nan]
        })
        strategy = PMNonExhaustStrategy()
        strategy.vehicle_dict = {"vehA": "some veh cat", "vehB": "some veh cat"}

        strategy.initialize_number_of_axles_per_vehicle(vehicle_data=vehicle_data)

        self.assertEqual(strategy.number_of_axles_per_vehicle["vehA"], 4.0)
        self.assertTrue(np.isnan(strategy.number_of_axles_per_vehicle["vehB"]))

    def test_add_emission_dicts(self):

        strategy = PMNonExhaustStrategy()
        dict1 = {
            "TSP": 1,
            "PM10": 2,
            "PM25": 3
        }
        dict2 = {
            "TSP": 4,
            "PM10": 5,
            "PM25": 6
        }
        dict3 = {
            "TSP": 7,
            "PM10": 8,
            "PM25": 9
        }
        added_dict_expected = {
            "TSP": 12,
            "PM10": 15,
            "PM25": 18
        }
        self.assertEqual(added_dict_expected, strategy.add_emission_dicts(dict1, dict2, dict3))

    def test_calculate_road_surface_wear_emissions(self):
        strategy = PMNonExhaustStrategy()
        strategy.vehicle_dict = {
            "vehA": "VehicleCategory.PC",
            "vehB": "VehicleCategory.HDV"
        }
        row = {
            "LinkID": "linkA",
            "Length": 12,
            "vehA": 5,
            "vehB": 7
        }

        emissions_actual_vehA = strategy.calculate_road_surface_wear_emissions("vehA", row)
        emissions_expected_vehA = {
            "TSP": 0.9,
            "PM10": 0.45,
            "PM25": 0.243
        }
        self.assertAlmostEqual(emissions_actual_vehA["TSP"], emissions_expected_vehA["TSP"])
        self.assertAlmostEqual(emissions_actual_vehA["PM10"], emissions_expected_vehA["PM10"])
        self.assertAlmostEqual(emissions_actual_vehA["PM25"], emissions_expected_vehA["PM25"])

        emissions_actual_vehB = strategy.calculate_road_surface_wear_emissions("vehB", row)
        emissions_expected_vehB = {
            "TSP": 6.384,
            "PM10": 3.192,
            "PM25": 1.72368
        }
        self.assertAlmostEqual(emissions_actual_vehB["TSP"], emissions_expected_vehB["TSP"])
        self.assertAlmostEqual(emissions_actual_vehB["PM10"], emissions_expected_vehB["PM10"])
        self.assertAlmostEqual(emissions_actual_vehB["PM25"], emissions_expected_vehB["PM25"])

    def test_get_road_surface_wear_ef_for_vehicle(self):

        strategy = PMNonExhaustStrategy()
        strategy.vehicle_dict = {
            "vehA": "VehicleCategory.PC",
            "vehB": "VehicleCategory.LCV",
            "vehC": "VehicleCategory.MC",
            "vehD": "VehicleCategory.Moped",
            "vehE": "VehicleCategory.HDV",
            "vehF": "VehicleCategory.UBus",
            "vehG": "VehicleCategory.Coach"
        }
        strategy.load_factor = 0.5

        self.assertEqual(strategy.get_road_surface_wear_ef_for_vehicle("vehA"), 0.015)
        self.assertEqual(strategy.get_road_surface_wear_ef_for_vehicle("vehB"), 0.015)
        self.assertEqual(strategy.get_road_surface_wear_ef_for_vehicle("vehC"), 0.006)
        self.assertEqual(strategy.get_road_surface_wear_ef_for_vehicle("vehD"), 0.006)
        self.assertAlmostEqual(strategy.get_road_surface_wear_ef_for_vehicle("vehE"), 0.076)
        self.assertAlmostEqual(strategy.get_road_surface_wear_ef_for_vehicle("vehF"), 0.076)
        self.assertAlmostEqual(strategy.get_road_surface_wear_ef_for_vehicle("vehG"), 0.076)

    def test_calculate_break_wear_emissions(self):

        strategy = PMNonExhaustStrategy()
        strategy.vehicle_dict = {
            "vehA": "VehicleCategory.PC",
            "vehB": "VehicleCategory.LCV"
        }
        strategy.los_speeds_dict = {
            ("linkA", "VehicleCategory.PC"): {"LOS1Speed": 5, "LOS2Speed": 20, "LOS3Speed": 40, "LOS4Speed": 50},
            ("linkA", "VehicleCategory.LCV"): {"LOS1Speed": 10, "LOS2Speed": 20, "LOS3Speed": 30, "LOS4Speed": 40}
        }
        row = {
            "LinkID": "linkA",
            "Length": 12,
            "vehA": 5,
            "vehB": 7,
            "LOS1Percentage": 0.4,
            "LOS2Percentage": 0.1,
            "LOS3Percentage": 0.6,
            "LOS4Percentage": 1
        }

        emissions_actual_vehA = strategy.calculate_break_wear_emissions("vehA", row)
        emissions_expected_vehA = {
            "TSP": 1.45665,
            "PM10": 1.427517,
            "PM25": 0.5680935
        }
        self.assertAlmostEqual(emissions_actual_vehA["TSP"], emissions_expected_vehA["TSP"])
        self.assertAlmostEqual(emissions_actual_vehA["PM10"], emissions_expected_vehA["PM10"])
        self.assertAlmostEqual(emissions_actual_vehA["PM25"], emissions_expected_vehA["PM25"])

        emissions_actual_vehB = strategy.calculate_break_wear_emissions("vehB", row)
        emissions_expected_vehB = {
            "TSP": 3.4466796,
            "PM10": 3.377746008,
            "PM25": 1.344205044

        }
        self.assertAlmostEqual(emissions_actual_vehB["TSP"], emissions_expected_vehB["TSP"])
        self.assertAlmostEqual(emissions_actual_vehB["PM10"], emissions_expected_vehB["PM10"])
        self.assertAlmostEqual(emissions_actual_vehB["PM25"], emissions_expected_vehB["PM25"])

    def test_calculate_break_wear_speed_factor(self):

        strategy = PMNonExhaustStrategy()
        self.assertAlmostEqual(1.67, strategy.calculate_break_wear_speed_factor(30))
        self.assertAlmostEqual(1.535, strategy.calculate_break_wear_speed_factor(45))
        self.assertAlmostEqual(0.32, strategy.calculate_break_wear_speed_factor(90))
        self.assertAlmostEqual(0.185, strategy.calculate_break_wear_speed_factor(100))

    def test_get_break_wear_ef_for_vehicle(self):

        strategy = PMNonExhaustStrategy()
        strategy.vehicle_dict = {
            "vehA": "VehicleCategory.PC",
            "vehB": "VehicleCategory.LCV",
            "vehC": "VehicleCategory.MC",
            "vehD": "VehicleCategory.Moped",
            "vehE": "VehicleCategory.HDV",
            "vehF": "VehicleCategory.UBus",
            "vehG": "VehicleCategory.Coach"
        }
        strategy.load_factor = 0.5

        self.assertEqual(strategy.get_break_wear_ef_for_vehicle("vehA"), 0.0075)
        self.assertEqual(strategy.get_break_wear_ef_for_vehicle("vehB"), 0.0117)
        self.assertEqual(strategy.get_break_wear_ef_for_vehicle("vehC"), 0.0037)
        self.assertEqual(strategy.get_break_wear_ef_for_vehicle("vehD"), 0.0037)
        self.assertAlmostEqual(strategy.get_break_wear_ef_for_vehicle("vehE"), 0.032747625)
        self.assertAlmostEqual(strategy.get_break_wear_ef_for_vehicle("vehF"), 0.032747625)
        self.assertAlmostEqual(strategy.get_break_wear_ef_for_vehicle("vehG"), 0.032747625)

    def test_ef_break_wear_hdv_ubus_coach(self):

        self.assertAlmostEqual(
            PMNonExhaustStrategy().ef_break_wear_hdv_ubus_coach(0.5),
            0.032747625
        )

    def test_calculate_tyre_wear_emissions(self):

        strategy = PMNonExhaustStrategy()
        strategy.vehicle_dict = {
            "vehA": "VehicleCategory.PC",
            "vehB": "VehicleCategory.LCV"
        }
        strategy.los_speeds_dict = {
            ("linkA", "VehicleCategory.PC"): {"LOS1Speed": 5, "LOS2Speed": 20, "LOS3Speed": 40, "LOS4Speed": 50},
            ("linkA", "VehicleCategory.LCV"): {"LOS1Speed": 10, "LOS2Speed": 20, "LOS3Speed": 30, "LOS4Speed": 40}
        }
        row = {
            "LinkID": "linkA",
            "Length": 12,
            "vehA": 5,
            "vehB": 7,
            "LOS1Percentage": 0.4,
            "LOS2Percentage": 0.1,
            "LOS3Percentage": 0.6,
            "LOS4Percentage": 1
        }

        emissions_actual_vehA = strategy.calculate_tyre_wear_emissions("vehA", row)
        emissions_expected_vehA = {
            "TSP": 1.81187808,
            "PM10": 1.087126848,
            "PM25": 0.7609887936
        }
        self.assertEqual(emissions_actual_vehA, emissions_expected_vehA)

        emissions_actual_vehB = strategy.calculate_tyre_wear_emissions("vehB", row)
        emissions_expected_vehB = {
            "TSP": 4.14438024,
            "PM10": 2.486628144,
            "PM25": 1.7406397008
        }
        self.assertAlmostEqual(emissions_actual_vehB["TSP"], emissions_expected_vehB["TSP"])
        self.assertAlmostEqual(emissions_actual_vehB["PM10"], emissions_expected_vehB["PM10"])
        self.assertAlmostEqual(emissions_actual_vehB["PM25"], emissions_expected_vehB["PM25"])

    def test_get_tyre_wear_ef_for_vehicle(self):

        strategy = PMNonExhaustStrategy()
        strategy.vehicle_dict = {
            "vehA": "VehicleCategory.PC",
            "vehB": "VehicleCategory.LCV",
            "vehC": "VehicleCategory.MC",
            "vehD": "VehicleCategory.Moped",
            "vehE": "VehicleCategory.HDV",
            "vehF": "VehicleCategory.UBus",
            "vehG": "VehicleCategory.Coach"
        }
        strategy.number_of_axles_per_vehicle = {
            "vehE": 4,
            "vehF": 4,
            "vehG": 4
        }
        strategy.load_factor = 0.5

        self.assertEqual(strategy.get_tyre_wear_ef_for_vehicle("vehA"), 0.0107)
        self.assertEqual(strategy.get_tyre_wear_ef_for_vehicle("vehB"), 0.0169)
        self.assertEqual(strategy.get_tyre_wear_ef_for_vehicle("vehC"), 0.0046)
        self.assertEqual(strategy.get_tyre_wear_ef_for_vehicle("vehD"), 0.0046)
        self.assertAlmostEqual(strategy.get_tyre_wear_ef_for_vehicle("vehE"), 0.04494)
        self.assertAlmostEqual(strategy.get_tyre_wear_ef_for_vehicle("vehF"), 0.04494)
        self.assertAlmostEqual(strategy.get_tyre_wear_ef_for_vehicle("vehG"), 0.04494)

    def test_emissions_formula(self):

        strategy = PMNonExhaustStrategy()
        self.assertEqual(
            720,
            strategy.emissions_formula(2, 3, 4, 5, 6)
        )

    def test_calculate_tyre_wear_speed_factor(self):

        strategy = PMNonExhaustStrategy()
        self.assertAlmostEqual(1.39, strategy.calculate_tyre_wear_speed_factor(30))
        self.assertAlmostEqual(1.293, strategy.calculate_tyre_wear_speed_factor(50))
        self.assertAlmostEqual(0.902, strategy.calculate_tyre_wear_speed_factor(100))

    def test_ef_tyre_wear_hdv_ubus_coach(self):

        strategy = PMNonExhaustStrategy()
        strategy.number_of_axles_per_vehicle = {
            "vehA": 4,
            "vehB": 2
        }
        self.assertAlmostEqual(
            0.04494,
            strategy.ef_tyre_wear_hdv_ubus_coach(vehicle_name="vehA", load_factor=0.5)
        )
        self.assertAlmostEqual(
            0.015087,
            strategy.ef_tyre_wear_hdv_ubus_coach(vehicle_name="vehB", load_factor=0)
        )

if __name__ == '__main__':
    main()