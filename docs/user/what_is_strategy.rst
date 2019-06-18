.. _what-is-strategy:

What is a Strategy?
===================

A Strategy implements a specific methodology/algorithm for calculating traffic emissions.
For example the ``CopertHotStrategy`` implements emission calculation with the COPERT methodology for hot emissions.

Each model run uses a specific Strategy to calculate emissions. Almost all configuration parameters are dependent on
the Strategy used. For instance the data requirements are different for all Strategies and most Strategies need
additional configuration parameters.

The use of Strategies makes it easy to extend YETI and include new ways of calculating emissions. If you
want to use a custom Strategy, look :ref:`here <add-strategy>`.

List of Strategies
------------------

Take a look at the individual Strategy pages for further details.

   - :doc:`copert_cold_strategy`
   - :doc:`copert_hot_strategy`
   - :doc:`copert_hot_strategy_fixed_speed`
   - :doc:`hbefa_hot_strategy`
   - :doc:`pm_non_exhaust_strategy`
