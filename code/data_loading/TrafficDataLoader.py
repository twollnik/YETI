import numpy as np
import pandas as pd

from code.constants.column_names import *
from code.constants.enumerations import Dir, DayType
from code.constants.mappings import FLEET_COMP_VEH_CAT_TO_LINK_DATA_TRAFFIC_PERC_MAPPING

# suppress pandas SettingWithCopyWarning
pd.options.mode.chained_assignment = None


class TrafficDataLoader:
    """
    This class provides functionality to calculate yeti_format traffic data from berlin_format traffic data.
    """

    def __init__(self, **kwargs):
        """ Initialize a TrafficDataLoader instance.

        You need to pass the following keyword arguments:
        - fleet_comp_data : a pd.DataFrame with the fleet composition data. It needs
                            to contain the columns specified in 'column_names.py' under
                            '# fleet comp data'.
        - link_data : a pd.DataFrame with street link data. It needs to contain the
                      columns specified in 'column_names.py' under '# link data'.
        - traffic_count_data : a pd.DataFrame with traffic count data. It needs to contain
                               all columns specifie in 'column_names.py' under '# traffic count data'.
        """

        self.fleet_comp_data = kwargs['fleet_comp_data']
        self.link_data = kwargs['link_data'][[SHAPE_LINK_ID, SHAPE_PC_PERC, SHAPE_LCV_PERC, SHAPE_HDV_PERC,
                                             SHAPE_UBUS_PERC, SHAPE_COACH_PERC, SHAPE_MC_PERC]]
        self.traffic_count_data = kwargs['traffic_count_data']

    def load_data(self):
        """ Get traffic data.

        This method uses the dataframes that were previously passed to the constructor method.

        :return: traffic_data : a pd.DataFrame
        """

        traffic_and_shape_data = pd.merge(self.traffic_count_data, self.link_data,
                                          left_on=[TRAFFIC_COUNT_LINK_ID], right_on=[SHAPE_LINK_ID])

        traffic_data_for_vehicle_categories = {}

        for vehicle_cat in FLEET_COMP_VEH_CAT_LEVELS:
            perc_column = FLEET_COMP_VEH_CAT_TO_LINK_DATA_TRAFFIC_PERC_MAPPING[vehicle_cat]
            traffic_for_veh_cat = traffic_and_shape_data[TRAFFIC_COUNT_VEH_COUNT] * traffic_and_shape_data[perc_column]
            traffic_data_for_vehicle_categories[vehicle_cat] = traffic_for_veh_cat

        traffic_data = traffic_and_shape_data[[SHAPE_LINK_ID, TRAFFIC_COUNT_DIR,
                                               TRAFFIC_COUNT_DAY_TYPE, TRAFFIC_COUNT_HOUR]]

        for i, row in enumerate(self.fleet_comp_data.itertuples()):
            veh_name = row.__getattribute__(FLEET_COMP_VEH_NAME)
            veh_cat = row.__getattribute__(FLEET_COMP_VEH_CAT)
            veh_perc = row.__getattribute__(FLEET_COMP_VEH_PERC)
            traffic_data[veh_name] = np.around(veh_perc * traffic_data_for_vehicle_categories[veh_cat], decimals=5)

        traffic_data[["LOS1Percentage", "LOS2Percentage", "LOS3Percentage", "LOS4Percentage"]] = \
            traffic_and_shape_data[[TRAFFIC_COUNT_LOS_1_PERC, TRAFFIC_COUNT_LOS_2_PERC,
                                    TRAFFIC_COUNT_LOS_3_PERC, TRAFFIC_COUNT_LOS_4_PERC]]

        if not {"LinkID", "Dir", "DayType", "Hour"}.issubset(traffic_data.columns):
            traffic_data = traffic_data.rename(columns={
                SHAPE_LINK_ID: "LinkID",
                TRAFFIC_COUNT_DIR: "Dir",
                TRAFFIC_COUNT_DAY_TYPE: "DayType",
                TRAFFIC_COUNT_HOUR: "Hour"
            })

        traffic_data["Dir"] = traffic_data["Dir"].apply(lambda x: Dir.from_val(x))
        traffic_data["DayType"] = traffic_data["DayType"].apply(lambda x: DayType.from_val(x))

        return traffic_data
