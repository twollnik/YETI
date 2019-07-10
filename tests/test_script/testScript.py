from unittest import TestCase, main
from unittest.mock import MagicMock
import os
import sys
import shutil
from datetime import datetime
import logging


class TestScript(TestCase):

    def setUp(self) -> None:

        if os.path.isdir("tests/test_script/"):
            os.chdir("tests/test_script/")

    def tearDown(self) -> None:
        os.chdir("../..")

    def test_config1(self):

        try:
            shutil.rmtree(f"output_mode_input_data")
        except FileNotFoundError:
            pass

        sys.argv = f"run_yeti.py -c test_config.yaml".split()
        logging.warning = MagicMock()

        execfile(f"../../run_yeti.py")

        self.assertTrue(os.path.isdir(f"./output_mode_input_data/"))
        assert_file_exists_and_not_empty(f"./output_mode_input_data/run_info.txt")
        assert_file_exists_and_not_empty(f"./output_mode_input_data/PollutantType.CO_emissions.csv")
        assert_file_exists_and_not_empty(f"./output_mode_input_data/PollutantType.NOx_emissions.csv")
        assert_file_exists_and_not_empty(f"./output_mode_input_data/unified_emission_factors.csv")
        assert_file_exists_and_not_empty(f"./output_mode_input_data/unified_los_speeds.csv")
        assert_file_exists_and_not_empty(f"./output_mode_input_data/unified_vehicle_data.csv")
        assert_file_exists_and_not_empty(f"./output_mode_input_data/unified_link_data.csv")
        assert_file_exists_and_not_empty(f"./output_mode_input_data/unified_traffic_data.csv")

        logging.warning.assert_not_called()

    def test_config2(self):

        try:
            shutil.rmtree(f"output_hbefa")
            shutil.rmtree(f"temp_unified_data")
        except FileNotFoundError:
            pass

        sys.argv = f"run_yeti.py -c test_config2.yaml".split()

        logging.warning = MagicMock()
        execfile(f"../../run_yeti.py")

        self.assertTrue(os.path.isdir(f"output_hbefa/"))
        assert_file_exists_and_not_empty(f"output_hbefa/run_info.txt")
        assert_file_exists_and_not_empty(f"output_hbefa/PollutantType.CO_emissions.csv")
        assert_file_exists_and_not_empty(f"output_hbefa/PollutantType.NOx_emissions.csv")
        assert_file_exists_and_not_empty(f"./temp_unified_data/unified_emission_factors.csv")
        assert_file_exists_and_not_empty(f"./temp_unified_data/unified_vehicle_data.csv")
        assert_file_exists_and_not_empty(f"./temp_unified_data/unified_link_data.csv")
        assert_file_exists_and_not_empty(f"./temp_unified_data/unified_traffic_data.csv")

        logging.warning.assert_not_called()

    def test_config3(self):

        try:
            shutil.rmtree(f"output_copert_with_speed")
        except FileNotFoundError:
            pass

        sys.argv = f"run_yeti.py -c test_config3.yaml".split()
        logging.warning = MagicMock()

        execfile(f"../../run_yeti.py")

        self.assertTrue(os.path.isdir(f"output_copert_with_speed/"))
        assert_file_exists_and_not_empty(f"output_copert_with_speed/run_info.txt")
        assert_file_exists_and_not_empty(f"output_copert_with_speed/PollutantType.CO_emissions.csv")
        assert_file_exists_and_not_empty(f"output_copert_with_speed/PollutantType.NOx_emissions.csv")

        logging.warning.assert_called_once()

    def test_config4(self):

        try:
            shutil.rmtree(f"output_copert_cold")
        except FileNotFoundError:
            pass

        sys.argv = f"run_yeti.py -c test_config4.yaml".split()
        logging.warning = MagicMock()

        execfile(f"../../run_yeti.py")

        self.assertTrue(os.path.isdir("output_copert_cold/"))
        assert_file_exists_and_not_empty("output_copert_cold/run_info.txt")
        assert_file_exists_and_not_empty("output_copert_cold/PollutantType.NOx_cold_emissions.csv")
        assert_file_exists_and_not_empty("output_copert_cold/PollutantType.NOx_hot_emissions.csv")
        assert_file_exists_and_not_empty("output_copert_cold/PollutantType.NOx_total_emissions.csv")
        assert_file_exists_and_not_empty("output_copert_cold/PollutantType.CO_cold_emissions.csv")
        assert_file_exists_and_not_empty("output_copert_cold/PollutantType.CO_hot_emissions.csv")
        assert_file_exists_and_not_empty("output_copert_cold/PollutantType.CO_total_emissions.csv")

        for file in ["output_copert_cold/PollutantType.NOx_cold_emissions.csv",
                     "output_copert_cold/PollutantType.NOx_hot_emissions.csv",
                     "output_copert_cold/PollutantType.NOx_total_emissions.csv",
                     "output_copert_cold/PollutantType.CO_cold_emissions.csv",
                     "output_copert_cold/PollutantType.CO_hot_emissions.csv",
                     "output_copert_cold/PollutantType.CO_total_emissions.csv"]:
            with open(file) as fp:
                file_header = fp.readline()
                self.assertEqual(file_header.split(',')[:4], ["LinkID", "DayType", "Dir", "Hour"])

        logging.warning.assert_not_called()

    def test_config5(self):

        try:
            shutil.rmtree(f"output_pm_non_exhaust")
        except FileNotFoundError:
            pass

        sys.argv = f"run_yeti.py -c test_config5.yaml".split()
        logging.warning = MagicMock()

        execfile(f"../../run_yeti.py")

        self.assertTrue(os.path.isdir("output_pm_non_exhaust/"))
        self.assertTrue(os.path.isfile("output_pm_non_exhaust/run_info.txt"))
        self.assertTrue(os.path.isfile("output_pm_non_exhaust/TSP_emissions.csv"))
        self.assertTrue(os.path.isfile("output_pm_non_exhaust/PM10_emissions.csv"))
        self.assertTrue(os.path.isfile("output_pm_non_exhaust/PM25_emissions.csv"))

        for file in ["output_pm_non_exhaust/TSP_emissions.csv",
                     "output_pm_non_exhaust/PM10_emissions.csv",
                     "output_pm_non_exhaust/PM25_emissions.csv"]:
            with open(file) as fp:
                file_header = fp.readline()
                self.assertEqual(file_header.split(',')[:4], ["LinkID", "DayType", "Dir", "Hour"])

        logging.warning.assert_not_called()

    def test_use_n_traffic_data_rows_works(self):

        try:
            shutil.rmtree(f"output_config6")
        except FileNotFoundError:
            pass

        sys.argv = f"run_yeti.py -c test_config6.yaml".split()
        execfile(f"../../run_yeti.py")

        num_lines = get_line_count("output_config6/PollutantType.NOx_emissions.csv")

        self.assertEqual(6, num_lines)


def execfile(filepath, globals=None, locals=None):
    if globals is None:
        globals = {}
    globals.update({
        "__file__": filepath,
        "__name__": "__main__",
    })
    with open(filepath, 'rb') as file:
        exec(compile(file.read(), filepath, 'exec'), globals, locals)


def assert_file_exists_and_not_empty(filename):

    if os.path.isfile(filename) is False:
        raise AssertionError(f"The file {filename} does not exist. It should have been created by the test.")

    lines = get_line_count(filename)
    if lines < 3:
        raise AssertionError(f"The file {filename} is too short. It is expected to include more content. "
                             f"(Length: {lines} lines)")


def get_line_count(filename):

    with open(filename) as fp:
        return len(fp.readlines())

if __name__ == '__main__':
    main()