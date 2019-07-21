.. _add-load-yeti-format-data-function:

Change how data in yeti_format is loaded
========================================

The ``load_yeti_format_data_function`` specified in a config file is responsible for loading data in yeti_format
from disc. Each ``load_yeti_format_data_function`` is related to a Strategy that works with the output of the
function.

How is ``load_yeti_format_data_function`` called?
-------------------------------------------------

``load_yeti_format_data_function`` is called with the single argument ``kwargs``. ``kwargs`` contains all all
arguments from the config file and the key-value pairs returned by the ``load_berlin_format_data_function`` that
was called earlier in the run.

.. code-block:: python

    def load_yeti_format_data(**kwargs):

        # load data in yeti_format from file

        return {
            # return dict with loaded data in yeti_format
        }

*Example*

Say you want to load los speeds data from file, because your Strategy requires los speeds data:

.. code-block:: python

    import pandas as pd

    def load_yeti_format_data(**kwargs):

        los_speeds_data_file = kwargs["yeti_format_los_speeds_data_file"]
        los_speeds_data = pd.read_csv(los_speeds_file)

        ... # load the other relevant datasets

        return {
            "los_speeds_data": los_speeds_data,
            ...
        }

You need to make sure that eather the config file or the return dictionary from the ``load_berlin_format_data_function`` contains
the key ``yeti_format_los_speeds_data_file``, so that you can access it in the ``kwargs``.

What should the ``load_yeti_format_data_function`` return?
----------------------------------------------------------

The function should return a dictionary. The dictionary should contain all dataframes that will be used by the Strategy.
Additionally the return dictionary needs to contain the keys ``"traffic_data"``, ``"link_data"``, and ``"vehicle_data"``.
For example:

.. code-block:: python

    def load_yeti_format_data(**kwargs):

        # load data in yeti_format from file

        return {
            "traffic_data": a_data_frame_with_yeti_format_traffic_data,
            "link_data": a_data_frame_with_yeti_format_link_data,
            "vehicle_data": a_data_frame_with_yeti_format_vehicle_data,
            ...
        }

