"""
This TestCase runs run_yeti on the configs in the folder example/example_configs to make
sure that the demo works correctly.
"""
from unittest import TestCase, main
from unittest.mock import MagicMock
import os
import sys
import time
import logging
import re


class TestCalcAvgDailyEmissions(TestCase):

    def setUp(self) -> None:

        if not "tests" in os.listdir("."):
            os.chdir("..")
        self.start_time = time.time()

        logging.warning = MagicMock()

    def tearDown(self) -> None:

        # remove all files that were created during this test
        for root, dirs, files in os.walk(".", topdown=False):
            for file_ in files:
                full_path = os.path.join(root, file_)
                stat = os.stat(full_path)

                if stat.st_mtime > self.start_time:
                    os.remove(full_path)

        # remove emtpy subfolders
        subfolders = next(os.walk('.'))[1]
        for subfolder in subfolders:
            if not os.listdir(subfolder):
                os.rmdir(subfolder)

        os.chdir("tests")

        logging.warning.reset_mock()

    def test_copert_hot_config(self):

        sys.argv = f"run_yeti.py -c example/example_configs/copert_hot_config.yaml".split()
        execfile(f"run_yeti.py")

        logging.warning.assert_not_called()

    def test_copert_cold_config(self):

        sys.argv = f"run_yeti.py -c example/example_configs/copert_cold_config.yaml".split()
        execfile(f"run_yeti.py")

        logging.warning.assert_not_called()

    def test_copert_hot_fixed_speed_config(self):

        sys.argv = f"run_yeti.py -c example/example_configs/copert_hot_fixed_speed_config.yaml".split()
        execfile(f"run_yeti.py")

        logging.warning.assert_not_called()

    def test_hbefa_hot_config(self):

        sys.argv = f"run_yeti.py -c example/example_configs/hbefa_hot_config.yaml".split()
        execfile(f"run_yeti.py")

        logging.warning.assert_not_called()

    def test_pm_non_exhaust_config(self):

        sys.argv = f"run_yeti.py -c example/example_configs/pm_non_exhaust_config.yaml".split()
        execfile(f"run_yeti.py")

        logging.warning.assert_not_called()

    def test_copert_hot_config_mode_unified_data(self):

        change_config_mode_to_unified_data("example/example_configs/copert_hot_config.yaml", "config_changed.yaml")

        try:
            sys.argv = f"run_yeti.py -c config_changed.yaml".split()
            execfile(f"run_yeti.py")
        except Exception as e:
            raise e
        else:
            logging.warning.assert_not_called()
        finally:
            os.remove("config_changed.yaml")

    def test_copert_cold_config_mode_unified_data(self):

        change_config_mode_to_unified_data("example/example_configs/copert_cold_config.yaml", "config_changed.yaml")

        try:
            sys.argv = f"run_yeti.py -c config_changed.yaml".split()
            execfile(f"run_yeti.py")
        except Exception as e:
            raise e
        else:
            logging.warning.assert_not_called()
        finally:
            os.remove("config_changed.yaml")


    def test_copert_hot_fixed_speed_config_mode_unified_data(self):

        change_config_mode_to_unified_data("example/example_configs/copert_hot_fixed_speed_config.yaml", "config_changed.yaml")

        try:
            sys.argv = f"run_yeti.py -c config_changed.yaml".split()
            execfile(f"run_yeti.py")
        except Exception as e:
            raise e
        else:
            logging.warning.assert_not_called()
        finally:
            os.remove("config_changed.yaml")

    def test_hbefa_hot_config_mode_unified_data(self):

        change_config_mode_to_unified_data("example/example_configs/hbefa_hot_config.yaml", "config_changed.yaml")

        try:
            sys.argv = f"run_yeti.py -c config_changed.yaml".split()
            execfile(f"run_yeti.py")
        except Exception as e:
            raise e
        else:
            logging.warning.assert_not_called()
        finally:
            os.remove("config_changed.yaml")

    def test_pm_non_exhaust_config_mode_unified_data(self):

        change_config_mode_to_unified_data("example/example_configs/pm_non_exhaust_config.yaml", "config_changed.yaml")

        try:
            sys.argv = f"run_yeti.py -c config_changed.yaml".split()
            execfile(f"run_yeti.py")
        except Exception as e:
            raise e
        else:
            logging.warning.assert_not_called()
        finally:
            os.remove("config_changed.yaml")


def execfile(filepath, globals=None, locals=None):
    if globals is None:
        globals = {}
    globals.update({
        "__file__": filepath,
        "__name__": "__main__",
    })
    with open(filepath, 'rb') as file:
        exec(compile(file.read(), filepath, 'exec'), globals, locals)


def change_config_mode_to_unified_data(input_file, output_file):

    with open(input_file) as fp:
        config_contents = fp.read()

    new_config_contents = re.sub(r"mode:[\s\t]+input_data", "mode:  unified_data", config_contents)

    with open(output_file, "w") as fp:
        fp.write(new_config_contents)

if __name__ == "__main__":
    main()
