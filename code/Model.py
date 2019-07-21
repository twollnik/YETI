import logging
import os
from time import time

from code.StrategyInvoker import StrategyInvoker
from code.script_helpers.create_info_file import create_info_file
from code.script_helpers.dynamic_import_from import dynamic_import_from
from code.strategy_helpers.helpers import get_timestamp


class Model:
    """
    This class implements the main flow of control for a YETI run.

    Model makes sure that everything that needs to be done is done and happens in the right order.
    It relies on user defined functions for data loading and validation. It also relies on the
    StrategyInvoker in combination with the user defined Strategy to calculate emissions.

    Methods
    -------
    run
        The main interface for this class. Implements the abstract flow of control for a
        YETI run and delegates the actual work to other functions.
    """

    def __init__(self):

        self.start_time = None
        self.config_file = None
        self.config_dict = None
        self.mode = None

        self.strategy_class = None
        self.yeti_format_data_load_function = None
        self.berlin_format_data_load_function = None
        self.validation_function = None

        self.emissions_output_folder = None
        self.yeti_format_data_output_folder = None

        self.n_steps = 6
        self.current_step = 1

    def run(self, config_dict, config_file):

        self.initialize(config_dict, config_file)
        self.log_run_information()

        self.log_step("Initializing output directories.")
        self.create_output_folders_if_necessary()

        self.log_step("Validating the dataset.")
        self.validate_dataset()

        self.log_step("Converting data in berlin_format to data in yeti_format.")
        yeti_format_file_locations = self.load_berlin_format_data()

        self.log_step("Loading yeti_format data.")
        yeti_format_data_dataframes = self.load_yeti_format_data(yeti_format_file_locations)

        self.log_step("Calculating emissions.")
        self.calculate_emissions_with_user_defined_strategy(yeti_format_data_dataframes)

        self.log_step("Creating 'run_info.txt'.")
        self.create_run_info_file()

        self.log_is_done_message()

    def initialize(self, config_dict, config_file):

        self.start_time = time()
        self.config_file = config_file
        self.config_dict = config_dict
        self.mode = self.config_dict["mode"]

        self.strategy_class = self.import_strategy()
        self.yeti_format_data_load_function, self.berlin_format_data_load_function, self.validation_function = \
            self.import_user_defined_functions()

    def import_strategy(self):

        path_to_strategy_class = self.config_dict["strategy"]
        strategy_class = dynamic_import_from(path_to_strategy_class)
        return strategy_class

    def import_user_defined_functions(self):

        load_yeti_format_data_function = self.config_dict["load_yeti_format_data_function"]
        load_berlin_format_data_function = self.config_dict["load_berlin_format_data_function"]
        validation_function = self.config_dict.get("validation_function")

        yeti_format_data_load_function = dynamic_import_from(load_yeti_format_data_function)

        if validation_function is not None:
            validation_function = dynamic_import_from(validation_function)
        else:
            validation_function = None

        if self.mode == "berlin_format":
            berlin_format_data_load_function = dynamic_import_from(load_berlin_format_data_function)
        else:
            berlin_format_data_load_function = None

        return yeti_format_data_load_function, berlin_format_data_load_function, validation_function

    def log_run_information(self):

        pollutants = self.config_dict["pollutants"]
        strategy = self.config_dict["strategy"]
        load_berlin_format_data_function = self.config_dict["load_berlin_format_data_function"]
        load_yeti_format_data_function = self.config_dict["load_yeti_format_data_function"]
        validation_function = self.config_dict.get("validation_function")

        logging.info(
            f"The config file for this run is: {os.path.abspath(self.config_file)}\n"
            f"pollutants: {pollutants}\n"
            f"mode: {self.mode}\n"
            f"strategy: {strategy}\n"
            f"load_berlin_format_data_function: {load_berlin_format_data_function}\n"
            f"load_yeti_format_data_function: {load_yeti_format_data_function}\n"
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
        yeti_format_output_folder = self.config_dict.get("output_folder_for_yeti_format_data")

        self.emissions_output_folder = self.create_folder_if_it_does_not_exist_already(emissions_output_folder)
        if yeti_format_output_folder is not None:
            self.yeti_format_data_output_folder = self.create_folder_if_it_does_not_exist_already(yeti_format_output_folder)

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
            logging.debug("No validation function given in config. Validation is skipped.")

    def load_berlin_format_data(self):

        if self.mode == 'berlin_format':
            yeti_format_file_locations = self.berlin_format_data_load_function(**self.config_dict)
        else:
            logging.debug("Call load yeti_format data function skipped because mode is 'yeti_format'.")
            yeti_format_file_locations = self.config_dict
        return yeti_format_file_locations

    def load_yeti_format_data(self, yeti_format_file_locations):

        kwargs = {
            **self.config_dict,
            **yeti_format_file_locations
        }
        yeti_format_data_dataframes = self.yeti_format_data_load_function(**kwargs)
        return yeti_format_data_dataframes

    def calculate_emissions_with_user_defined_strategy(self, yeti_format_data_dataframes):

        emission_calc_config = {
            **self.config_dict,
            **yeti_format_data_dataframes,
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