How to support more pollutants, area types, ...
===============================================

There are some restrictions on the data requirements:

1. The number of supported pollutants is quite small.
2. There can only be two directions and two area types in the link data: R/L and 0/1 respectively.
3. There are four day types: 1,2,3,7.
4. The number of vehicle types is limited and their names are set.

These restrictions are in place because of the hard-coding of some values in the conversion from berlin_format
to yeti_format. Also some Strategies use hard-coded values. Most Strategies don't use hard-coded values.

These are the Strategies that don't use hard-coded values:

- CopertHotStrategy
- CopertHotFixedSpeedStrategy
- HbefaColdStrategy
- PMNonExhaustStrategy

These Strategies use hard-coded values:

- HbefaHotStrategy: uses hard-coded values for road types and area types.
- CopertColdStrategy: uses hard-coded values for pollutant types and vehicle categories.

The following sections describe how to circumvent the restrictions outlined above.

If you are using the mode ``berlin_format``:
Write your own ``load_berlin_data_function`` that does not enforce the restrictions. The function should convert
your data to ``yeti_format``. Make sure that the data in ``yeti_format`` is complete and coherent.
Look here for more information: :doc:`add_load_berlin_format_data_function`

If you are using mode ``yeti_format``:
You don't need to write a new ``load_berlin_data_function``.

This should be sufficient for the Strategies that don't use hard coding, as listed above. If you want to work with a Strategy
that uses hard-coding, some additional steps may be required:

- If your data does not conflict with the hard-coded values nothing else needs to be done. Refer to the list above
  to see which values are hard-coded in the Strategies. For example if you want to use different vehicle categories,
  you don't need to change the HbefaHotStrategy (it only uses hard-coded values for road and area types, not for
  vehicle categories). You would have to change the CopertColdStrategy.
- If your data does conflict with the hard-coded values you need to change the Strategy. How exactly you need to change
  the Strategy depends on the exact format of the data you want to use.
