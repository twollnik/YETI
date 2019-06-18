import pandas as pd

from code.constants.column_names import *
from code.constants.enumerations import VehicleCategory
from code.constants.mappings import FLEET_COMP_VEH_CAT_TO_UNIFIED_VEH_CAT_MAPPING


class VehicleDataLoader:

    def __init__(self, **kwargs):
        """ Initialize a VehicleDataLoader instance.

        You need to pass this keyword argument:
        - fleet_comp_data : a pd.DataFrame with the fleet composition data. It needs
                            to contain the columns specified in 'column_names.py' under
                            '# fleet comp data'.
        """

        self.fleet_comp_data = kwargs["fleet_comp_data"]

    def load_data(self):
        """ Get vehicle data.

        This method uses the dataframe that was previously passed to the constructor method.

        :return: vehicle_data : a pd.DataFrame conaining vehicle data in unified_data format
        """

        vehicle_data = self.fleet_comp_data[[FLEET_COMP_VEH_NAME, FLEET_COMP_VEH_CAT, FLEET_COMP_NUM_AXLES]]
        vehicle_data = vehicle_data.rename(index=str, columns={FLEET_COMP_VEH_NAME: "VehicleName",
                                                               FLEET_COMP_VEH_CAT: "VehicleCategory",
                                                               FLEET_COMP_NUM_AXLES: "NumberOfAxles"})

        def transform_vehicle_category(veh_data: pd.Series) -> VehicleCategory:
            veh_cat = str(veh_data["VehicleCategory"])
            return FLEET_COMP_VEH_CAT_TO_UNIFIED_VEH_CAT_MAPPING[veh_cat]

        vehicle_data["VehicleCategory"] = vehicle_data.apply(transform_vehicle_category, axis=1)

        return vehicle_data
