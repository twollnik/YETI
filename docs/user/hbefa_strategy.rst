HbefaStrategy
=============

The HbefaStrategy implements emission calculation for hot and (optionally) cold emissions focusing
on calculation with the Hbefa methodology.

.. note::

    The possible configurations for this Strategy can become quite complex. Please have a look at the
    example config files ``hbefa_config.yaml``, ``hbefa_hot_config.yaml``,
    and ``hbefa_hot_and_copert_cold_config.yaml`` in the folder
    ``example/example_configs/``. They contain example configurations
    for the ``HbefaStrategy`` and may help you to understand how the ``HbefaStrategy`` can be used.

hot emissions
-------------
The ``HbefaHotStrategy`` is used to calculate hot emissions.

cold emissions
--------------
By default the ``HbefaColdStrategy`` is used to calculate cold emissions. In the config file the argument
``cold_strategy`` may be used to specify the path to a different Strategy. If a ``cold_strategy`` is
given in the config file it will be used instead of the ``HbefaColdStrategy``. Note that cold emissions are only
calculated if the config argument ``only_hot`` is not set to True.

A note on the data loading process
----------------------------------

The conversion of berlin_format data to yeti_format data is conducted independently for the hot
and the cold Strategies. This is done to keep the dependencies between the hot and cold Strategies
to a minimum. It enables the ``HbefaStrategy`` to work with any cold Strategy you want.

The consequence is that some computations may be done twice, because they are done by both
the hot and the cold ``load_berlin_format_data_function`` s. The constructed yeti_format files
will be in two subfolders of the output folder (the output folder is specified in the config file).

Data Requirements
-----------------
The data required for the ``HbefaHotStrategy`` is required for the ``HbefaStrategy`` in all cases.

If ``only_hot`` is set to ``no`` or not given in the config file additional data is required depending on
the config argument ``cold_strategy``:

- The argument ``cold_strategy`` is not given in the config file. Then the data required for the
  ``CopertColdStrategy`` is also required.
- The argument ``cold_strategy`` is given in the config file. Then the data required for the given ``cold_strategy`` is also required.

What to put in the config.yaml
------------------------------
If you want to use the ``HbefaStrategy`` for your calculations, you need to set the following options
in your config.yaml. Don’t forget to add the parameters specified here: :doc:`Configuring YETI <config>`

If using mode ``berlin_format``:
''''''''''''''''''''''''''''''''

.. code-block:: yaml

    mode:                             berlin_format
    strategy:                         code.hbefa_strategy.HbefaStrategy.HbefaStrategy
    load_berlin_format_data_function: code.hbefa_strategy.load_berlin_format_data.load_hbefa_berlin_format_data
    load_yeti_format_data_function:   code.hbefa_strategy.load_yeti_format_data.load_hbefa_yeti_format_data

    only_hot:           no  # or yes. Default is no

    [..]  # add the file locations for the data required by the HbefaHotStrategy

    # if only_hot is yes, the following arguments may be omitted.
    cold_strategy:                         path.to.ColdStrategy
    cold_load_berlin_format_data_function: path.to.load_berlin_format_data_function.for.cold_strategy
    cold_load_yeti_format_data_function:   path.to.load_yeti_format_data_function.for.cold_strategy

    [..]  # add the file locations of any additional files needed for the cold_strategy
    [..]  # add any additional args that you want to pass to the cold_strategy


If using mode ``yeti_format``:
'''''''''''''''''''''''''''''''

.. code-block:: yaml

    mode:                           yeti_format
    strategy:                       code.copert_strategy.HbefaStrategy.HbefaStrategy
    load_yeti_format_data_function: code.hbefa_strategy.load_yeti_format_data.load_hbefa_yeti_format_data

    only_hot:           no  # or yes. Default is no

    [..]  # add the file locations for the data required by the HbefaHotStrategy

    # if only_hot is yes, the following arguments may be omitted.
    cold_strategy:                       path.to.ColdStrategy
    cold_load_yeti_format_data_function: path.to.load_yeti_format_data_function.for.cold_strategy

    [..]  # add the file locations of any additional files needed for the cold_strategy
    [..]  # add any additional args that you want to pass to the cold_strategy


How to deal with naming conflicts
'''''''''''''''''''''''''''''''''
Naming conflicts between the config arguments for the hot Strategy and the arguments for the
cold Strategy are an issue that you will certainly encounter. For example ``berlin_format_emission_factors`` is a config argument
for the ``HbefaHotStrategy`` and for the ``HbefaColdStrategy``, however the two Strategies require input data
in a different format. How do we deal with this issue when we want to use the ``HbefaColdStrategy`` to
calculate cold emissions with the ``HbefaStrategy``?

We solve this naming issue by prefixing the argument that should go to the hot Strategy with ``hot_[..]``.
The argument that should go to the cold Strategy is prefixed with ``cold_[..]``.

In our example for ``berlin_format_emission_factors`` we would add these lines to the config:

.. code-block:: yaml

    hot_berlin_format_emission_factors:    path/to/ef_data_for_hot_strategy.csv
    cold_berlin_format_emission_factors:   path/to/ef_data_for_cold_strategy.csv

If the two Strategies require the same config argument, there is no need to add prefixes. For example the config argument
``berlin_format_link_data`` is required for the ``HbefaHotStrategy`` and the ``HbefaColdStrategy``. However both
Strategies require the exact same data. Therefore it is sufficient to specify it once:

.. code-block:: yaml

    berlin_format_link_data:               path/to/berlin_format_link_data.csv

A note on the validation_function
'''''''''''''''''''''''''''''''''
We currently don't provide a dedicated validation function for this Strategy.
If you are only calculating hot emissions (set ``only_hot: yes`` in the config file)
you can use the validation function for the ``HbefaHotStrategy``.


Output
------
The output of this Strategy depends on the config arguments. There are three cases:

1. ``only_hot`` is set to True. Then the output is the same as for the ``HbefaHotStrategy``.
2. ``only_hot`` is not set to True and no ``cold_strategy`` is given in the config file.
   Then the output consists of the files generated by the ``HbefaHotStrategy``
   (prefixed with ``hot_[..]``) and the files produced by the ``HbefaColdStrategy`` (prefixed with ``cold_[..]``).
3. ``only_hot`` is not set to True and a ``cold_strategy`` is given in the config file.
   Then the output consists of the files generated by the ``HbefaHotStrategy``
   (prefixed with ``hot_[..]``) and the files produced by the ``cold_strategy`` (prefixed with ``cold_[..]``).
