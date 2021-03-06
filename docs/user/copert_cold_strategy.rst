CopertColdStrategy
==================

.. warning::

    This Strategy cannot be used by itself. It can only be used as a ``cold_strategy`` with
    the ``CopertStrategy`` or the ``HbefaStrategy``.

The ``CopertColdStrategy`` implements emission calculation with the
`COPERT methodology for cold start emissions <https://www.eea.europa.eu/publications/emep-eea-guidebook-2016/>`_.
It uses global assumptions about the average length of a trip (in km/h) and the average ambient temperature
(in degrees Celsius) that are set in the configuration file.

Also in the configuration file you may specify some road types and area types that will be excluded
from the cold emission calculation. This means that cold emissions will be zero for all vehicles at links that belong
to the road types or area types that you want to exclude.
Possible road types to be excluded are: ``MW_Nat``, ``MW_City``, ``Trunk_Nat``, ``Trunk_City``, ``Distr``,
``Local``, and ``Access``. Area types that can be excluded are ``Rural`` and ``Urban``.

The ``CopertColdStrategy`` takes the emissions from the hot strategy that is used in the
``CopertStrategy`` or ``HbefaStrategy`` as input. It uses the hot emissions to derive hot emission
factors and to calculate total emissions.

Output of a model run with this Strategy are two csv files per pollutant:

- cold start emissions
- total emissions

Data requirements
-----------------

What data the ``CopertColdStrategy`` requires depends on the ``mode`` set in the configuration file for the run.

Data requirements for mode ``berlin_format``
''''''''''''''''''''''''''''''''''''''''''''

All input data in ``berlin_format`` required by the ``CopertHotStrategy`` is also required for the ``CopertColdStrategy``.

.. _cold-ef-data-explained:

Additionally a file with **cold emission factors** is required:

.. image:: ../../diagrams/cold_ef_table.png
    :height: 250
    :width: 250

:ref:`how-to-read-er`

This is the cold ef table as provided by EEA recommendations.

- *Pollutant*: One of the following: ``CO``, ``NOx``, or ``VOC``.
- *VehSegment*: A vehicle segment. One of the following: ``Mini``, ``Small``, ``Medium``, or ``Large-SUV-Executive``.
- *MinSpeed*: The minimum speed the A,B and C values in this row are valid for.
- *MaxSpeed*: The maximum speed the A,B and C values in this row are valid for.
- *MinTemp*: The minimum temperature the A,B and C values in this row are valid for.
- *MaxTemp*: The maximum temperature the A,B and C values in this row are valid for.
- *A*: The A parameter for the cold ef calculation.
- *B*: The B parameter for the cold ef calculation.
- *C*: The C parameter for the cold ef calculation.

*Example*:

========= ========== ======== ======== ======= ======= ===== ====== =====
Pollutant VehSegment MinSpeed MaxSpeed MinTemp MaxTemp A     B      C
========= ========== ======== ======== ======= ======= ===== ====== =====
CO        Mini       5        25       -20     15      0.563 -0.895 4.964
CO        Mini       26       45       -20     15      0.842 -0.349 3.485
CO        Mini       5        45       15              0.222 -0.876 10.12
========= ========== ======== ======== ======= ======= ===== ====== =====

Data requirements for mode ``yeti_format``
'''''''''''''''''''''''''''''''''''''''''''

All data in ``yeti_format`` required by the ``CopertHotStrategy`` is also required for the ``CopertColdStrategy``.

Additional requirements:

- A file with cold emission factors is required, as :ref:`described above <cold-ef-data-explained>`.
- A vehicle mapping file is required. It needs to be in :ref:`this format <mapping-data-explained>`.

Supported Pollutants
--------------------

``CopertColdStrategy`` supports these pollutants:

.. code-block:: yaml

    PollutantType.CO
    PollutantType.NOx
    PollutantType.VOC

Set the pollutants for a run in your config file. For example:

.. code-block:: yaml

    pollutants:          [PollutantType.CO, PollutantType.NOx]

Make sure to include emission factors for the pollutants you are using in the emission factor data.

What to put in the config.yaml
------------------------------
If you want to use the ``CopertColdStrategy`` for your calculations, you need to set
the following options in your ``config.yaml``.
Don't forget to add the parameters specified here: :doc:`config`

If using mode ``berlin_format``:
''''''''''''''''''''''''''''''''

.. code-block:: yaml

    strategy:                     code.copert_strategy.CopertStrategy.CopertStrategy
    load_berlin_format_data_function:     code.copert_strategy.load_berlin_format_data.load_copert_berlin_format_data
    load_yeti_format_data_function:   code.copert_strategy.load_yeti_format_data.load_copert_yeti_format_data
    validation_function:          code.copert_cold_strategy.validate.validate_copert_cold_berlin_format_files

    berlin_format_link_data:              path/to/link_data.csv
    berlin_format_fleet_composition:      path/to/fleet_composition_data.csv
    berlin_format_emission_factors:       path/to/emission_factor_data.csv
    berlin_format_los_speeds:             path/to/los_speeds_data.csv
    berlin_format_traffic_data:           path/to/traffic_data.csv
    berlin_format_vehicle_mapping:        path/to/vehicle_mapping_data.csv
    berlin_format_cold_ef_table:          path/to/cold_ef_table.csv

    ltrip:                        12  # the average length of a trip in km/h
    temperature:                  15  # the average ambient temperature in °C
    exclude_road_types:           [MW_City]  # Exclude multiple road types like this: [MW_City, Trunk_City]
    exclude_area_types:           [Rural]    # Or: [Urban]

If using mode ``yeti_format``:
'''''''''''''''''''''''''''''''

.. code-block:: yaml

    strategy:                     code.copert_strategy.CopertStrategy.CopertStrategy
    load_yeti_format_data_function:   code.copert_strategy.load_yeti_format_data.load_copert_yeti_format_data
    validation_function:          code.copert_cold_strategy.validate.validate_copert_cold_yeti_format_files

    yeti_format_emission_factors:     path/to/yeti_format_ef_data.csv
    yeti_format_los_speeds:           path/to/yeti_format_los_speed_data.csv
    yeti_format_vehicle_data:         path/to/yeti_format_vehicle_data.csv
    yeti_format_link_data:            path/to/yeti_format_link_data.csv
    yeti_format_traffic_data:         path/to/yeti_format_traffic_data.csv
    yeti_format_cold_ef_table:        path/to/cold_ef_table.csv
    yeti_format_vehicle_mapping:      path/to/vehicle_mapping_data.csv

    ltrip:                        12  # the average length of a trip in km/g
    temperature:                  15  # the average ambient temperature in °C
    exclude_road_types:           [MW_City]  # Exclude multiple road types like this: [MW_City, Trunk-City]
    exclude_area_types:           [Rural]    # Or: [Urban]

.. _use-different-hot-strategy:
