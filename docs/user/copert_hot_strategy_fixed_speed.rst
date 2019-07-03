CopertHotFixedSpeedStrategy
===========================

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

Data requirements for mode ``input_data``
'''''''''''''''''''''''''''''''''''''''''

The same ``input_data`` as ``CopertHotStrategy`` is required with these modifications:

- los speeds data is not required.
- The link data may contain the column ``Speed_kmh`` with fixed speeds for each street link.
- The traffic data does not need to contain los percentage columns (LOS1Perc ... LOS4Perc).

Data requirements for mode ``unified_data``
'''''''''''''''''''''''''''''''''''''''''''

The same ``unified_data`` as ``CopertHotStrategy`` is required with these modifications:

- unified los speeds data is not required.
- The unified link data may contain the column ``Speed`` with fixed speeds for each street link.
- The unified traffic data does not need to contain los percentage columns (LOS1Percentage ... LOS4Percentage)

Supported pollutants
--------------------

``CopertHotFixedSpeedStrategy`` supports these pollutants:

.. code-block:: yaml

    # add one of the following lines to your config.yaml
    pollutant:  PollutantType.NOx
    pollutant:  PollutantType.CO
    pollutant:  PollutantType.NH3
    pollutant:  PollutantType.VOC
    pollutant:  PollutantType.PM_Exhaust

Make sure to include emission factors for the pollutant you are using in the emission factor data.

What to put in the config.yaml
------------------------------
If you want to use the ``CopertHotFixedSpeedStrategy`` for the your calculations, you need to set
the following options in your ``config.yaml``.
Don't forget to add the parameters specified here: :doc:`config`.

If using mode ``input_data``:
'''''''''''''''''''''''''''''

.. code-block:: yaml

    strategy:                        code.copert_hot_fixed_speed_strategy.CopertHotFixedSpeedStrategy.CopertHotFixedSpeedStrategy
    load_input_data_function:        code.copert_hot_fixed_speed_strategy.load_input_data.load_copert_fixed_speed_input_data
    load_unified_data_function:      code.copert_hot_fixed_speed_strategy.load_unified_data.load_copert_fixed_speed_unified_data
    validation_function:             code.copert_hot_fixed_speed_strategy.validate.validate_copert_fixed_speed_input_files

    # if you want to use a global speed for all links, include this:
    v:                            50

    input_link_data:              path/to/link_data.csv
    input_fleet_composition:      path/to/fleet_composition_data.csv
    input_emission_factors:       path/to/emission_factor_data.csv
    input_traffic_data:           path/to/traffic_data.csv
    input_vehicle_mapping:        path/to/vehicle_mapping_data.csv

    use_nh3_tier2_ef:             yes or no
    # if you set use_nh3_tier2_ef to yes, also add these lines:
    input_nh3_emission_factors:   path/to/nh3_emission_factor_data.csv
    input_nh3_mapping:            path/to/nh3_mapping_data.csv

You may have data on Tier 2 emission factors for NH3. If you set ``use_nh3_tier2_ef: yes`` in the config file,
YETI will read them from the specified files and use them in the emission calculation for pollutant ``PollutantType.NH3``.

If using mode ``unified_data``:
'''''''''''''''''''''''''''''''

.. code-block:: yaml

    strategy:                        code.copert_hot_fixed_speed_strategy.CopertHotFixedSpeedStrategy.CopertHotFixedSpeedStrategy
    load_unified_data_function:      code.copert_hot_fixed_speed_strategy.load_unified_data.load_copert_fixed_speed_unified_data
    validation_function:             code.copert_hot_fixed_speed_strategy.validate.validate_copert_fixed_speed_unified_files

    # if you want to use a global speed for all links, include this:
    v:                            50

    unified_emission_factors:     path/to/unified_ef_data.csv
    unified_vehicle_data:         path/to/unified_vehicle_data.csv
    unified_link_data:            path/to/unified_link_data.csv
    unified_traffic_data:         path/to/unified_traffic_data.csv