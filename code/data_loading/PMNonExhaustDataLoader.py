from typing import Tuple

import pandas as pd

from code.data_loading.DataLoader import DataLoader
from code.data_loading.FileDataLoader import PMNonExhaustFileDataLoader


class PMNonExhaustDataLoader(DataLoader):

    def load_berlin_format_data(self, use_nh3_ef: bool):

        return PMNonExhaustFileDataLoader(**self.filenames_dict).load_data(use_nh3_ef=False)

    def load_emission_factor_data(self,
                                  use_nh3_ef: bool,
                                  fleet_comp_data: pd.DataFrame,
                                  vehicle_mapping_data: pd.DataFrame,
                                  ef_data: pd.DataFrame,
                                  nh3_ef_data: pd.DataFrame,
                                  nh3_mapping_data: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:

        return (None, None)