.. _add-load-input-data-function:

Support a new data format
=========================

This page describes how to adapt YETI to work with a different input_data dataset. We assume that the input_data
you want to use can be converted to fit the unified_data format.

The function ``load_input_data_function`` (that you specify in the config file) is responsible for handling
input_data. It does these four things:

1. Load the input_data from file.
2. Convert the input_data to unified_data.
3. Save the unified_data to file.
4. Return the locations of the unified_data files.

It is likely that you can change the input_data loading behaviour without having to write much code yourself.
We provide the class ``DataLoader`` that is extensible and can likely be adapted to your needs without
too much effort. More info :ref:`below <use-data-loader>`.

Example
-------

This as an example ``load_input_data_function``:

.. code-block:: python

    def load_input_data_for_my_strategy(**kwargs) -> Dict[str, str]:

        # load the input_data
        # convert the input_data to unified_data
        # save the unified_data to disc

        # then return the locations of the unified_data files in a dictionary
        return {
            "unified_link_data": "path/to/unified_link_data.csv",
            "unified_traffic_data": "path/to/unified_traffic_data.csv",
            ...
        }

How is the function called?
---------------------------

The ``load_input_data_function`` is called with a single argument: ``kwargs``. ``kwargs`` is a
dictionary that contains all arguments from the config file.

For example, if your config file looks like this:

.. code-block:: yaml

    # config.yaml
    mode:                         input_data
    strategy:                     path.to.Strategy
    load_input_data_function:     path.to.input_data_load_function
    load_unified_data_function:   path.to.unified_data_load_function
    output_folder:                output_folder
    input_link_data:              path/to/link_data.csv
    input_fleet_composition:      path/to/fleet_composition_data.csv
    input_emission_factors:       path/to/emission_factor_data.csv
    input_los_speeds:             path/to/los_speeds_data.csv
    input_traffic_data:           path/to/traffic_data.csv
    input_vehicle_mapping:        path/to/vehicle_mapping_data.csv

Then the ``kwargs`` dictionary the ``load_input_data_function`` is called with looks like this:

.. code-block:: python

    {
        "mode":                         "input_data",
        "strategy":                     "path.to.Strategy",
        "load_input_data_function":     "path.to.input_data_load_function",
        "load_unified_data_function":   "path.to.unified_data_load_function",
        "output_folder":                "output_folder",
        "input_link_data":              "path/to/link_data.csv",
        "input_fleet_composition":      "path/to/fleet_composition_data.csv",
        "input_emission_factors":       "path/to/emission_factor_data.csv",
        "input_los_speeds":             "path/to/los_speeds_data.csv",
        "input_traffic_data":           "path/to/traffic_data.csv",
        "input_vehicle_mapping":        "path/to/vehicle_mapping_data.csv"
    }

You can work with the ``kwargs`` like any other Python dictionary. ``kwargs`` gives you access to all
configuration arguments. Use them.

What should the function return?
--------------------------------

The ``load_input_data_function`` should return a dictionary containing paths to the unified_data
files that were constructed and saved by the ``load_input_data_function``.

*Example*

Let's say the ``load_input_data_function`` creates the four files ``unified_data/link_data.csv``,
``unified_data/traffic_data.csv``, ``unified_data/vehicle_data.csv``, and ``unified_data/ef_data.csv`` that
contain data in unified_data format.
Then the return dictionary of the function should look like this:

.. code-block:: python

    {
        unified_link_data:      unified_data/link_data.csv
        unified_traffic_data:   unified_data/traffic_data.csv
        unified_vehicle_data:   unified_data/vehicle_data.csv
        unified_ef_data:        unified_data/ef_data.csv
    }

Note that the ``load_unified_data_function`` that is specified in the config will be called after the
``load_input_data_function``. The keys in the return dictionary must match the keyword arguments
that the ``load_unified_data_function`` expects as input.

.. _use-data-loader:

Use the existing ``DataLoader``
-------------------------------

As mentioned at the top of the page, there is an easy way to adapt to a new input_data format. We provide the
class ``DataLoader`` that is responsible for loading input_data from file and converting it to unified_data
format. We also provide the function ``save_dataframes`` to save the unified_data to file and construct the
return dictionary.

The ``DataLoader`` is originally designed to work with input_data as requried by the
:doc:`CopertHotStrategy <../user/copert_hot_strategy>` and output unified_data as required by the
``CopertHotStrategy``. We will now discuss how to adapt the ``DataLoader`` to your data requirements.

There are two usage scenarios:

1. One of your input_data files has a different format.
2. You don't use all the unified_data files that are used by the ``CopertHotStrategy``.

We will take a detailed look at the two usage scenarios a bit later on the page. For now
we want to look at what they have in common:

You need to subclass the ``DataLoader`` and use the new class in the ``load_input_data_function``. For example:

Let's say you wrote the ``MyDataLoader`` that extends the ``DataLoader`` to fit your needs:

.. code-block:: python

    from code.data_loading.DataLoader import DataLoader

    class MyDataLoader(DataLoader):

        ...

Now you want to use ``MyDataLoader`` in the ``load_input_data_function``:

.. code-block:: python

    from path.to.MyDataLoader import MyDataLoader
    from code.strategy_helpers.helpers import save_dataframes

    def load_input_data(**kwargs):

        output_folder = kwargs["output_folder"]
        loader = MyDataLoader(**kwargs)
        data = loader.load_data(use_nh3_ef=False)
        (link_data, vehicle_data, traffic_data, los_speeds_data, emission_factor_data, _) = data

        unified_data_file_paths = save_dataframes(
            output_folder,
            {
                "unified_emission_factors": emission_factor_data,
                "unified_los_speeds": los_speeds_data,
                "unified_vehicle_data": vehicle_data,
                "unified_link_data": link_data,
                "unified_traffic_data": traffic_data
             }
        )
        return unified_data_file_paths

