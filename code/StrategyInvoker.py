import logging
import os
from datetime import datetime

import pandas as pd


class StrategyInvoker:

    def __init__(self, **kwargs):
        """
        :param kwargs:
            - link_data
            - vehicle_data
            - traffic_data
            - emission_factor_data
            - los_speeds_data (optional depending on strategy)
            - emission_calculation_function
            - pollutant
            - links_to_use (optional)
        """

        self.link_data = None
        self.vehicle_data = None
        self.traffic_data = None
        self.emission_calculation_function = None
        self.pollutant = None
        self.link_list = None

        self.output_file = None
        self.use_header = True

        self.vehicle_dict = None
        self.traffic_and_link_data = None

        self.strategy = None
        self.emissions_store = []

    def calculate_and_save_emissions(self, emissions_output_folder, save_interval_in_rows: int = 10000, **kwargs):

        logging.debug("Initializing data.")
        self.initialize(emissions_output_folder, **kwargs)

        logging.debug("Calculating emissions.")
        for i, row in self.traffic_and_link_data_rows():

            self.display_progress(i)

            try:
                emissions = self.strategy.calculate_emissions(row, self.vehicle_dict, **kwargs)
                emissions_row = self.associate_emissions_with_time_and_location_info(emissions, row)
                self.add_row_to_emissions_store(emissions_row)

            except Exception as e:
                self.handle_error_in_emission_calculation(e, row)

            if self.it_is_time_to_save_emissions(i, save_interval_in_rows):
                self.save_emissions()

        self.save_emissions()

    def initialize(self, emissions_output_folder, **kwargs):

        self.initialize_strategy(**kwargs)
        self.initialize_attributes(emissions_output_folder, **kwargs)
        self.initialize_traffic_and_link_data()
        self.initialize_vehicle_dict()

    def initialize_strategy(self, **kwargs):

        self.strategy = kwargs["Strategy"]()

    def initialize_attributes(self, emissions_output_folder, **kwargs):

        self.link_data = kwargs.get("link_data")
        self.vehicle_data = kwargs.get("vehicle_data")
        self.traffic_data = kwargs.get("traffic_data")
        self.emission_calculation_function = kwargs.get("emission_calculation_function")
        self.pollutant = kwargs.get("pollutant")
        self.link_list = kwargs.get("links_to_use")

        self.output_file = self.get_output_file_name(emissions_output_folder)

        self.vehicle_dict = None
        self.traffic_and_link_data = None

    def initialize_traffic_and_link_data(self):

        data = pd.merge(self.link_data, self.traffic_data, on="LinkID")
        if self.link_list is not None and len(self.link_list) > 0:
            data = data[data["LinkID"].isin(self.link_list)]
        self.traffic_and_link_data = data

        self.traffic_data = None  # save memory by garbage collecting traffic_data early

    def initialize_vehicle_dict(self):

        self.vehicle_dict = {
            t.VehicleName: str(t.VehicleCategory)
            for t in self.vehicle_data.itertuples()
        }

    def get_output_file_name(self, output_folder):

        output_file = f"{output_folder}/emissions.csv"
        if not os.path.isdir(output_folder):
            os.mkdir(output_folder)
        return output_file

    def traffic_and_link_data_rows(self):

        for i, row in self.traffic_and_link_data.iterrows():
            row = row.to_dict()
            yield i, row

    def add_row_to_emissions_store(self, row):

        self.emissions_store.append(row)

    def it_is_time_to_save_emissions(self, row_index, save_interval_in_rows):

        return row_index % save_interval_in_rows == 0

    def save_emissions(self):

        if self.there_are_emissions_to_save():

            if self.should_save_multiple_files():
                self.save_emission_dicts_to_files()

            else:
                emission_data = pd.DataFrame(self.emissions_store)
                self.save_dataframe_to_file(emission_data, self.output_file)

            self.emissions_store = []
            self.use_header = False  # only output the header once

    def save_emission_dicts_to_files(self):

        names = self.get_emission_dicts_names()
        for name in names:
            emission_data = pd.DataFrame([
                {
                    **item[name],
                    "LinkID": item["LinkID"],
                    "DayType": item["DayType"],
                    "Dir": item["Dir"],
                    "Hour": item["Hour"]
                }
                for item in self.emissions_store
            ])
            folder, _, file = self.output_file.rpartition("/")
            output_file = f"{folder}/{name}_{file}"
            self.save_dataframe_to_file(emission_data, output_file)

    def there_are_emissions_to_save(self):

        return len(self.emissions_store) > 0

    def get_emission_dicts_names(self):

        names = [
            key for key in self.emissions_store[0].keys()
            if isinstance(self.emissions_store[0][key], dict)
        ]
        return names

    def should_save_multiple_files(self):

        return any(isinstance(item, dict) for item in self.emissions_store[0].values())

    def save_dataframe_to_file(self, data, file):

        with open(file, "a") as fp:
            data.to_csv(fp, header=self.use_header, index_label=False, index=False)

    def associate_emissions_with_time_and_location_info(self, emissions, row):

        return {
            **{"LinkID": row["LinkID"], "DayType": row["DayType"], "Hour": row["Hour"], "Dir": row["Dir"]},
            **emissions
        }

    def handle_error_in_emission_calculation(self, e, row):

        logging.warning(
            f"An Error occured when processing the traffic data row "
            f"(LinkID: {row['LinkID']}, Dir: {row['Dir']}, DayType: {row['DayType']}, Hour: {row['Hour']}\n"
        )
        logging.exception(e)

    def display_progress(self, current_row):

        perc_done = current_row / len(self.traffic_and_link_data) * 100
        print("%.1f percent done" % perc_done, end='\r')
