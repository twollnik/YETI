""" This module contains helper functions used by the DataLoaders. """
import pandas as pd

from code.constants.enumerations import *


def convert_dir_and_day_type(df: pd.DataFrame,
                             dir_col: str = 'Dir',
                             day_type_col: str = 'DayType') -> pd.DataFrame:
    """ Convert strings to enumeration instances.

    Convert the strings in the columns dir_col and day_type_col of the given
    dataframe to instances of the Dir or DayType enumeration classes.
    """

    df.loc[:, dir_col] = df[dir_col].apply(lambda x: Dir.from_val(x))
    df.loc[:, day_type_col] = df[day_type_col].apply(lambda x: DayType.from_val(x))
    return df
