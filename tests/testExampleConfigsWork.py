"""
This TestCase runs run_yeti on the configs in the folder example/example_configs to make
sure that the demo works correctly.
"""
import logging
import os
import re
import shutil
import sys
import time
from unittest import TestCase, main
from unittest.mock import MagicMock

import pandas as pd


class TestCalcAvgDailyEmissions(TestCase):

    def setUp(self) -> None:

        self.old_dir = os.getcwd()
        if not "tests" in os.listdir("."):
            os.chdir("..")

        self.start_time = time.time()
        logging.warning = MagicMock()

        self.output_dir = "tests/temp_output_created_by_tests"

    def tearDown(self) -> None:

        # remove all files that were created during this test
        if os.path.isdir(self.output_dir):
            shutil.rmtree(self.output_dir)

        os.chdir(self.old_dir)
        logging.warning.reset_mock()

    def test_copert_hot_config(self):

        change_output_folder_to_test_folder("example/example_configs/copert_hot_config.yaml", self.output_dir)

        sys.argv = f"run_yeti.py -c {self.output_dir}/config.yaml".split()
        execfile(f"run_yeti.py")

        logging.warning.assert_not_called()

    def test_copert_cold_config(self):

        change_output_folder_to_test_folder("example/example_configs/copert_cold_config.yaml", self.output_dir)

        sys.argv = f"run_yeti.py -c {self.output_dir}/config.yaml".split()
        execfile(f"run_yeti.py")

        logging.warning.assert_not_called()

        # ------- test that the hot emissions data does not have the same values in all rows --------
        hot_emissions = pd.read_csv(f"{self.output_dir}/PollutantType.CO_hot_emissions.csv")
        emission_values = [(row["pc vehicle_a"], row["lcv vehicle_b"]) for _, row in hot_emissions.iterrows()]
        unique_emission_values = set(emission_values)
        self.assertGreater(len(unique_emission_values), 2)

    def test_copert_hot_fixed_speed_config(self):

        change_output_folder_to_test_folder("example/example_configs/copert_hot_fixed_speed_config.yaml", self.output_dir)

        sys.argv = f"run_yeti.py -c {self.output_dir}/config.yaml".split()
        execfile(f"run_yeti.py")

        logging.warning.assert_not_called()

    def test_hbefa_hot_config(self):

        change_output_folder_to_test_folder("example/example_configs/hbefa_hot_config.yaml", self.output_dir)

        sys.argv = f"run_yeti.py -c {self.output_dir}/config.yaml".split()
        execfile(f"run_yeti.py")

        logging.warning.assert_not_called()

    def test_hbefa_cold_config(self):

        change_output_folder_to_test_folder("example/example_configs/hbefa_hot_config.yaml", self.output_dir)

        sys.argv = f"run_yeti.py -c {self.output_dir}/config.yaml".split()
        execfile(f"run_yeti.py")

        logging.warning.assert_not_called()

    def test_pm_non_exhaust_config(self):

        change_output_folder_to_test_folder("example/example_configs/pm_non_exhaust_config.yaml", self.output_dir)

        sys.argv = f"run_yeti.py -c {self.output_dir}/config.yaml".split()
        execfile(f"run_yeti.py")

        logging.warning.assert_not_called()

    def test_copert_config(self):

        change_output_folder_to_test_folder("example/example_configs/copert_config.yaml", self.output_dir)

        sys.argv = f"run_yeti.py -c {self.output_dir}/config.yaml".split()
        execfile(f"run_yeti.py")

        logging.warning.assert_not_called()

    def test_hbefa_config(self):

        change_output_folder_to_test_folder("example/example_configs/hbefa_config.yaml", self.output_dir)

        sys.argv = f"run_yeti.py -c {self.output_dir}/config.yaml".split()
        execfile(f"run_yeti.py")

        logging.warning.assert_not_called()

    def test_hbefa_hot_and_copert_cold_config(self):

        change_output_folder_to_test_folder("example/example_configs/hbefa_hot_and_copert_cold_config.yaml", self.output_dir)

        sys.argv = f"run_yeti.py -c {self.output_dir}/config.yaml".split()
        execfile(f"run_yeti.py")

        logging.warning.assert_not_called()

    def test_copert_hot_config_mode_yeti_format(self):

        change_output_folder_to_test_folder("example/example_configs/copert_hot_config.yaml", self.output_dir)
        change_config_mode_to_yeti_format_data(f"{self.output_dir}/config.yaml", f"{self.output_dir}/config.yaml")
        update_validation_function(f"{self.output_dir}/config.yaml",
                                   "code.copert_hot_strategy.validate.validate_copert_yeti_format_files",
                                   f"{self.output_dir}/config.yaml")

        try:
            sys.argv = f"run_yeti.py -c {self.output_dir}/config.yaml".split()
            execfile(f"run_yeti.py")
        except Exception as e:
            raise e
        else:
            logging.warning.assert_called_once()

    def test_copert_cold_config_mode_yeti_format(self):

        change_output_folder_to_test_folder("example/example_configs/copert_cold_config.yaml", self.output_dir)
        change_config_mode_to_yeti_format_data(f"{self.output_dir}/config.yaml", f"{self.output_dir}/config.yaml")
        update_validation_function(f"{self.output_dir}/config.yaml",
                                   "code.copert_cold_strategy.validate.validate_copert_cold_yeti_format_files",
                                   f"{self.output_dir}/config.yaml")

        try:
            sys.argv = f"run_yeti.py -c {self.output_dir}/config.yaml".split()
            execfile(f"run_yeti.py")
        except Exception as e:
            raise e
        else:
            logging.warning.assert_called_once()

    def test_copert_hot_fixed_speed_config_mode_yeti_format(self):

        change_output_folder_to_test_folder("example/example_configs/copert_hot_fixed_speed_config.yaml", self.output_dir)
        change_config_mode_to_yeti_format_data(f"{self.output_dir}/config.yaml", f"{self.output_dir}/config.yaml")
        update_validation_function(f"{self.output_dir}/config.yaml",
                                   "code.copert_hot_fixed_speed_strategy.validate.validate_copert_fixed_speed_yeti_format_files",
                                   f"{self.output_dir}/config.yaml")

        try:
            sys.argv = f"run_yeti.py -c {self.output_dir}/config.yaml".split()
            execfile(f"run_yeti.py")
        except Exception as e:
            raise e
        else:
            logging.warning.assert_called_once()

    def test_hbefa_hot_config_mode_yeti_format(self):

        change_output_folder_to_test_folder("example/example_configs/hbefa_hot_config.yaml", self.output_dir)
        change_config_mode_to_yeti_format_data(f"{self.output_dir}/config.yaml", f"{self.output_dir}/config.yaml")
        update_validation_function(f"{self.output_dir}/config.yaml",
                                   "code.hbefa_hot_strategy.validate.validate_hbefa_yeti_format_files",
                                   f"{self.output_dir}/config.yaml")

        try:
            sys.argv = f"run_yeti.py -c {self.output_dir}/config.yaml".split()
            execfile(f"run_yeti.py")
        except Exception as e:
            raise e
        else:
            logging.warning.assert_not_called()

    def test_hbefa_cold_config_mode_yeti_format(self):

        change_output_folder_to_test_folder("example/example_configs/hbefa_cold_config.yaml", self.output_dir)
        change_config_mode_to_yeti_format_data(f"{self.output_dir}/config.yaml", f"{self.output_dir}/config.yaml")

        try:
            sys.argv = f"run_yeti.py -c {self.output_dir}/config.yaml".split()
            execfile(f"run_yeti.py")
        except Exception as e:
            raise e
        else:
            logging.warning.assert_not_called()

    def test_pm_non_exhaust_config_mode_yeti_format(self):

        change_output_folder_to_test_folder("example/example_configs/pm_non_exhaust_config.yaml", self.output_dir)
        change_config_mode_to_yeti_format_data(f"{self.output_dir}/config.yaml", f"{self.output_dir}/config.yaml")
        update_validation_function(f"{self.output_dir}/config.yaml",
                                   "code.pm_non_exhaust_strategy.validate.validate_pm_non_exhaust_yeti_format_files",
                                   f"{self.output_dir}/config.yaml")

        try:
            sys.argv = f"run_yeti.py -c {self.output_dir}/config.yaml".split()
            execfile(f"run_yeti.py")
        except Exception as e:
            raise e
        else:
            logging.warning.assert_not_called()

    def test_copert_config_mode_yeti_format(self):

        change_output_folder_to_test_folder("example/example_configs/copert_config.yaml", self.output_dir)
        change_config_mode_to_yeti_format_data(f"{self.output_dir}/config.yaml", f"{self.output_dir}/config.yaml")

        try:
            sys.argv = f"run_yeti.py -c {self.output_dir}/config.yaml".split()
            execfile(f"run_yeti.py")
        except Exception as e:
            raise e
        else:
            logging.warning.assert_not_called()

    def test_hbefa_config_mode_yeti_format(self):

        change_output_folder_to_test_folder("example/example_configs/hbefa_config.yaml", self.output_dir)
        change_config_mode_to_yeti_format_data(f"{self.output_dir}/config.yaml", f"{self.output_dir}/config.yaml")

        try:
            sys.argv = f"run_yeti.py -c {self.output_dir}/config.yaml".split()
            execfile(f"run_yeti.py")
        except Exception as e:
            raise e
        else:
            logging.warning.assert_not_called()


    def test_hbefa_hot_and_copert_cold_config_mode_yeti_format(self):

        change_output_folder_to_test_folder("example/example_configs/hbefa_hot_and_copert_cold_config.yaml", self.output_dir)
        change_config_mode_to_yeti_format_data(f"{self.output_dir}/config.yaml", f"{self.output_dir}/config.yaml")

        try:
            sys.argv = f"run_yeti.py -c {self.output_dir}/config.yaml".split()
            execfile(f"run_yeti.py")
        except Exception as e:
            raise e
        else:
            logging.warning.assert_not_called()


