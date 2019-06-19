"""
This TestCase runs run_yeti on the configs in the folder example/example_configs to make
sure that the demo works correctly.
"""
from unittest import TestCase, main
import os
import sys
import time


class TestCalcAvgDailyEmissions(TestCase):

    def setUp(self) -> None:

        os.chdir("..")
        self.start_time = time.time()

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

    def test_copert_hot_config(self):

        sys.argv = f"run_yeti.py -c example/example_configs/copert_hot_config.yaml".split()
        execfile(f"run_yeti.py")

    def test_copert_cold_config(self):

        sys.argv = f"run_yeti.py -c example/example_configs/copert_cold_config.yaml".split()
        execfile(f"run_yeti.py")

    def test_copert_hot_fixed_speed_config(self):

        sys.argv = f"run_yeti.py -c example/example_configs/copert_hot_fixed_speed_config.yaml".split()
        execfile(f"run_yeti.py")

    def test_hbefa_hot_config(self):

        sys.argv = f"run_yeti.py -c example/example_configs/hbefa_hot_config.yaml".split()
        execfile(f"run_yeti.py")

    def test_pm_non_exhaust_config(self):

        sys.argv = f"run_yeti.py -c example/example_configs/pm_non_exhaust_config.yaml".split()
        execfile(f"run_yeti.py")


def execfile(filepath, globals=None, locals=None):
    if globals is None:
        globals = {}
    globals.update({
        "__file__": filepath,
        "__name__": "__main__",
    })
    with open(filepath, 'rb') as file:
        exec(compile(file.read(), filepath, 'exec'), globals, locals)


if __name__ == "__main__":
    main()
