.. _add-load-input-data-function:

Support a new data format
=========================

This page describes how to adapt YETI to work with a dataset that is not in berlin_format and not in yeti_format.
We assume that the dataset you want to use can be converted to fit the yeti_format.

The function ``load_berlin_format_data_function`` (that you specify in the config file) is responsible for handling
input data. It does these four things:

1. Load the input data from file.
2. Convert the input data to fit yeti_format.
3. Save the constructed data in yeti_format to file.
4. Return the locations of the files in yeti_format.

It is likely that you can change the input data loading behaviour without having to write much code yourself.
We provide the class ``DataLoader`` that is extensible and can likely be adapted to your needs without
too much effort. More info :ref:`below <use-data-loader>`.

Example
-------

This as an example ``load_berlin_format_data_function``:

.. code-block:: python

    def load_berlin_format_data_for_my_strategy(**kwargs) -> Dict[str, str]:

        # load the data in berlin_format
        # convert the data to yeti_format
        # save the data in yeti_format to disc

        # then return the locations of the files in yeti_format in a dictionary
        return {
            "yeti_format_link_data": "path/to/yeti_format_link_data.csv",
            "yeti_format_traffic_data": "path/to/yeti_format_traffic_data.csv",
            ...
        }

How is the function called?
---------------------------

The ``load_berlin_format_data_function`` is called with a single argument: ``kwargs``. ``kwargs`` is a
dictionary that contains all arguments from the config file.

For example, if your config file looks like this:

.. code-block:: yaml

    # config.yaml
    mode:           berlin_format
    strategy:                     path.to.Strategy
    load_berlin_format_data_function:     path.to.berlin_format_data_load_function
    load_yeti_format_data_function:   path.to.yeti_format_data_load_function
    output_folder:                output_folder
    berlin_format_link_data:              path/to/link_data.csv
    berlin_format_fleet_composition:      path/to/fleet_composition_data.csv
    berlin_format_emission_factors:       path/to/emission_factor_data.csv
    berlin_format_los_speeds:             path/to/los_speeds_data.csv
    berlin_format_traffic_data:           path/to/traffic_data.csv
    berlin_format_vehicle_mapping:        path/to/vehicle_mapping_data.csv

Then the ``kwargs`` dictionary the ``load_berlin_format_data_function`` is called with looks like this:

