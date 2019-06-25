from time import time

import logging
import os

from code.script_helpers.create_info_file import create_info_file
from code.script_helpers.dynamic_import_from import dynamic_import_from
from code.strategy_helpers.helpers import get_timestamp
from code.StrategyInvoker import StrategyInvoker


class Model:

    def __init__(self):

        self.start_time = None
        self.config_file = None
        self.config_dict = None
        self.mode = None

        self.strategy_class = None
        self.unified_data_load_function = None
        self.input_data_load_function = None
        self.validation_function = None

        self.emissions_output_folder = None
        self.unified_data_output_folder = None

        self.n_steps = 6
        self.current_step = 1

    def run(self, config_dict, config_file):

        self.initialize(config_dict, config_file)
        self.log_run_information()

        self.log_step("Initializing output directories.")
        self.create_output_folders_if_necessary()

        self.log_step("Validating the dataset.")
        self.validate_dataset()

        self.log_step("Converting input data to unified data.")
        unified_file_locations = self.load_input_data()

        self.log_step("Loading unified_data.")
        unified_data_dataframes = self.load_unified_data(unified_file_locations)

        self.log_step(f"Calculating emissions for pollutant {self.config_dict['pollutant']}.")
        self.calculate_emissions_with_user_defined_strategy(unified_data_dataframes)

        self.log_step("Creating 'run_info.txt'.")
        self.create_run_info_file()

        self.log_is_done_message()

    def initialize(self, config_dict, config_file):

        self.start_time = time()
        self.config_file = config_file
        self.config_dict = config_dict
        self.mode = self.config_dict["mode"]

        self.strategy_class = self.import_strategy()
        self.unified_data_load_function, self.input_data_load_function, self.validation_function = \
            self.import_user_defined_functions()

    def import_strategy(self):

        path_to_strategy_class = self.config_dict["strategy"]
        strategy_class = dynamic_import_from(path_to_strategy_class)
        return strategy_class

    def import_user_defined_functions(self):

        load_unified_data_function = self.config_dict["load_unified_data_function"]
        load_input_data_function = self.config_dict["load_input_data_function"]
        validation_function = self.config_dict.get("validation_function")

        unified_data_load_function = dynamic_import_from(load_unified_data_function)

        if validation_function is not None:
            validation_function = dynamic_import_from(validation_function)
        else:
            validation_function = None

        if self.mode == "input_data":
            input_data_load_function = dynamic_import_from(load_input_data_function)
        else:
            input_data_load_function = None

        return unified_data_load_function, input_data_load_function, validation_function

    def log_run_information(self):

        pollutant = self.config_dict["pollutant"]
        strategy = self.config_dict["strategy"]
        load_input_data_function = self.config_dict["load_input_data_function"]
        load_unified_data_function = self.config_dict["load_unified_data_function"]
        validation_function = self.config_dict.get("validation_function")

        logging.info(
            f"The config file for this run is: {os.path.abspath(self.config_file)}\n"
            f"pollutant: {pollutant}\n"
            f"mode: {self.mode}\n"
            f"strategy: {strategy}\n"
            f"load_input_data_function: {load_input_data_function}\n"
            f"load_unified_data_function: {load_unified_data_function}\n"
            f"validation_function: {validation_function}\n"
            f"\n"
            f"start time: {get_timestamp(short=True)}"
            f"\n"
        )

    def log_step(self, message):

        logging.info(f"Step {self.current_step} of {self.n_steps}: {message}")
        self.current_step += 1

    def create_output_folders_if_necessary(self):

        emissions_output_folder = self.config_dict["output_folder"]
        unified_output_folder = self.config_dict.get("output_folder_for_unified_data")

        self.emissions_output_folder = self.create_folder_if_it_does_not_exist_already(emissions_output_folder)
        if unified_output_folder is not None:
            self.unified_data_output_folder = self.create_folder_if_it_does_not_exist_already(unified_output_folder)

    def create_folder_if_it_does_not_exist_already(self, folder_name: str) -> str:

        folder_name = folder_name[:-1] if folder_name[-1] in ["/", "\\"] else folder_name
        if os.path.isdir(folder_name) is False:
            os.mkdir(folder_name)
        logging.debug(f"Initialized {os.path.abspath(folder_name)}")
        return folder_name

    def validate_dataset(self):

        if self.validation_function is not None:
            self.validation_function(**self.config_dict)
        else:
            logging.debug("No input data validation function given in config. Validation is skipped.")

    def load_input_data(self):

        if self.mode == 'input_data':
            unified_file_locations = self.input_data_load_function(**self.config_dict)
        else:
            logging.debug("Call load input data function skipped because mode is 'unified_data'.")
            unified_file_locations = self.config_dict
        return unified_file_locations

    def load_unified_data(self, unified_file_locations):

        kwargs = {
            **self.config_dict,
            **unified_file_locations
        }
        unified_data_dataframes = self.unified_data_load_function(**kwargs)
        return unified_data_dataframes

    def calculate_emissions_with_user_defined_strategy(self, unified_data_dataframes):

        emission_calc_config = {
            **self.config_dict,
            **unified_data_dataframes,
            "Strategy": self.strategy_class
        }
        StrategyInvoker().calculate_and_save_emissions(self.emissions_output_folder, **emission_calc_config)

    def create_run_info_file(self):

        end_time = time()
        file_location = f"{self.emissions_output_folder}/run_info.txt"
        create_info_file(file_location, get_timestamp(), self.mode, self.start_time, end_time, self.config_dict)

    def log_is_done_message(self):

        end_time = time()
        logging.info(
            f"Done. The output files are in {self.emissions_output_folder}. "
            f"Duration of run: {(end_time - self.start_time) / 60} min")