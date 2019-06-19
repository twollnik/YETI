from collections import defaultdict
from itertools import chain, product

import pandas as pd

from code.constants.mappings import *
from code.constants.column_names import *


class LosSpeedsDataLoader:

    def __init__(self, **kwargs):
        """ Initialize a LosSpeedsDataLoader instance.

        You need to pass these keyword arguments:
        - link_data : a pd.DataFrame with street link data. It needs to contain the
                      columns specified in 'column_names.py' under '# link data'.
        - los_speeds_data : a pd.DataFrame with los speeds information for different
                            road types and vehicle categories. It needs to contain the
                            columns specified in 'column_names.py' under '# los speeds data'.
        """

        self.link_data = kwargs['link_data']
        self.los_speeds_data = kwargs['los_speeds_data']

    def load_data(self):
        """ Get los speeds data.

        This method uses the dataframes that were previously passed to the constructor method.

        :return: los_speeds_data : a pd.DataFrame with los speed information for all links in link_data.
        """

        mapping_df = self.construct_mapping_between_link_and_los_speeds_data()
        merged_link_and_los_speeds_data = self.merge_data_using_mapping(mapping_df)
        los_speeds_in_unified_data_format = self.reformat_merged_data_to_fit_unified_data_format(
            merged_link_and_los_speeds_data)
        los_speeds_for_mopeds = self.get_speeds_for_vehicle_category_moped(los_speeds_in_unified_data_format)

        return self.construct_dataframe(los_speeds_in_unified_data_format, los_speeds_for_mopeds)

    def construct_mapping_between_link_and_los_speeds_data(self):

        self.drop_speed_col_from_shape_data_if_possible()
        unique_link_situations = self.link_data[[SHAPE_AREA_CAT, SHAPE_ROAD_CAT, SHAPE_MAX_SPEED]].drop_duplicates()

        mapping_df_parts = []
        for _, row in unique_link_situations.iterrows():
            for los_type in range(1, 5):

                mapping_df_parts.append({
                    "AreaCat": row[SHAPE_AREA_CAT],
                    "RoadCat": row[SHAPE_ROAD_CAT],
                    "MaxSpeed_kmh": row[SHAPE_MAX_SPEED],
                    "TS": self.get_ts_for_link_situation_and_los_type(row, los_type)
                })

        return pd.DataFrame(mapping_df_parts)

    def drop_speed_col_from_shape_data_if_possible(self):

        if SHAPE_SPEED_OPTIONAL in self.link_data.columns:
            self.link_data = self.link_data.drop(SHAPE_SPEED_OPTIONAL, axis=1)

    def get_ts_for_link_situation_and_los_type(self, row: pd.Series, los_type: int) -> str:

        road_type = HEBEFA_ROAD_CAT_TO_LOS_SPEEDS_DATA_ROAD_CAT_MAPPING[
            str(row[SHAPE_ROAD_CAT])]
        traffic_situation = self.get_traffic_situation(road_type, row[SHAPE_MAX_SPEED], row[SHAPE_AREA_CAT])

        if los_type == 1:
            return f"{traffic_situation}/Freeflow"
        if los_type == 2:
            return f"{traffic_situation}/Heavy"
        if los_type == 3:
            return f"{traffic_situation}/Satur."
        if los_type == 4:
            return f"{traffic_situation}/St+Go"

    def merge_data_using_mapping(self, mapping):

        link_with_ts = pd.merge(self.link_data, mapping, left_on=[SHAPE_AREA_CAT, SHAPE_ROAD_CAT, SHAPE_MAX_SPEED],
                                right_on=["AreaCat", "RoadCat", "MaxSpeed_kmh"])

        link_and_los_speeds_merged = pd.merge(
            link_with_ts, self.los_speeds_data, left_on="TS", right_on=LOS_SPEED_TRAFFIC_SITUATION)

        link_and_los_speeds_merged = link_and_los_speeds_merged[
            [SHAPE_LINK_ID, LOS_SPEED_VEH_CAT, LOS_SPEED_TRAFFIC_SITUATION, LOS_SPEED_SPEED]]

        link_and_los_speeds_merged["VehCat"] = link_and_los_speeds_merged["VehCat"].apply(
            lambda veh_cat: VEH_CAT_MAPPING[veh_cat])

        return link_and_los_speeds_merged

    def get_traffic_situation(self, road_type: str, max_speed: str, area_type: str) -> str:
        """ Format link categorization information as string.

        Link categorization information includes road type, area type
        and max speed for a particular link.

        If area_type is none, type urban will be assumed.
        """

        if area_type is None or str(area_type) == "1":
            return f"URB/{road_type}/{max_speed}"
        else:
            return f"RUR/{road_type}/{max_speed}"

    def reformat_merged_data_to_fit_unified_data_format(self, merged_link_and_los_speeds_data):

        df_parts = defaultdict(dict)
        for i, row in merged_link_and_los_speeds_data.iterrows():
            row = row.to_dict()
            los_string = row["TrafficSituation"].split("/")[-1]
            if los_string == "Freeflow":
                los_type = 1
            elif los_string == "Heavy":
                los_type = 2
            elif los_string == "Satur.":
                los_type = 3
            elif los_string == "St+Go":
                los_type = 4
            df_parts[(row["LinkID"], row["VehCat"])].update({
                f"LOS{los_type}Speed": row["Speed_kmh"],
                "LinkID": row["LinkID"],
                "VehicleCategory": row["VehCat"]
            })

        return df_parts

    def get_speeds_for_vehicle_category_moped(self, df_parts):

        moped_speeds = defaultdict(dict)
        for val in df_parts.values():
            if val["VehicleCategory"] == VehicleCategory.MC:
                val["VehicleCategory"] = VehicleCategory.Moped
                moped_speeds[(val["LinkID"], val["VehicleCategory"])] = val

        return moped_speeds

    def construct_dataframe(self, los_speeds_in_unified_data_format, los_speeds_for_mopeds):

        all_rows_for_los_speeds_dataframe = chain(
            los_speeds_in_unified_data_format.values(), los_speeds_for_mopeds.values())
        list_of_rows_for_los_speeds_dataframe = [val for val in all_rows_for_los_speeds_dataframe]
        los_speeds_dataframe = pd.DataFrame(list_of_rows_for_los_speeds_dataframe)

        return los_speeds_dataframe
