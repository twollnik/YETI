from typing import List

import csv
import logging
import os
import pandas as pd

import code.constants.column_names

#
# ---- main interface ----
# When interacting with this module, use only these two functions.
#

def validate_dataset(file: str, shorthand: str, data: pd.DataFrame = None) -> bool:
    """ Validate the given dataset.

    This function will check that
    - the seperator is ','
    - all necessary columns are present in the data
    - the percentage columns contain only floats in the range 0 to 1
    - the categorical columns contain the expected set of values

    :param file: Path to the csv file that is being checked.
    :param shorthand: The shorthand used to abbreviate filenames in 'code/constants/column_names.py'.
                      For example the shorthand for the fleet composition data is 'FLEET_COMP'.
    :param data: OPTIONAL. A dataframe containing the data from the given file. If this parameter is given the data
                 won't be loaded (meaning the function will run faster).
    :return: False if any error was found during validation. Otherwise return True.
    """

    file = os.path.abspath(file)

    logging.debug(f"Validating the file {file}")

    # check file format (header exists and seperator is ',')
    is_comma_separated = check_separator_is_comma(file)
    if is_comma_separated is False:
        return False

    if data is None:
        data = pd.read_csv(file)

    # check that the data contains all the non-optional columns
    expected_columns = [
        val for key, val in code.constants.column_names.__dict__.items()
        if key.startswith(shorthand) and not key.endswith("OPTIONAL") and isinstance(val, str)
    ]
    if len(expected_columns) == 0:
        logging.warning(f"Please verify that you have passed the correct shorthand for the file {file}. You passed: {shorthand}")
    contains_all_columns = check_column_names(file, data, expected_columns)

    # check that the percentage columns contain only floats in the range 0 to 1
    percentage_columns_expected = [
        val for key, val in code.constants.column_names.__dict__.items()
        if key.startswith(shorthand) and key.endswith("PERC") and val in data.columns
    ]
    perc_columns_are_valid = check_are_perc_columns(file, data, percentage_columns_expected)

    # check that the categorical columns contain the expected set of values
    categorical_columns_expected = [
        (code.constants.column_names.__dict__[key.replace("_LEVELS", "")], val)
        for key, val in code.constants.column_names.__dict__.items()
        if key.startswith(shorthand) and key.endswith("_LEVELS") and isinstance(val, list)
           and code.constants.column_names.__dict__[key.replace("_LEVELS", "")] in data.columns
    ]
    categories_are_correct = True
    for column_name, levels in categorical_columns_expected:
        col_has_correct_categories = check_categories_are_correct(file, data, column_name, levels)
        categories_are_correct = False if col_has_correct_categories is False else categories_are_correct

    return all([contains_all_columns, perc_columns_are_valid, categories_are_correct])


def check_mapping(from_file: str, to_file: str,
                  from_cols: List, to_cols: List,
                  from_df: pd.DataFrame = None,
                  to_df: pd.DataFrame = None) -> bool:
    """ Check the mapping between from_file and to_file. """

    if from_df is None:
        from_df = pd.read_csv(from_file)
    if to_df is None:
        to_df = pd.read_csv(to_file)

    mapped_df = pd.merge(
        from_df,
        to_df,
        left_on=from_cols,
        right_on=to_cols
    )

    mapped_df_from_cols_values = list(mapped_df[from_cols].drop_duplicates().itertuples(index=False))
    from_df_from_cols_values = list(from_df[from_cols].drop_duplicates().itertuples(index=False))

    mapping_is_correct = all([val in mapped_df_from_cols_values for val in from_df_from_cols_values])

    if mapping_is_correct is False:
        logging.warning(f"The mapping between {from_file} and {to_file} seems to be incorrect. Make sure all the values in "
                        f"the columns [{', '.join(from_cols)}] in {from_file} are present in the columns "
                        f"[{', '.join(to_cols)}] in {to_file}.")

    return mapping_is_correct


def check_separator_is_comma(file: str) -> bool:
    with open(file) as csvfile:
        sample = csvfile.read(2048)
    try:
        delimiter = csv.Sniffer().sniff(sample).delimiter
    except csv.Error as e:
        if "delimiter" in str(e):
            logging.warning(f"Could not determine the delimiter for file {file} automatically. "
                            f"Please manually check that you are using the delimiter ','.")
            return True, ""
        else:
            raise e

    if delimiter != ',':
        logging.warning(f"{file} does not have the correct separator. Use ',' instead of '{delimiter}'. "
                        f"Also make sure to use '.' as decimal point (the decimal point is not checked automatically).")
        return False
    return True


def check_column_names(file: str, df: pd.DataFrame, colnames_expected: List[str]) -> bool:
    is_equal = True
    colnames_actual = df.columns
    for colname in colnames_expected:
        if colname not in colnames_actual:
            logging.warning(f"{file} is missing the column {colname}")
            is_equal = False
    return is_equal


def check_are_perc_columns(file: str, df: pd.DataFrame, column_names: List[str]) -> bool:
    are_valid = [
        check_is_perc_column(file, df, column_name) for column_name in column_names
    ]
    return all(are_valid)


def check_is_perc_column(file: str, df: pd.DataFrame, column_name: str) -> bool:
    try:
        if not all([0 <= float(i) <= 1 for i in df[column_name].values]):
            logging.warning(f"{file}: All values in column {column_name} should be between 0 and 1.")
            return False
        return True
    except ValueError as e:
        if 'float' in str(e):
            logging.warning(f"{file}: All values in column {column_name} must have type float.")
            return False
        else:
            raise e


def check_categories_are_correct(file: str, df: pd.DataFrame, column_name: str, expected_categories: List[str]) -> bool:
    actual_categories = [str(x) for x in list(df[column_name].astype("category").cat.categories)]
    unknown_categories = [cat for cat in actual_categories if cat not in expected_categories]
    if len(unknown_categories) > 0:
        logging.warning(f"{file}: The values in {column_name} don't match the expected values.\n"
                        f"\t expected values: {', '.join([str(x) for x in expected_categories])}\n"
                        f"\t actual values: {', '.join([str(x) for x in actual_categories])}")
        return False
    return True