.. code-block:: python

    {
        "mode":                         "berlin_format",
        "strategy":                     "path.to.Strategy",
        "load_berlin_format_data_function":     "path.to.berlin_format_data_load_function",
        "load_yeti_format_data_function":   "path.to.yeti_format_data_load_function",
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

The ``load_berlin_format_data_function`` should return a dictionary containing paths to the files with data in yeti_format
that were constructed and saved by the ``load_berlin_format_data_function``.

*Example*

Let's say the ``load_berlin_format_data_function`` creates the four files ``yeti_format_data/link_data.csv``,
``yeti_format_data/traffic_data.csv``, ``yeti_format_data/vehicle_data.csv``, and ``yeti_format_data/ef_data.csv`` that
contain data in yeti_format.
Then the return dictionary of the function should look like this:

.. code-block:: python

    {
        yeti_format_link_data:      yeti_format_data/link_data.csv
        yeti_format_traffic_data:   yeti_format_data/traffic_data.csv
        yeti_format_vehicle_data:   yeti_format_data/vehicle_data.csv
        yeti_format_ef_data:        yeti_format_data/ef_data.csv
    }

Note that the ``load_yeti_format_data_function`` that is specified in the config will be called after the
``load_berlin_format_data_function``. The keys in the return dictionary must match the keyword arguments
that the ``load_yeti_format_data_function`` expects as input.

.. _use-data-loader:

Use the existing ``DataLoader``
-------------------------------

As mentioned at the top of the page, there is an easy way to adapt to a new input data format (meaning
data in a format different from berlin_format). We provide the
class ``DataLoader`` that is responsible for loading input data from file and converting it to yeti_format.
We also provide the function ``save_dataframes`` to save the data in yeti_format to file and construct the
return dictionary.

The ``DataLoader`` is originally designed to work with data in berlin_format as required by the
:doc:`CopertHotStrategy <../user/copert_hot_strategy>` and output data in yeti_format as required by the
``CopertHotStrategy``. We will now discuss how to adapt the ``DataLoader`` to your data requirements.

There are two usage scenarios:

1. One of your berlin_format files has a different format.
2. You don't use all the files in yeti_format that are used by the ``CopertHotStrategy``.

We will take a detailed look at the two usage scenarios a bit later on the page. For now
we want to look at what they have in common:

You need to subclass the ``DataLoader`` and use the new class in the ``load_berlin_format_data_function``. For example:

Let's say you wrote the ``MyDataLoader`` that extends the ``DataLoader`` to fit your needs:

.. code-block:: python

    from code.data_loading.DataLoader import DataLoader

    class MyDataLoader(DataLoader):

        ...

Now you want to use ``MyDataLoader`` in the ``load_berlin_format_data_function``:

.. code-block:: python

    from path.to.MyDataLoader import MyDataLoader
    from code.strategy_helpers.helpers import save_dataframes

    def load_berlin_format_data(**kwargs):

        output_folder = kwargs["output_folder"]
        loader = MyDataLoader(**kwargs)
        data = loader.load_data(use_nh3_ef=False)
        (link_data, vehicle_data, traffic_data, los_speeds_data, emission_factor_data, _) = data

        yeti_format_data_file_paths = save_dataframes(
            output_folder,
            {
                "yeti_format_emission_factors": emission_factor_data,
                "yeti_format_los_speeds": los_speeds_data,
                "yeti_format_vehicle_data": vehicle_data,
                "yeti_format_link_data": link_data,
                "yeti_format_traffic_data": traffic_data
             }
        )
        return yeti_format_data_file_paths

Now we will take a look at the two usage scenarios mentioned before.

1. One of your berlin_format files has a different format
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This means that you will need to change

1. How the input data is read from file.
2. How one or multiple files in yeti_format are constructed.

For this you will need a ``DataLoader`` subclass so that you can change the behaviour of the ``DataLoader``.

1. Change how the input data is read from file.
'''''''''''''''''''''''''''''''''''''''''''''''

The class ``FileDataLoader`` is responsible for loading input data (e.g. data in berlin_format) from file.
To change how input data is loaded you should subclass the ``FileDataLoader``, override relevant methods
and make your ``DataLoader`` use the new ``FileDataLoader``

First, here is **how to subclass the FileDataLoader:**

.. code-block:: python

    from code.data_loading.FileDataLoader import FileDataLoader

    MyFileDataLoader(FileDataLoader):

        ...  # override the method you would like to change


Secondly, these are the **methods you can override:**

.. code-block:: python

    load_link_data_from_file(self)  # override this method to change how berlin_format link data is loaded from file
    load_fleet_comp_data_from_file(self)  # override this method to change how berlin_format fleet composition data is loaded from file
    load_traffic_count_data_from_file(self)  # override this method to change how berlin_format traffic data is loaded from file
    load_emission_factor_data_from_file(self)  # override this method to change how berlin_format emission factor data is loaded from file
    load_los_speeds_data_from_file(self)  # override this method to change how berlin_format los_speeds data is loaded from file
    load_vehicle_mapping_data_from_file(self)  # override this method to change how berlin_format vehicle mapping data is loaded from file
    load_nh3_ef_data_from_file_if_wanted(self, use_nh3_ef)  # override this method to change how berlin_format tier 2 NH3 emission factor data is loaded from file

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

        # override the method load_berlin_format_data
        def load_berlin_format_data(self, use_nh3_ef: bool):
            return MyFileDataLoader(**self.filenames_dict).load_data(use_nh3_ef)

2. Change how one or multiple files in yeti_format are constructed
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

Every yeti_format file is constructed in a dedicated method by the ``DataLoader``. To change
how a yeti_format file is constructed, override the method that constructs it.

These are the methods that construct data in yeti_format:

.. code-block:: python

    # load_traffic_data depends on the berlin_format fleet composition data, link data, and traffic data
    load_traffic_data(self, fleet_comp_data, link_data, traffic_data)

    # load_link_data depends on the berlin_format link data
    load_link_data(self, link_data: pd.DataFrame)

    # load_vehicle_data depends on the berlin_format fleet composition data
    load_vehicle_data(self, fleet_comp_data: pd.DataFrame)

    # load_emission_factor_data depends on the berlin_format fleet composition data, vehicle mapping data,
    # emission factor data, NH3 ef data, and NH3 ef mapping data
    load_emission_factor_data(self,
                              use_nh3_ef: bool,
                              fleet_comp_data: pd.DataFrame,
                              vehicle_mapping_data: pd.DataFrame,
                              ef_data: pd.DataFrame,
                              nh3_ef_data: pd.DataFrame,
                              nh3_mapping_data: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]

    # load_los_speeds_data depends on the berlin_format link data and los speeds data
    load_los_speeds_data(self, link_data: pd.DataFrame, los_speeds_data: pd.DataFrame)

The comments in the code block above show which methods need to be overridden when which input
dataset changes format. For example if the input link data changes, you need to override
``load_traffic_data``, ``load_link_data``, and ``load_los_speeds_data``.

For example if your traffic data format changes, you will need to override ``load_traffic_data``:

.. code-block:: python


    from code.data_loading.DataLoader import DataLoader

    class MyDataLoader(DataLoader):

        # override the method load_traffic_data
        def load_traffic_data(self, fleet_comp_data, link_data, traffic_data):

            # construct the traffic data in yeti_format
            yeti_format_traffic_data = ...

            return yeti_format_traffic_data

2. You don't use all the files in yeti_format that are used by the ``CopertHotStrategy``.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
If this is the case you should override the method that constructs the yeti_format file that
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