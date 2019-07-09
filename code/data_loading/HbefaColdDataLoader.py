import pandas as pd
from typing import Tuple

from code.constants.enumerations import PollutantType
from code.constants.column_names import *
from code.data_loading.DataLoader import DataLoader
from code.data_loading.TrafficDataLoader import TrafficDataLoader


class HbefaColdDataLoader(DataLoader):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def load_input_data(self, use_nh3_ef: bool):

        link_data = pd.read_csv(self.filenames_dict["link_data_file"])
        fleet_comp_data = pd.read_csv(self.filenames_dict["fleet_comp_file"])
        cold_starts_data = pd.read_csv(self.filenames_dict["cold_starts_file"])
        emission_factor_data = pd.read_csv(self.filenames_dict["emission_factor_file"])

        return emission_factor_data, fleet_comp_data, None, link_data, cold_starts_data, None, None, None

    def load_los_speeds_data(self, link_data: pd.DataFrame, los_speeds_data: pd.DataFrame):

        return None

    def load_emission_factor_data(self,
                                  use_nh3_ef: bool,
                                  fleet_comp_data: pd.DataFrame,
                                  vehicle_mapping_data: pd.DataFrame,
                                  ef_data: pd.DataFrame,
                                  nh3_ef_data: pd.DataFrame,
                                  nh3_mapping_data: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:

        unified_ef_data = ef_data.rename(columns={"VehName": "VehicleName"})

        # convert pollutants to PollutantType objects
        unified_ef_data["Pollutant"] = unified_ef_data["Pollutant"].apply(
            lambda poll: PollutantType.from_val(poll))

        return unified_ef_data, pd.DataFrame()

    def load_traffic_data(self, fleet_comp_data, link_data, traffic_data):
        # Note that traffic_data contains the cold starts data.

        # Make sure that traffic_data fits the format required by the TrafficDataLoader.
        traffic_data_for_traffic_data_loader = traffic_data
        traffic_data_for_traffic_data_loader[TRAFFIC_COUNT_LOS_1_PERC] = 0
        traffic_data_for_traffic_data_loader[TRAFFIC_COUNT_LOS_2_PERC] = 0
        traffic_data_for_traffic_data_loader[TRAFFIC_COUNT_LOS_3_PERC] = 0
        traffic_data_for_traffic_data_loader[TRAFFIC_COUNT_LOS_4_PERC] = 0
        traffic_data_for_traffic_data_loader = traffic_data_for_traffic_data_loader.rename(
            columns={"NumberOfStarts": TRAFFIC_COUNT_VEH_COUNT})

        # Convert to unified_data format (for traffic data)
        unified_traffic_data = TrafficDataLoader(
            fleet_comp_data=fleet_comp_data,
            traffic_count_data=traffic_data_for_traffic_data_loader,
            link_data=link_data
        ).load_data()

        # Convert the unified traffic data to unified cold starts data
        unified_cold_starts_data = unified_traffic_data.drop(["LOS1Percentage", "LOS2Percentage", "LOS3Percentage", "LOS4Percentage"], axis=1)

        return unified_cold_starts_data