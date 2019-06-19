from unittest import TestCase, main
import os
import sys

from time import time


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

        os.chdir("tests")


    def test_copert_hot_config(self):

        sys.argv = f"run_yeti.py -c example/example_configs/copert_hot_config.yaml".split()
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
