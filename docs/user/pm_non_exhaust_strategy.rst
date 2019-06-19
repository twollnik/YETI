PMNonExhaustStrategy
====================

The ``PMNonExhaustStrategy`` implements emission calculation for PM from non-exhaust emissions.
Sources for PM non-exhaust emissions are tyre wear, brake wear and road surface emissions.

It uses a global assumption about the load_factor for trucks. You need to specify the assumed load_factor
in the configuration file as a number between 0 and 1.

This Strategy calculates total suspended particles (TSP), PM10, and PM25 emissions independently
for tyre wear, brake wear, and road surface emissions. Then it will add up the emissions
from all sources to obtain total PM non-exhaust emissions for TSP, PM10, and PM25 and output the result.

Output of a model run with this Strategy are three csv files:

- TSP emissions
- PM10 emissions
- PM25 emissions

Data Requirements
-----------------

What data the ``PMNonExhaustStrategy`` requires depends on the ``mode`` set in the configuration file for the run.

Data requirements for mode ``input_data``
'''''''''''''''''''''''''''''''''''''''''

.. image:: ../../diagrams/pm_non_exhaust_input_data_requirements.png
    :width: 400
    :height: 400

:ref:`how-to-read-er`

--------

**link data** |br|
Just like the link data required for the other Strategies. See :ref:`here <link-data-explained>`.

--------

**traffic data** |br|
Just like the traffic data required for the other Strategies. See :ref:`here <traffic-data-explained>`.

--------

**fleet composition data** |br|
Just like the fleet composition data required for the other Strategies. See :ref:`here <fleet-comp-data-explained>`.

--------

**los speeds data** |br|
Just like the los speeds data data required for the ``CopertHotStrategy``. See :ref:`here <los-speeds-data-explained>`.

Data requirements for mode ``unified_data``
'''''''''''''''''''''''''''''''''''''''''''

.. image:: ../../diagrams/pm_non_exhaust_unified_data_requirements.png
    :width: 400
    :height: 400

:ref:`how-to-read-er`

--------

**unified link data** |br|
Just like the unified link data required for the other Strategies. See :ref:`here <unified-link-data-explained>`.

--------

**unified vehicle data** |br|
Just like the unified vehicle data required for the other Strategies. See :ref:`here <unified-vehicle-data-explained>`.

--------

**unified traffic data** |br|
Just like the unified traffic data required for the other Strategies. See :ref:`here <unified-traffic-data-explained>`.

--------

**unified los speeds data** |br|
Just like the unified los speeds data data required for the ``CopertHotStrategy``. See :ref:`here <unified-los-speeds-data-explained>`.

Supported Pollutants
--------------------

The only pollutant supported by this Strategy is ``PollutantType.PM_Non_Exhaust``. Set it in the config file:

.. code-block:: yaml

    pollutant:              PollutantType.PM_Non_Exhaust

What to put in the config.yaml
------------------------------
If you want to use the ``PMNonExhaustStrategy`` for your calculations, you need to set
the following options in your ``config.yaml``.
Don't forget to add the parameters specified here: :doc:`config`

Please note that we currently don't provide validation functions for this Strategy.

If using mode ``input_data``:
'''''''''''''''''''''''''''''

.. code-block:: yaml

    strategy:                     code.pm_non_exhaust_strategy.PMNonExhaustStrategy.PMNonExhaustStrategy
    load_input_data_function:     code.pm_non_exhaust_strategy.load_input_data.load_pm_non_exhaust_input_data
    load_unified_data_function:   code.pm_non_exhaust_strategy.load_unified_data.load_pm_non_exhaust_unified_data

    input_link_data:              path/to/link_data.csv
    input_fleet_composition:      path/to/fleet_composition_data.csv
    input_los_speeds:             path/to/los_speeds_data.csv
    input_traffic_data:           path/to/traffic_data.csv

    load_factor:                  0.3  # A number between 0 and 1. The assumption about the average load of trucks.

If using mode ``unified_data``:
'''''''''''''''''''''''''''''''

.. code-block:: yaml

    strategy:                     code.pm_non_exhaust_strategy.PMNonExhaustStrategy.PMNonExhaustStrategy
    load_unified_data_function:   code.pm_non_exhaust_strategy.load_unified_data.load_pm_non_exhaust_unified_data

    unified_link_data:            path/to/unified_link_data.csv
    unified_vehicle_data:         path/to/unified_vehicle_data.csv
    unified_los_speeds:           path/to/unified_los_speed_data.csv
    unified_traffic_data:         path/to/unified_traffic_data.csv

    load_factor:                  0.3  # A number between 0 and 1. The assumption about the average load of trucks.


.. |br| raw:: html

    <br>
