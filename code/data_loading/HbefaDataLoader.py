from typing import Tuple

import logging
import pandas as pd

from code.data_loading.DataLoader import DataLoader
from code.data_loading.EmissionFactorDataLoader import HbefaEmissionFactorDataLoader
from code.data_loading.FileDataLoader import HbefaFileDataLoader


class HbefaDataLoader(DataLoader):
    """ Use this DataLoader to load unified data from input data with hbefa emission factors.

    Different concrete data loaders will be used than in DataLoader and less input files are required.
    """

    def __init__(self, **kwargs):
        """Initialize a HbefaDataLoader instance

        You may pass the following keyword arguments to specify file locations. If you don't pass
        some of these arguments, the default locations as specified in 'default_filenames.py' will be used.
        Possible keyword arguments:
        - emission_factor_file
        - fleet_comp_file
        - link_data_file
        - traffic_data_file
        """

        super().__init__(**kwargs)

    def load_input_data(self, use_nh3_ef: bool):  # -> 8 - tuple of pd.DataFrames

        if use_nh3_ef is True:
            logging.warning("use_nh3_tier2_ef set to False for Hbefa data loading. (You passed True)")
        return HbefaFileDataLoader(**self.filenames_dict).load_data(use_nh3_ef=False)

    def load_emission_factor_data(self,
                                  use_nh3_ef,
                                  fleet_comp_data,
                                  vehicle_mapping_data,
                                  ef_data,
                                  nh3_ef_data,
                                  nh3_mapping_data) -> Tuple[pd.DataFrame, pd.DataFrame]:

        return HbefaEmissionFactorDataLoader(ef_data=ef_data).load_data()

    def load_los_speeds_data(self, link_data: pd.DataFrame, los_speeds_data: pd.DataFrame):

        return None