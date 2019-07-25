import os
from unittest import TestCase, main

from code.copert_hot_strategy.load_yeti_format_data import load_copert_hot_yeti_format_data


class TestYetiFormatDataLoader(TestCase):

    def setUp(self) -> None:

        if os.path.isfile("./tests/test_data/yeti_format_data/emission_factor_data.csv"):
            self.init_path = "./tests"
        else:
            self.init_path = ".."

        yeti_format_data = load_copert_hot_yeti_format_data(
            yeti_format_emission_factors=f'{self.init_path}/test_data/yeti_format_data/emission_factor_data.csv',
            yeti_format_los_speeds=f'{self.init_path}/test_data/yeti_format_data/los_speeds_data.csv',
            yeti_format_vehicle_data=f'{self.init_path}/test_data/yeti_format_data/vehicle_data.csv',
            yeti_format_link_data=f'{self.init_path}/test_data/yeti_format_data/link_data.csv',
            yeti_format_traffic_data=f'{self.init_path}/test_data/yeti_format_data/traffic_data.csv',
        )
        self.link_data = yeti_format_data["link_data"]
        self.vehicle_data = yeti_format_data["vehicle_data"]
        self.traffic_data = yeti_format_data["traffic_data"]
        self.los_speeds_data = yeti_format_data["los_speeds_data"]
        self.emission_factor_data = yeti_format_data["emission_factor_data"]

        yeti_format_data = load_copert_hot_yeti_format_data(
            yeti_format_emission_factors=f'{self.init_path}/test_data/yeti_format_data/emission_factor_data.csv',
            yeti_format_los_speeds=f'{self.init_path}/test_data/yeti_format_data/los_speeds_data.csv',
            yeti_format_vehicle_data=f'{self.init_path}/test_data/yeti_format_data/vehicle_data.csv',
            yeti_format_link_data=f"{self.init_path}/test_data/yeti_format_data/link_data_with_speed.csv",
            yeti_format_traffic_data=f'{self.init_path}/test_data/yeti_format_data/traffic_data.csv',
        )
        self.link_data_speed = yeti_format_data["link_data"]
        self.vehicle_data_speed = yeti_format_data["vehicle_data"]
        self.traffic_data_speed = yeti_format_data["traffic_data"]
        self.los_speeds_data_speed = yeti_format_data["los_speeds_data"]
        self.emission_factor_data_speed = yeti_format_data["emission_factor_data"]

    def test_yeti_format_data_loader_columns(self):

        self.assertTrue({
            "VehicleName", "Pollutant", "MinSpeed", "MaxSpeed",
            "Alpha", "Beta", "Gamma", "Delta", "Epsilon", "Zita",
            "Hta", "Thita", "ReductionPerc", "EF", "Mode", "Slope", "Load"
        }.issubset(self.emission_factor_data.columns))

        self.assertTrue({
            "LinkID", "Length", "RoadType", "AreaType"
        }.issubset(self.link_data.columns))
        self.assertTrue({
            "LinkID", "Length", "RoadType", "AreaType", "Speed"
        }.issubset(self.link_data_speed.columns))

        self.assertTrue({
            "LinkID", "Dir", "DayType", "Hour", "pc vehicle_a", "lcv vehicle_b",
            "LOS1Percentage", "LOS2Percentage", "LOS3Percentage", "LOS4Percentage"
        }.issubset(self.traffic_data.columns))

        self.assertTrue({
            "VehicleName", "VehicleCategory"
        }.issubset(self.vehicle_data.columns))

        self.assertTrue({
            "LinkID", "VehicleCategory", "LOS1Speed", "LOS2Speed", "LOS3Speed", "LOS4Speed"
        }.issubset(self.los_speeds_data.columns))

    def test_behaviour_with_speed_unchanged(self):

        self.assertTrue(self.emission_factor_data.equals(self.emission_factor_data_speed))
        self.assertTrue(self.traffic_data.equals(self.traffic_data_speed))
        self.assertTrue(self.vehicle_data.equals(self.vehicle_data_speed))
        self.assertTrue(self.los_speeds_data.equals(self.los_speeds_data_speed))
    
    def test_dataframe_lengths(self):
        self.assertEqual(len(self.emission_factor_data), 13)
        self.assertEqual(len(self.link_data), 2)
        self.assertEqual(len(self.traffic_data), 288)
        self.assertEqual(len(self.vehicle_data), 2)
        self.assertEqual(len(self.los_speeds_data), 4)

if __name__ == "__main__":
    main()