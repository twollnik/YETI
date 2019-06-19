YETI - Yet Another Emissions From Traffic Inventory
====================================================

|Build Status| |Coverage| |Docs| |Python version| |License|

.. |Build Status| image:: https://travis-ci.com/twollnik/YETI.svg?branch=master
    :target: https://travis-ci.com/twollnik/YETI
.. |Docs| image:: https://readthedocs.org/projects/iass-yeti/badge/?version=latest
    :target: https://iass-yeti.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status
.. |Python version| image:: https://img.shields.io/badge/Python%20version-3.6%20and%20above-lightgrey.svg
.. |Coverage| image:: https://codecov.io/gh/twollnik/YETI/branch/master/graph/badge.svg?token=mr44XEAIG5
   :target: https://codecov.io/gh/twollnik/YETI
   :alt: Test coverage
.. |License| image:: https://img.shields.io/badge/license-GPLv3-blue.svg
   :target: https://github.com/twollnik/YETI/blob/master/LICENSE


YETI is a tool for bottom-up traffic emission calculation. It helps you create high-resolution
traffic emission inventories.

YETI supports common emission calculation methodologies like COPERT or HBEFA. It was originally built to
work with data for the City of Berlin, but is flexible enough to be adopted to different datasets and regions.

This README is intended as a first introduction to the project. For more detailed information,
see the `docs <https://iass-yeti.readthedocs.io/en/latest//>`_.

.. contents:: Contents
    :local:
    :backlinks: none

.. installation-start-do-not-remove

Installation and Setup
----------------------

1. Make sure your Python version is supported
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
This project requires Python 3.6 or above. You can find our your Python version by running
``python --version`` on the command line. If your Python version is below 3.6, please upgrade to a newer version.

Note that YETI is tested for Python 3.6 and 3.7. However it should also work with newer Python versions. When in doubt,
run the tests on your computer. If they pass, you are good to go.

2. Clone the GitHub repository
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Clone the GitHub repositiory by running ``git clone https://github.com/twollnik/YETI.git`` on the command line.
You need to have git installed for this step. If you don't have git, get it `here <https://git-scm.com/book/en/v2/Getting-Started-Installing-Git/>`_.

These directories will be downloaded: ``code``, ``diagrams``, ``docs``, ``example``, and ``tests``.

3. Install the necessary packages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Install dependencies with pip by running ``pip install -r requirements.txt`` on the command line
from the repository root directory.
If you want to do development work you should also install dev dependencies:  ``pip install -r requirements-dev.txt``.

.. installation-end-do-not-remove
.. demo-start-do-not-remove

Demo
----

We have included example configuration files and example data for you to try out. You can find the example files
in the folder ``example/``. To run the demo, execute the following command on the command line from the
repository root directory: ``python -m run_yeti -c example/example_configs/copert_hot_config.yaml``. Instead of the
``copert_hot_config.yaml`` you can use any of the
`config files <https://iass-yeti.readthedocs.io/en/latest/user/config.html/>`_ in ``example/example_configs/``.

.. demo-end-do-not-remove
.. usage-start-do-not-remove

Usage
-----

Run the model
^^^^^^^^^^^^^

All interactions with YETI use the script ``run_yeti.py`` from the
project root directory. Run the script from the command line:
``python -m run_yeti``. Make sure that you run the script from the
repository root directory.

``run_yeti.py`` uses a configuration file in `YAML format <https://en.wikipedia.org/wiki/YAML>`_
where a `Strategy <https://iass-yeti.readthedocs.io/en/latest/user/what_is_strategy.html>`_
for the emission calculation method is defined together with all the necessary input/output file
locations and other parameters.

You may specify the location of the config file: ``python -m run_yeti -c path/to/config.yaml``.
If you don't specify a location for the config file explicitly, the path ``./config.yaml`` is used.
`Look here <https://iass-yeti.readthedocs.io/en/latest/user/config.html>`_
for more detailed information what should be included in the config file.

Run ``python -m run_yeti --help`` for short usage information.

