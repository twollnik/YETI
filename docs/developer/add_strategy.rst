.. _add-strategy:

Add a Strategy
==============

Add a new Strategy if you want to support a new methodology/algorithm for emission calculation.
Before you add a new Strategy be sure to check that none of the existing Strategies do what you want.

Before you continue reading, make sure you have understood the :doc:`high level process <high_level_how_does_it_work>`
YETI works with.

Strategies are classes
----------------------

A Strategy is a Python class that is defined in a ``.py`` file. Each Strategy needs to contain the function
``calculate_emissions``.

.. code-block:: python

    class MyStrategy:

        def calculate_emissions(self,
                                traffic_and_link_data_row: Dict[str, Any],
                                vehicle_dict: Dict[str, str],
                                pollutant: str,
                                **kwargs):

            # Put the emission calculation logic here.

The function signature may be confusing for now. That is okay, we will get to the parameters in a second.

Why do we use a class? The answer is that classes can have state. Having the option to store data or results
in attributes gives you a lot more flexibility in the implementation.

Strategies collaborate with data handling functions
---------------------------------------------------

The functions ``load_input_data_function`` and ``load_unified_data_function`` (as specified in the config)
are used to load the data that is required by the Strategy.

``load_input_data_function`` is a function that reads the input_data for the Strategy from file, converts it to
unified_data format and saves the constructed unified_data to file. :doc:`more <add_load_input_data_function>`

``load_unified_data_function`` has the simple job of reading the required unified_data for the Strategy from
file. :doc:`more <add_load_unified_data_function>`

Each Strategy has a corresponding ``load_input_data_function`` and ``load_unified_data_function``.
If you write your own Strategy you may have to also write new data loading functions.

You can access the output of the data loading functions in ``calculate_emissions``, as described
:ref:`here <return-value-of-load-unified-data-function-is-passed-to-strategy>`.

How are Strategies called?
--------------------------

The Strategy's function ``calculate_emissions`` is called many times in a model run. The class that calls
``calculate_emissions`` is the ``StrategyInvoker``.

Let's take a look at the parameters of ``calculate_emissions``:

``traffic_and_link_data_row``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The ``StrategyInvoker`` performs an
`SQL-style inner join <https://www.w3resource.com/sql/joins/perform-an-inner-join.php>`_ on the given
unified link data and unified traffic data. It then calls the Strategy's method ``calculate_emissions`` once per row
in the resulting dataframe. The row is passed to ``calculate_emissions`` as a dictionary.

Let's look at an example. Say your link data and traffic data (belonging to ``unified_data`` class) look like this:

*link data*:

====== ============== ================ ========
LinkID AreaType       RoadType         MaxSpeed
====== ============== ================ ========
42_123 AreaType.Rural RoadType.MW_City 100
65_485 AreaType.Urban RoadType.Local   30
====== ============== ================ ========

*traffic_data*:

====== ===== ================ ==== ====================== ========================
LinkID Dir   DayType          Hour PC petrol <1.4L Euro-1 LCV diesel M+N1-I Euro-2
====== ===== ================ ==== ====================== ========================
42_123 Dir.L DayType.MONtoTHU 0    0.32                   0.0023999999
65_485 Dir.R DayType.SUN      9    12.8                   0.012
====== ===== ================ ==== ====================== ========================

After the SQL-style join we have this dataframe with the traffic and link data:

====== ============== ================ ======== ===== ================ ==== ====================== ========================
LinkID AreaType       RoadType         MaxSpeed Dir   DayType          Hour PC petrol <1.4L Euro-1 LCV diesel M+N1-I Euro-2
====== ============== ================ ======== ===== ================ ==== ====================== ========================
42_123 AreaType.Rural RoadType.MW_City 100      Dir.L DayType.MONtoTHU 0    0.32                   0.0023999999
65_485 AreaType.Urban RoadType.Local   30       Dir.R DayType.SUN      9    12.8                   0.012
====== ============== ================ ======== ===== ================ ==== ====================== ========================

The first call to ``calculate_emissions`` will be with this ``traffic_and_link_data_row`` :

.. code-block:: python

    {
    "LinkID":   42_123,
    "AreaType": "AreaType.Rural",
    "RoadType": "RoadType.MW_City",
    "MaxSpeed": 100,
    "Dir":      "Dir.L",
    "DayType":  "DayType.MONtoTHU",
    "Hour":     0,
    "PC petrol <1.4L Euro-1": 0.32,
    "LCV diesel M+N1-I Euro-2": 0.0023999999
    }

Now the Strategy's job is to take this dictionary and calculate emissions for the two vehicles.

The second call to ``calculate_emissions`` receives a dictionary with the data from the second
traffic and link data row as ``traffic_and_link_data_row``.

``vehicle_dict``
^^^^^^^^^^^^^^^^
This parameter is a dictionary mapping the names of vehicle classes to the corresponding vehicle category. For example
``calculate_emissions`` may be called with a ``vehicle_dict`` such as this:

.. code-block:: python

    {
        "PC petrol <1.4L Euro-1": "VehicleCategory.PC",
        "LCV diesel M+N1-I Euro-2": "VehicleCategory.LCV"
    }

In ``calculate_emissions`` you can use the ``vehicle_dict`` to access the category of a vehicle by its name or
use it to iterate over all vehicles. For example:

