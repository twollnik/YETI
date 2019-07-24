Welcome to YETI - Yet Another Emissions From Traffic Inventory's documentation!
===============================================================================

YETI is a tool for street level bottom-up traffic emission calculation. It helps you create high-resolution
traffic emission inventories.

YETI supports common emission calculation methodologies like COPERT or HBEFA. The methodologies
are implemented as :ref:`Strategies <what-is-strategy>`. You can select which Strategy to use for a model run
in the :ref:`configuration file <config>`.

YETI was originally built for the City of Berlin, but is flexible enough to be adopted to different datasets.
Find out how to customize YETI for your needs in the developer section. Start here: :ref:`Process`

The code for YETI can be found on `GitHub <https://github.com/twollnik/YETI/>`_.

.. toctree::
   :maxdepth: 1
   :caption: User Documentation

   user/installation_setup
   user/demo
   user/usage
   user/config
   user/data_formats
   user/output_format
   user/what_is_strategy
   user/copert_strategy
   user/copert_hot_strategy
   user/copert_hot_strategy_fixed_speed
   user/copert_cold_strategy
   user/hbefa_hot_strategy
   user/pm_non_exhaust_strategy

.. toctree::
   :maxdepth: 1
   :caption: Developer Documentation

   developer/hard_coding
   developer/high_level_how_does_it_work
   developer/add_strategy
   developer/add_validate_function
   developer/add_load_berlin_format_data_function
   developer/add_load_yeti_format_data_function
   developer/update_docs
   developer/contributing
