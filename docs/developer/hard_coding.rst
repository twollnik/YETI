How to support more pollutants, area types, ...
===============================================

About
-----

The docs impose a lot of restrictions on the input data. For example:

1. The number of supported pollutants is quite small.
2. There can only be two directions and two area types in the link data: R/L and 0/1 respectively.
3. There are four day types: 1,2,3,7.
4. The number of vehicle types is limited and their names are set.

This page covers how to work around these restrictions to make YETI work with your data.

Where do restrictions exist?
----------------------------

The restrictions for the input data are in place because some values are hard-coded. This applies to 

- The conversion from berlin_format to yeti_format data for all Strategies.
- Some strategies use hard-coded values for the calculation step, thus imposing restrictions on 
  the input data. Most Strategies  don't.

Below are the Strategies that don't impose any restrictions on the input data *for the calculation step*. 
Remember that these Strategies still impose restrictions when it comes to converting berlin_format data to yeti_format data.

- CopertHotStrategy
- CopertHotFixedSpeedStrategy
- HbefaColdStrategy
- PMNonExhaustStrategy

The following Strategies impose some restrictions on the input data for the calculation step:

- HbefaHotStrategy: Possible road types and area types are hard-coded. 
  Refer to the docs page for HbefaHotStrategy for more.
- CopertColdStrategy: Possible pollutant types and vehicle categories are hard-coded. 
  Refer to the docs page for CopertColdStrategy for more.

How to work around the restrictions
-----------------------------------

If you want to work with data in ``berlin_format`` you will have to write your own ``load_berlin_data_function`` 
that does not enforce the restrictions. The function should convert
your data to ``yeti_format``. Make sure that the data in ``yeti_format`` is complete and coherent.
Look here for more information: :doc:`add_load_berlin_format_data_function`

If you are already working with data in yeti_format you don't need to write new data loading functions.

This should be sufficient for the Strategies that enforce restrictions for the calculation step, as listed above. 
If you want to work with a Strategy that does enforce restrictions for the calculation step, you may need
to take additional action:

- If your data does not conflict with the hard-coded values nothing else needs to be done. Refer to the list above
  to see which values are hard-coded in the Strategies. For example if you want to use different vehicle categories,
  you don't need to change the HbefaHotStrategy (it only uses hard-coded values for road and area types, not for
  vehicle categories). 
- If your data does conflict with the hard-coded values you need to change code for the Strategy. How exactly you need to change
  the Strategy depends on the exact format of the data you want to use.