def change_output_folder_to_test_folder(config_file, new_output_dir):

    with open(config_file) as fp:
        config_contents = fp.read()

    new_config_contents = re.sub(r"output_folder:[\s\t]+\w+", f"output_folder:  {new_output_dir}", config_contents)

    if not os.path.isdir(new_output_dir):
        os.mkdir(new_output_dir)

    with open(f"{new_output_dir}/config.yaml", "w") as fp:
        fp.write(new_config_contents)


def execfile(filepath, globals=None, locals=None):
    if globals is None:
        globals = {}
    globals.update({
        "__file__": filepath,
        "__name__": "__main__",
    })
    with open(filepath, 'rb') as file:
        exec(compile(file.read(), filepath, 'exec'), globals, locals)


def change_config_mode_to_yeti_format_data(input_file, output_file):

    with open(input_file) as fp:
        config_contents = fp.read()

    new_config_contents = re.sub(r"mode:[\s\t]+berlin_format", "mode:  yeti_format", config_contents)

    with open(output_file, "w") as fp:
        fp.write(new_config_contents)


def update_validation_function(input_file, validation_function, output_file):

    with open(input_file) as fp:
        config_contents = fp.read()

    if "validation_function" in config_contents:
        new_config_contents = re.sub(r"validation_function:[\s\t]+[\.\w]+",
                                     f"validation_function:  {validation_function}",
                                     config_contents)
    else:
        new_config_contents = config_contents + f"\nvalidation_function:  {validation_function}"
    with open(output_file, "w") as fp:
        fp.write(new_config_contents)


if __name__ == "__main__":
    main()