Now we will take a look at the two usage scenarios mentioned before.

1. One of your input_data files has a different format
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This means that you will need to change

1. How the input_data is read from file.
2. How one or multiple unified_data files are constructed.

For this you will need a ``DataLoader`` subclass so that you can change the behaviour of the ``DataLoader``.

1. Change how the input_data is read from file.
'''''''''''''''''''''''''''''''''''''''''''''''

The class ``FileDataLoader`` is responsible for loading input_data from file. To change how input_data
is loaded you should subclass the ``FileDataLoader``, override relevant methods and make your ``DataLoader``
use the new ``FileDataLoader``

First, here is **how to subclass the FileDataLoader:**

.. code-block:: python

    from code.data_loading.FileDataLoader import FileDataLoader

    MyFileDataLoader(FileDataLoader):

        ...  # override the method you would like to change


Secondly, these are the **methods you can override:**

.. code-block:: python

    load_link_data_from_file(self)  # override this method to change how input_data link data is loaded from file
    load_fleet_comp_data_from_file(self)  # override this method to change how input_data fleet composition data is loaded from file
    load_traffic_count_data_from_file(self)  # override this method to change how input_data traffic data is loaded from file
    load_emission_factor_data_from_file(self)  # override this method to change how input_data emission factor data is loaded from file
    load_los_speeds_data_from_file(self)  # override this method to change how input_data los_speeds data is loaded from file
    load_vehicle_mapping_data_from_file(self)  # override this method to change how input_data vehicle mapping data is loaded from file
    load_nh3_ef_data_from_file_if_wanted(self, use_nh3_ef)  # override this method to change how input_data tier 2 NH3 emission factor data is loaded from file

The ``self`` argument to the functions will give you access to these attributes:

.. code-block:: python

    self.emission_factor_file
    self.los_speeds_file
    self.fleet_comp_file
    self.link_data_file
    self.traffic_file
    self.vehicle_name_to_category_mapping
    self.nh3_ef_file
    self.nh3_mapping_file

For example, here is how you would change the way that link data is loaded from file:

.. code-block:: python

    from code.data_loading.FileDataLoader import FileDataLoader

    MyFileDataLoader(FileDataLoader):

        def load_link_data_from_file(self):

            link_data_file_location = self.link_data_file
            link_data = ...  # read the link data from file
            return link_data

The last thing you need to do is to **make your DataLoader use the new MyFileDataLoader:**

.. code-block:: python

    from code.data_loading.DataLoader import DataLoader
    from path.to.MyFileDataLoader import MyFileDataLoader

    class MyDataLoader(DataLoader):

        # override the method load_input_data
        def load_input_data(self, use_nh3_ef: bool):
            return MyFileDataLoader(**self.filenames_dict).load_data(use_nh3_ef)

2. Change how one or multiple unified_data files are constructed
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

Every unified_data file is constructed in a dedicated method by the ``DataLoader``. To change
how a unified_data file is constructed, override the method that constructs it.

These are the methods that construct unified_data:

.. code-block:: python

    # load_traffic_data depends on the input_data fleet composition data, link data, and traffic data
    load_traffic_data(self, fleet_comp_data, link_data, traffic_data)

    # load_link_data depends on the input_data link data
    load_link_data(self, link_data: pd.DataFrame)

    # load_vehicle_data depends on the input_data fleet composition data
    load_vehicle_data(self, fleet_comp_data: pd.DataFrame)

    # load_emission_factor_data depends on the input_data fleet composition data, vehicle mapping data,
    # emission factor data, NH3 ef data, and NH3 ef mapping data
    load_emission_factor_data(self,
                              use_nh3_ef: bool,
                              fleet_comp_data: pd.DataFrame,
                              vehicle_mapping_data: pd.DataFrame,
                              ef_data: pd.DataFrame,
                              nh3_ef_data: pd.DataFrame,
                              nh3_mapping_data: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]

    # load_los_speeds_data depends on the input_data link data and los speeds data
    load_los_speeds_data(self, link_data: pd.DataFrame, los_speeds_data: pd.DataFrame)

The comments in the code block above show which methods need to be overridden when which input_data
dataset changes format. For example if the input_data link data changes, you need to override
``load_traffic_data``, ``load_link_data``, and ``load_los_speeds_data``.

For example if your input_data traffic data format changes, you will need to override ``load_traffic_data``:

.. code-block:: python


    from code.data_loading.DataLoader import DataLoader

    class MyDataLoader(DataLoader):

        # override the method load_traffic_data
        def load_traffic_data(self, fleet_comp_data, link_data, traffic_data):

            # construct the traffic data in unified format
            unified_traffic_data = ...

            return unified_traffic_data

2. You don't use all the unified_data files that are used by the ``CopertHotStrategy``.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
If this is the case you should override the method that constructs the unified_data file that
you don't want to use. Let the method return None. For example say you don't want to use emission factor
data:

.. code-block:: python

    from code.data_loading.DataLoader import DataLoader

    class MyDataLoader(DataLoader):

        load_emission_factor_data(self,
                              use_nh3_ef: bool,
                              fleet_comp_data: pd.DataFrame,
                              vehicle_mapping_data: pd.DataFrame,
                              ef_data: pd.DataFrame,
                              nh3_ef_data: pd.DataFrame,
                              nh3_mapping_data: pd.DataFrame):

            return None