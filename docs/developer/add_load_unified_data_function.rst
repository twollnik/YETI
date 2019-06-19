.. _add-load-unified-data-function:

Change how unified_data is loaded
=================================

The ``load_unified_data_function`` specified in a config file is responsible for loading unified_data
files from disc. Each ``load_unified_data_function`` is related to a Strategy that works with the output of the
function.

How is ``load_unified_data_function`` called?
---------------------------------------------

``load_unified_data_function`` is called with the single argument ``kwargs``. ``kwargs`` contains all all
arguments from the config file and the key-value pairs returned by the ``load_input_data_function`` that
was called earlier in the run.

.. code-block:: python

    def load_unified_data(**kwargs):

        # load unified_data from file

        return {
            # return dict with loaded unified_data
        }

*Example*

Say you want to load los speeds data from file, because your Strategy requires los speeds data:

.. code-block:: python

    import pandas as pd

    def load_unified_data(**kwargs):

        los_speeds_data_file = kwargs["unified_los_speeds_data_file"]
        los_speeds_data = pd.read_csv(los_speeds_file)

        ... # load the other relevant datasets

        return {
            "los_speeds_data": los_speeds_data,
            ...
        }

You need to make sure that eather the config file or the return dictionary from the ``load_input_data_function`` contains
the key ``unified_los_speeds_data_file``, so that you can access it in the ``kwargs``.

What should the ``load_unified_data_function`` return?
------------------------------------------------------

The function should return a dictionary. The dictionary should contain all dataframes that will be used by the Strategy.
Additionally the return dictionary needs to contain the keys ``"traffic_data"``, ``"link_data"``, and ``"vehicle_data"``.
For example:

.. code-block:: python

    def load_unified_data(**kwargs):

        # load unified_data from file

        return {
            "traffic_data": a_data_frame_with_unified_traffic_data,
            "link_data": a_data_frame_with_unified_link_data,
            "vehicle_data": a_data_frame_with_unified_vehicle_data,
            ...
        }