Output of a model run are one or multiple emissions csv files and a file ``run_info.txt``.
All output files will be in the ``output_folder`` that you specify in the configuration file.

Run the tests
^^^^^^^^^^^^^^

We include Python unit tests to test most of the YETI code. If you modified the code and want to see if
it still works, you may want to execute the tests. Note that the tests are also run on our test
server automatically every time you push to the GitHub repository.

Execute the tests by running ``make test`` on the command line from the repository root
directory.

Note that `GNU Make <https://www.gnu.org/software/make/>`_ needs to be installed on your computer for
this to work. If you don't have GNU Make installed, you can run the tests with
``python -m unittest tests/*/test*.py tests/test*.py``.

.. usage-end-do-not-remove
.. data-requirements-start-do-not-remove

Data Requirements
------------------

YETI is a street level model. The road network you want to calculate emissions for needs to be
divided into street links.

For example datasets, take a look at ``example/example_input_data`` and ``example/example_unified_data``.

The two data classes
^^^^^^^^^^^^^^^^^^^^

We differentiate between ``input_data`` and ``unified_data``.

``input_data`` is data in the format that we were using at the start of
this project. It is not ideal for the calculations and needs to be
transformed to a different format to be suitable for the emissions
calculation.

``unified_data`` is data in a unified format. We provide functions to
transform ``input_data`` to ``unified_data`` for all Strategies.

The data that you are working with is likely in a different
format than our ``input_data``, however chances are that you can
tranform your data to fit the format of the ``unified_data`` class. If this is the
case, you only need to
`write a function to convert your data <https://iass-yeti.readthedocs.io/en/latest/developer/add_load_input_data_function.html>`_ to
``unified_data``. Once this is done you can use YETI with your data and
don't need to adapt any other part of the system.

Data requirements depend on Strategy
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The data requirements depend on how you want to calculate emissions. For
example calculating emissions with the COPERT methodology requires
different input data than a calculation with the HBEFA methodology.

Take a look at the `docs <https://iass-yeti.readthedocs.io/en/latest/user/what_is_strategy.html>`_
page of the Strategy you want to use to find out about the data requirements for that Strategy.

File format
^^^^^^^^^^^

All data files are csv files. They use comma (' , ') as seperator and the dot (' . ') for decimal points.

.. data-requirements-end-do-not-remove
.. contributing-start-do-not-remove

Contributing to YETI
--------------------

We are open for collaboration, however we have limited resources to review contributions.

Anyhow, all contributions should follow these guidelines:

- Code should comply with the `PEP8 style guide <https://www.python.org/dev/peps/pep-0008/>`_ as much as possible.
- All new features should be tested. YETI uses the built-in ``unittest`` module.
  If you are new to testing in Python, this website is a good starting point:
  `unittest introduction <http://pythontesting.net/framework/unittest/unittest-introduction/>`_.
- We follow a green build policy. This means that all the tests need to succeed on the test server
  before a Pull Request can be merged.

.. contributing-end-do-not-remove

--------------

This Section will be removed in a future version:

Emission calculation formula
----------------------------

The emissions are calculated according to the basis equation: E (g/h for
VehClass) = l \* nVeh \* EF

Emissions are determined per street segment (sst, for each traffic
direction and depending on its type and area), per hour (h) of a day
type (dt, 4 different ones accounted for), per driving mode (dm, 4
different LOS), for a vehicle class (VehClass = combination of Category,
Technology, Euro standard and Fuel).

With the data available for the city of Berlin the number of Vehicles is
determined by nVeh = QKfz \* LOSxPerc \* "Cat"14\_DTV \* Anteil

Currently ef is calculate for each VehClass according to COPERT method
as described above (4.i.) and velocity (speed\_kmh) for the each driving
mode LOS is taken from HBEFA database

Using the naming of vars this means that: E = length\_m \* VehCount \*
LOSx\_Perc \* Catx\_Perc \* VehPercofCat \* EF

Note on Units: lenght is then converted to km EF is in g/km nVeh is
number of vehicles from a certain class (per street per driving mode per
hour)
