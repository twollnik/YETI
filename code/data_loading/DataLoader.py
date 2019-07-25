from typing import Tuple

import pandas as pd

from code.constants.column_names import *
from code.data_loading.EmissionFactorDataLoader import EmissionFactorDataLoader
from code.data_loading.FileDataLoader import FileDataLoader
from code.data_loading.LinkDataLoader import LinkDataLoader
from code.data_loading.LosSpeedsDataLoader import LosSpeedsDataLoader
from code.data_loading.TrafficDataLoader import TrafficDataLoader
from code.data_loading.VehicleDataLoader import VehicleDataLoader


class DataLoader:
    """ Load and transform input data in berlin_format.

    This class implements the high-level algorithm to load and transform the data,
    so that it fits the yeti_format. DataLoader relies on other
    data loaders to implement the concrete logic (e.g. loading the datasets
    from file and converting them to the right format).
    """

    def __init__(self, **kwargs):
        """ Initialize a DataLoader instance

        You may pass the following keyword arguments to specify file locations. If you don't pass
        some of these arguments, the default locations as specified in 'default_filenames.py' will be used.
        Possible keyword arguments:
        - emission_factor_file
        - fleet_comp_file
        - link_data_file
        - traffic_data_file
        - los_speeds_file
        - vehicle_mapping_file
        - nh3_ef_file
        - nh3_mapping_file
        """

        self.filenames_dict = kwargs

    def load_data(self, use_nh3_ef: bool = True, **kwargs):
        """ Load and transform input data in berlin_format.

        This method will delegate responsibilities to other classes to perform all
        relevant operations to convert the data in berlin_format to data in yeti_format.
        It will use the file locations that were passed to the constructor ('__init__').

        :return: link_data, vehicle_data, traffic_data, los_speeds_data, emission_factor_data and missing_ef_data
                 in yeti_format as pd.DataFrames
        """

        print("[data_loading] 1/7: Loading data from file.")
        (emission_factor_data, fleet_comp_data, los_speeds_data, link_data, traffic_count_data,
         vehicle_name_emissions_category_mapping_data, nh3_ef_data, nh3_mapping_data) = \
            self.load_berlin_format_data(use_nh3_ef)

        print("[data_loading] 2/7: Filtering unmatched links.")
        traffic_count_data, unused_links = self.filter_unused_links(traffic_count_data, link_data)

        print(f"\tNumber of links in traffic_count_data with no corresponding link in shape_data: {len(unused_links)}")

        print("[data_loading] 3/7: Building link_and_traffic_data.")
        yeti_format_link_data = self.load_link_data(link_data)

        print("[data_loading] 4/7: Building vehicle_data.")
        vehicle_data = self.load_vehicle_data(fleet_comp_data=fleet_comp_data)

        print("[data_loading] 5/7: Building emission_factor_data.")
        ef_data, missing_ef_data = self.load_emission_factor_data(
            use_nh3_ef,
            fleet_comp_data=fleet_comp_data,
            vehicle_mapping_data=vehicle_name_emissions_category_mapping_data,
            ef_data=emission_factor_data,
            nh3_ef_data=nh3_ef_data,
            nh3_mapping_data=nh3_mapping_data
        )

        print("[data_loading] 6/7: Building los_speeds_data.")
        los_speeds_data = self.load_los_speeds_data(link_data, los_speeds_data)

        print("[data_loading] 7/7: Building traffic_data.")
        traffic_data = self.load_traffic_data(fleet_comp_data, link_data, traffic_count_data)

        print("[data_loading] Done.")
        return yeti_format_link_data, vehicle_data, traffic_data, los_speeds_data, ef_data, missing_ef_data

    def filter_unused_links(self, traffic_count_data, shape_data):
        """ From traffic_count_data remove all rows with a LinkID that is not in shape_data.

        :return: updated_traffic_count_data, unused_links
        """

        unused_links = traffic_count_data[~traffic_count_data[TRAFFIC_COUNT_LINK_ID].isin(
            shape_data[SHAPE_LINK_ID].tolist())][TRAFFIC_COUNT_LINK_ID]
        unique_unused_links = unused_links.unique().tolist()

        link_ids = shape_data[SHAPE_LINK_ID].tolist()
        validated_traffic_count_data = traffic_count_data[
            traffic_count_data[TRAFFIC_COUNT_LINK_ID].isin(link_ids)]

        return validated_traffic_count_data, unique_unused_links

    def load_traffic_data(self, fleet_comp_data, link_data, traffic_data):

        return TrafficDataLoader(
            fleet_comp_data=fleet_comp_data, link_data=link_data, traffic_count_data=traffic_data
        ).load_data()

    def load_berlin_format_data(self, use_nh3_ef: bool):  # -> 8 - tuple of pd.DataFrames

        return FileDataLoader(**self.filenames_dict).load_data(use_nh3_ef, use_hbefa_ef=False)

    def load_link_data(self, link_data: pd.DataFrame) -> pd.DataFrame:

        return LinkDataLoader(link_data=link_data).load_data()

    def load_vehicle_data(self, fleet_comp_data: pd.DataFrame) -> pd.DataFrame:

        return VehicleDataLoader(fleet_comp_data=fleet_comp_data).load_data()

    def load_emission_factor_data(self,
                                  use_nh3_ef: bool,
                                  fleet_comp_data: pd.DataFrame,
                                  vehicle_mapping_data: pd.DataFrame,
                                  ef_data: pd.DataFrame,
                                  nh3_ef_data: pd.DataFrame,
                                  nh3_mapping_data: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:

        return EmissionFactorDataLoader(
            use_nh3_tier2_ef=use_nh3_ef,
            fleet_comp_data=fleet_comp_data,
            vehicle_mapping_data=vehicle_mapping_data,
            ef_data=ef_data,
            nh3_ef_data=nh3_ef_data,
            nh3_mapping_data=nh3_mapping_data
        ).load_data()

    def load_los_speeds_data(self, link_data: pd.DataFrame, los_speeds_data: pd.DataFrame):

        return LosSpeedsDataLoader(link_data=link_data, los_speeds_data=los_speeds_data).load_data()