.. code-block:: python

    # MyStrategy.py
    class MyStrategy:
        def calculate_emissions(self,
                                traffic_and_link_data_row: Dict[str, Any],
                                vehicle_dict: Dict[str, str],
                                pollutant: str,
                                **kwargs):

            ...
            # access the category of a vehicle by its name:
            vehicle_a = ...  # assign some vehicle name to vehicle_a
            category_of_vehicle_a = vehicle_dict[vehicle_a]  # get vehicle_a's category
            ...
            # iterate over all vehicles:
            for vehicle_name, vehicle_category in vehicle_dict.items():
                # do some computation using vehicle_name and/or vehicle_category
            ...


The ``vehicle_dict`` is constructed from the unified vehicle data by the ``StrategyInvoker`` class.

``pollutant``
^^^^^^^^^^^^^
A String. The pollutant as specified in the configuration file.

``**kwargs``
^^^^^^^^^^^^
**All parameters specified in the configuration file** are passed to ``calculate_emissions`` as
`keyword arguments <https://treyhunner.com/2018/04/keyword-arguments-in-python/>`_. This means that you
can use all arguments from the config file in your strategy. You can even define custom
config options for your Strategy. An example for using a config parameter in the Strategy:

.. code-block:: yaml

    # config.yaml
    average_slope:      0.15

.. code-block:: python

    # MyStrategy.py
    class MyStrategy:
        def calculate_emissions(self,
                                traffic_and_link_data_row: Dict[str, Any],
                                vehicle_dict: Dict[str, str],
                                pollutant: str,
                                **kwargs):

            average_slope = kwargs["average_slope"]
            # You can now use average_slope in the emission calculation.

.. _return-value-of-load-unified-data-function-is-passed-to-strategy:

The **return value of the ``load_unified_data_function``** is also passed to ``calculate_emissions`` as keyword
arguments. This means that you can load the required data for the Strategy in the
``load_unified_data_function`` and then access it in the Strategy. For more details
on the ``load_unified_data_function`` look :doc:`here <add_load_unified_data_function>`.
An example for using a return value of the ``load_unified_data_function`` in the Strategy:

.. code-block:: python

    # function_to_load_unified_data.py
    import pandas as pd

    def load_unified_data(...):
        ...
        some_pandas_dataframe = pd.read_csv(...) # load the data
        ...
        return {
            "some_dataset": some_pandas_dataframe,
            ...
        }

.. code-block:: python

    # MyStrategy.py
    class MyStrategy:
        def calculate_emissions(self,
                                traffic_and_link_data_row: Dict[str, Any],
                                vehicle_dict: Dict[str, str],
                                pollutant: str,
                                **kwargs):

            some_dataset = kwargs["some_dataset"]
            # You can now use the dataframe some_dataset for the emission calculation.

What should Strategies return?
------------------------------
As discussed above, the Strategy's function ``calculate_emissions`` is called once for each row in a dataframe
obtained from joining the link data and the traffic data in an SQL-style fashion.

Each call to ``calculate_emissions`` should return the emissions for one row in the output emissions dataframe(s) as
a dictionary.

The ``StrategyInvoker`` will associate the emissions with the right link ID, day type, hour and direction and
save the emissions to disc.

One emissions file
^^^^^^^^^^^^^^^^^^
Most Strategies want to output a single csv file with emission data. To do so, a Strategy should return one dictionary
with emissions on each call to ``calculate_emissions``.

For example:

Let's say ``calculate_emissions`` was called with this ``traffic_and_link_data_row``:

.. code-block:: python

    {
    "LinkID":   42_123,
    "AreaType": "AreaType.Rural",
    "RoadType": "RoadType.MW_City",
    "MaxSpeed": 100,
    "Dir":      "Dir.L",
    "DayType":  "DayType.MONtoTHU",
    "Hour":     0,
    "PC petrol <1.4L Euro-1": 0.32,
    "LCV diesel M+N1-I Euro-2": 0.0023999999
    }

It should return a dictionary in this format:

.. code-block:: python

    {
    "PC petrol <1.4L Euro-1":   some_emissions_value,
    "LCV diesel M+N1-I Euro-2": some_other_emissions_value
    }

This will result in the following row being added to the emissions dataframe that is saved to disc:

====== ===== ================ ==== ====================== ==========================
LinkID Dir   DayType          Hour PC petrol <1.4L Euro-1 LCV diesel M+N1-I Euro-2
====== ===== ================ ==== ====================== ==========================
42_123 Dir.L DayType.MONtoTHU 0    some_emissions_value   some_other_emissions_value
====== ===== ================ ==== ====================== ==========================

Multiple emission files
^^^^^^^^^^^^^^^^^^^^^^^
Some Strategies want to output multiple emissions files. For example the ``PMNonExhaustStrategy`` outputs three
emission files; one file per particle type.

How many emission files are created depends on the output of ``calculate_emissions``. If you want to output multiple
emissions files, ``calculate_emissions`` needs to output a nested dictionary in this format:

.. code-block:: python

    {
    "emission_type_A":
        {
        "PC petrol <1.4L Euro-1": some type a emissions value,
        "LCV diesel M+N1-I Euro-2": some other type a emissions value,
        ...
        },
    "emission_type_B":
        {
        "PC petrol <1.4L Euro-1": some type b emissions value,
        "LCV diesel M+N1-I Euro-2": some other type b emissions value,
        ...
        }
    }

This will create two emissions files, one with type a emissions and one with type b emissions. The names
of the output emission files are prefixed with the corresponding keys of the outer dictionary.
