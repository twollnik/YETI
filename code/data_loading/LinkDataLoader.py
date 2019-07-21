from code.constants.column_names import *
from code.constants.enumerations import AreaType, RoadType


class LinkDataLoader:

    def __init__(self, **kwargs):
        """ Initialize a LinkDataLoader instance.

        You need to pass this keyword argument:
        - link_data : a pd.DataFrame with street link data. It needs to contain the
                      columns specified in 'column_names.py' under '# link data'.
                      The link length needs to be in meters.
        """

        self.link_data = kwargs['link_data']

    def load_data(self):
        """ Get link data.

        This method uses the dataframe that was previously passed to the constructor method.

        Note that the link length needs to be in meters in the berlin_format data and will be
        in kilometers in the output data.

        :return: link_data : a pd.DataFrame
        """

        link_data_new = self.link_data[
            [SHAPE_LINK_ID, SHAPE_LENGTH, SHAPE_AREA_CAT, SHAPE_ROAD_CAT, SHAPE_MAX_SPEED]]
        if SHAPE_SPEED_OPTIONAL in self.link_data.columns:
            link_data_new.loc[:, "Speed"] = self.link_data[SHAPE_SPEED_OPTIONAL]

        link_data_new.loc[:, SHAPE_LENGTH] = link_data_new[SHAPE_LENGTH] / 1000  # convert m to km

        link_data_new = link_data_new.rename(
            columns={SHAPE_LINK_ID: "LinkID", SHAPE_LENGTH: "Length",
                     SHAPE_ROAD_CAT: "RoadType", SHAPE_AREA_CAT: "AreaType",
                     SHAPE_MAX_SPEED: "MaxSpeed"})

        # convert to enumeration objects
        link_data_new.loc[:, "AreaType"] = link_data_new["AreaType"].apply(lambda val: AreaType.from_val(val))
        link_data_new.loc[:, "RoadType"] = link_data_new["RoadType"].apply(lambda val: RoadType.from_val(val))

        return link_data_new
