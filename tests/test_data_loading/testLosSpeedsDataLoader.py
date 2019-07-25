import os
from unittest import TestCase, main

import pandas as pd

from code.data_loading.LosSpeedsDataLoader import LosSpeedsDataLoader
from tests.helper import df_equal


class TestLosSpeedsDataLoader(TestCase):

    def setUp(self) -> None:

        self.link_data = pd.DataFrame.from_dict({
            "LinkID": ["linkA"],
            "AreaCat": ["1"],
            "RoadCat": ["5"],
            "MaxSpeed_kmh": ["100"]
        })

    def test_load_data(self):

        if os.path.isfile("./tests/test_data/berlin_format_data/shape_data.csv"):
            init_path = "./tests"
        else:
            init_path = ".."

        los_speeds_data_no_speed_in_link_data = LosSpeedsDataLoader(
            link_data=pd.read_csv(f"{init_path}/test_data/berlin_format_data/shape_data.csv"),
            los_speeds_data=pd.read_csv(f"{init_path}/test_data/berlin_format_data/los_speed_data.csv")
        ).load_data()
        los_speeds_data_with_speed_in_link_data = LosSpeedsDataLoader(
            link_data=pd.read_csv(f"{init_path}/test_data/berlin_format_data/shape_data_with_speed.csv"),
            los_speeds_data=pd.read_csv(f"{init_path}/test_data/berlin_format_data/los_speed_data.csv")
        ).load_data()

        self.assertTrue(df_equal(los_speeds_data_no_speed_in_link_data, los_speeds_data_with_speed_in_link_data))

        los_speeds_data_expected = pd.read_csv(f"{init_path}/test_data/yeti_format_data/los_speeds_data.csv")

        self.assertTrue(df_equal(los_speeds_data_no_speed_in_link_data, los_speeds_data_expected))

    def test_veh_category_coach(self):

        los_speeds_data = pd.DataFrame.from_dict({
            "VehCat": ["coach"],
            "TrafficSituation": ["URB/MW-City/100/Freeflow"],
            "Speed_kmh": [20]
        })
        loader = LosSpeedsDataLoader(
            link_data=self.link_data,
            los_speeds_data=los_speeds_data
        )
        yeti_format_los_speeds_data = loader.load_data()
        vehicle_category_in_yeti_format_data = yeti_format_los_speeds_data.iloc[0]["VehicleCategory"]

        self.assertEqual("VehicleCategory.COACH", vehicle_category_in_yeti_format_data)

    def test_vehicle_category_urban_bus(self):

        los_speeds_data = pd.DataFrame.from_dict({
            "VehCat": ["urban bus"],
            "TrafficSituation": ["URB/MW-City/100/Freeflow"],
            "Speed_kmh": [20]
        })
        loader = LosSpeedsDataLoader(
            link_data=self.link_data,
            los_speeds_data=los_speeds_data
        )
        yeti_format_los_speeds_data = loader.load_data()
        vehicle_category_in_yeti_format_data = yeti_format_los_speeds_data.iloc[0]["VehicleCategory"]

        self.assertEqual("VehicleCategory.UBUS", vehicle_category_in_yeti_format_data)

    def test_vehicle_category_motorcycle(self):

        los_speeds_data = pd.DataFrame.from_dict({
            "VehCat": ["motorcycle"],
            "TrafficSituation": ["URB/MW-City/100/Freeflow"],
            "Speed_kmh": [20]
        })
        loader = LosSpeedsDataLoader(
            link_data=self.link_data,
            los_speeds_data=los_speeds_data
        )
        yeti_format_los_speeds_data = loader.load_data()

        self.assertEqual("VehicleCategory.MC", yeti_format_los_speeds_data.iloc[0]["VehicleCategory"])
        self.assertEqual("VehicleCategory.MOPED", yeti_format_los_speeds_data.iloc[1]["VehicleCategory"])

    def test_vehicle_category_HGV(self):

        los_speeds_data = pd.DataFrame.from_dict({
            "VehCat": ["HGV"],
            "TrafficSituation": ["URB/MW-City/100/Freeflow"],
            "Speed_kmh": [20]
        })
        loader = LosSpeedsDataLoader(
            link_data=self.link_data,
            los_speeds_data=los_speeds_data
        )
        yeti_format_los_speeds_data = loader.load_data()
        vehicle_category_in_yeti_format_data = yeti_format_los_speeds_data.iloc[0]["VehicleCategory"]

        self.assertEqual("VehicleCategory.HDV", vehicle_category_in_yeti_format_data)

if __name__ == "__main__":
    main()
