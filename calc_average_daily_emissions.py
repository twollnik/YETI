"""
This script reads an emissions file and calculates the average daily emissions.

Methodology:
1. Read the given input file
2. Remove the columns "LinkID", "Hour", "Dir" and "DayType"
3. Multiply the emissions for day type MONtoTHU by 4
4. Sum all values
5. Divide the result by 7
"""

import argparse
import pandas as pd


def calc_avg_daily_emissions(input_file: str):

    print(f"Reading emissions from file {input_file}")
    emissions_df = pd.read_csv(
        input_file,
        index_col=0
    )

    # find out which rows correspond to data from Mon, Tue, Wed or Thu.
    weekday_rows = emissions_df["DayType"] == "DayType.MONtoTHU"

    print("Removing non emissions columns.")
    emissions_df = emissions_df.drop(
        ["LinkID", "Hour", "DayType", "Dir"],
        axis=1
    )
    if "Unnamed: 0" in emissions_df.columns:
        emissions_df.drop("Unnamed: 0")

    print("Summing emissions.")
    emissions_df[weekday_rows] *= 4
    total_emissions = emissions_df.sum().sum()

    print("Calculating average daily emissions.")
    average_daily_emissions = total_emissions / 7

    return average_daily_emissions


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input_file", "-i",
        help="Path to the the csv file with the emissions data.",
        dest="input_file",
        type=str)
    args = parser.parse_args()
    input_file = args.input_file

    average_daily_emissions = calc_avg_daily_emissions(input_file)

    print(f"The average daily emissions are {average_daily_emissions} grams. \n"
          f"This is with respect to the data in {input_file}")
