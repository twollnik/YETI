from typing import Dict, Any, List

import pandas as pd

from code.Strategy import Strategy


def df_equal(actual: pd.DataFrame, expected: pd.DataFrame):

    if sorted(actual.columns) != sorted(expected.columns):
        raise AssertionError(f"expected: \n{sorted(expected.columns)}\n"
                             f"actual: \n{sorted(actual.columns)}")

    actual = actual[expected.columns]  # column order should match

    actual = actual.applymap(lambda val: round(float(val), 1) if isinstance(val, int) else val)
    actual = actual.round(3)
    expected = expected.applymap(lambda val: round(float(val), 1) if isinstance(val, int) else val)
    expected = expected.round(3)

    actual = actual.astype(str)
    expected = expected.astype(str)

    actual = actual.applymap(lambda val: "0.0" if val == "0" else val)
    expected = expected.applymap(lambda val: "0.0" if val == "0" else val)

    actual_data = [tuple(x) for x in actual.values]
    expected_data = [tuple(x) for x in expected.values]

    if sorted(actual_data) == sorted(expected_data):
        return True

    if actual_data != expected_data:
        print("Differences between the two dataframes:")
        print(f"Columns actual: {', '.join(list(actual.columns))}")
        print(f"Columns expected: {', '.join(list(expected.columns))}")
        for i, (df1_row, df2_row) in enumerate(zip(actual_data, expected_data)):
            if df1_row != df2_row:
                print(f"row: {i+1}")
                print(f"actual: {df1_row}")
                print(f"expected: {df2_row}", end="\n\n")

    return actual_data == expected_data


def mock_load_data_function(**kwargs):

    return kwargs


class MockStrategy(Strategy):

    def calculate_emissions(self,
                            traffic_and_link_data_row: Dict[str, Any],
                            vehicle_dict: Dict[str, str],
                            pollutants: List[str],
                            **kwargs):

        return {"poll": {"vehA": 100}}