CopertHotFixedSpeedStrategy
===========================

.. note::

    It is recommended to use the :doc:`CopertStrategy <copert_strategy>` with the config arguments
    ``only_hot: yes`` and ``fixed_speed: yes`` instead of this Strategy.

The ``CopertHotFixedStrategy`` implements emission calculation with the COPERT methodology
for hot emissions at the street level. It uses speed-dependent emission factors with fixed
speed values.

There are two ways to specify the fixed speed:

1. Add the parameter ``v: {speed, an integer}`` to your configuration file. The specified speed
   is used for all emission calculations.
2. Add a speed column (``Speed_kmh``) to the input file with the link data to specify a fixed
   speed for all emission calculations at a particular street link.

If you include ``v`` in the config file and add a speed column to the link data, the speed value in
``v`` will take precedence.

Data requirements
-----------------
What data the ``CopertHotFixedSpeedStrategy`` requires depends on the ``mode`` set in the configuration file for the run.

Data requirements for mode ``berlin_format``
''''''''''''''''''''''''''''''''''''''''''''

The same data in ``berlin_format`` as ``CopertHotStrategy`` is required with these modifications:

- los speeds data is not required.
- The link data may contain the column ``Speed_kmh`` with fixed speeds for each street link.
- The traffic data does not need to contain los percentage columns (LOS1Perc ... LOS4Perc).

Data requirements for mode ``yeti_format``
'''''''''''''''''''''''''''''''''''''''''''

The same data in ``yeti_format`` as ``CopertHotStrategy`` is required with these modifications:

- yeti_format los speeds data is not required.
- The yeti_format link data may contain the column ``Speed`` with fixed speeds for each street link.
- The yeti_format traffic data does not need to contain los percentage columns (LOS1Percentage ... LOS4Percentage)

Supported pollutants
--------------------

``CopertHotFixedSpeedStrategy`` supports these pollutants:

.. code-block:: yaml

    PollutantType.NOx
    PollutantType.CO
    PollutantType.NH3
    PollutantType.VOC
    PollutantType.PM_Exhaust

Set the pollutants for a run in your config file. For example:

.. code-block:: yaml

    pollutants:          [PollutantType.CO, PollutantType.NOx]

Make sure to include emission factors for the pollutants you are using in the emission factor data.

What to put in the config.yaml
------------------------------
If you want to use the ``CopertHotFixedSpeedStrategy`` for the your calculations, you need to set
the following options in your ``config.yaml``.
Don't forget to add the parameters specified here: :doc:`config`.

If using mode ``berlin_format``:
''''''''''''''''''''''''''''''''

.. code-block:: yaml

    strategy:                        code.copert_hot_fixed_speed_strategy.CopertHotFixedSpeedStrategy.CopertHotFixedSpeedStrategy
    load_berlin_format_data_function:        code.copert_hot_fixed_speed_strategy.load_berlin_format_data.load_copert_fixed_speed_berlin_format_data
    load_yeti_format_data_function:      code.copert_hot_fixed_speed_strategy.load_yeti_format_data.load_copert_fixed_speed_yeti_format_data
    validation_function:             code.copert_hot_fixed_speed_strategy.validate.validate_copert_fixed_speed_berlin_format_files

    # if you want to use a global speed for all links, include this:
    v:                            50

    berlin_format_link_data:              path/to/link_data.csv
    berlin_format_fleet_composition:      path/to/fleet_composition_data.csv
    berlin_format_emission_factors:       path/to/emission_factor_data.csv
    berlin_format_traffic_data:           path/to/traffic_data.csv
    berlin_format_vehicle_mapping:        path/to/vehicle_mapping_data.csv

    use_nh3_tier2_ef:             yes or no
    # if you set use_nh3_tier2_ef to yes, also add these lines:
    berlin_format_nh3_emission_factors:   path/to/nh3_emission_factor_data.csv
    berlin_format_nh3_mapping:            path/to/nh3_mapping_data.csv

You may have data on Tier 2 emission factors for NH3. If you set ``use_nh3_tier2_ef: yes`` in the config file,
YETI will read them from the specified files and use them in the emission calculation for pollutant ``PollutantType.NH3``.

If using mode ``yeti_format``:
'''''''''''''''''''''''''''''''

.. code-block:: yaml

    strategy:                        code.copert_hot_fixed_speed_strategy.CopertHotFixedSpeedStrategy.CopertHotFixedSpeedStrategy
    load_yeti_format_data_function:      code.copert_hot_fixed_speed_strategy.load_yeti_format_data.load_copert_fixed_speed_yeti_format_data
    validation_function:             code.copert_hot_fixed_speed_strategy.validate.validate_copert_fixed_speed_yeti_format_files

    # if you want to use a global speed for all links, include this:
    v:                            50

    yeti_format_emission_factors:     path/to/yeti_format_ef_data.csv
    yeti_format_vehicle_data:         path/to/yeti_format_vehicle_data.csv
    yeti_format_link_data:            path/to/yeti_format_link_data.csv
    yeti_format_traffic_data:         path/to/yeti_format_traffic_data.csv