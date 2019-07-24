"""
CopertStrategy

This module provides an interface to calculate hot and (optionally) cold emissions.

Regarding the hot emissions:
The Copert methodology for hot emissions is used to calculate hot emissions. The CopertStrategy relies
on other Strategies to do the actual calculation. By default it uses the CopertHotStrategy.
If the config argument 'fixed_speed' is set to True, the CopertHotFixedSpeedStrategy is used to
calculate hot emissions using fixed speeds.

Regarding the cold emissions:
By default the CopertColdStrategy is used to calculate cold emissions. In the config file the argument
'cold_strategy' may be used to specify the path to a different Strategy. If a cold_strategy is
given in the config file it will be used instead of the CopertColdStrategy. Note that cold emissions are only
calculated if the config argument 'only_hot' is not set to True.

Possible config arguments:
- only_hot (Calculate only hot emissions. Don't calculate cold emissions.)
- fixed_speed (Use the CopertHotFixedSpeedStrategy instead of the CopertHotStrategy to calculate hot emissions.)
- cold_strategy (Path to a Strategy class to be used for the cold emission calculation. Defaults to CopertColdStrategy.)

Output
The output of this Strategy depends on the config arguments. There are three cases:
1. only_hot is set to True. Then the output is the same as for the CopertStrategy or the CopertHotFixedSpeedStrategy.
2. only_hot is not set to True and no cold_strategy is given in the config. Then the output is the same as for the
   CopertColdStrategy.
3. only_hot is not set to True and a cold_strategy is given in the config. Then the output consists of the files
   generated by the CopertHotStrategy or CopertHotFixedSpeedStrategy (prefixed with 'hot_') and the files produced
   by the cold_strategy (prefixed with 'cold_').
"""
from typing import Any, Dict, List

from code.copert_cold_strategy.CopertColdStrategy import CopertColdStrategy
from code.copert_hot_fixed_speed_strategy.CopertHotFixedSpeedStrategy import CopertHotFixedSpeedStrategy
from code.copert_hot_strategy.CopertHotStrategy import CopertHotStrategy
from code.copert_strategy.copert_helpers import remove_prefix_from_keys, add_prefix_to_keys, drop_keys_starting_with
from code.script_helpers.dynamic_import_from import dynamic_import_from


class CopertStrategy:
    """
    Calculates hot and (optionally) cold emissions focusing on calculation with the copert methodology.

    Attributes
    ----------
    hot_strategy
        The Strategy used to calculate hot emissions. Defaults to CopertHotStrategy. If 'fixed_speed'
        is set to True in the config file, CopertHotFixedSpeedStrategy is used as hot_strategy.
    cold_strategy
        The Strategy used to calculate cold emissions. Defaults to CopertColdStrategy. If 'cold_strategy'
        is set in the config file, the Strategy specified there is used as cold_strategy to
        calculate cold emissions.

    Methods
    -------
    calculate_emissions
        The main interface for this Strategy. calculate_emissions is called over and over during
        a model run. Its job is to take a single traffic row (and some other parameters) and output
        a single emissions row for each pollutant.
    """

    def __init__(self):

        self.hot_strategy = None
        self.cold_strategy = None

    def calculate_emissions(self,
                            traffic_and_link_data_row: Dict[str, Any],
                            vehicle_dict: Dict[str, str],
                            pollutants: List[str],
                            **kwargs):

        self.initialize_if_necessary(**kwargs)

        if kwargs.get("only_hot") is True:
            return self.hot_strategy.calculate_emissions(
                traffic_and_link_data_row, vehicle_dict, pollutants, **kwargs)

        if "cold_strategy" in kwargs:
            hot_emissions = self.calculate_hot_emissions(traffic_and_link_data_row, vehicle_dict, pollutants, **kwargs)
            cold_emissions = self.calculate_cold_emissions(traffic_and_link_data_row, vehicle_dict, pollutants, kwargs)
            return {**hot_emissions, **cold_emissions}

        if kwargs.get("fixed_speed") is True:
            kwargs["hot_strategy"] = "code.copert_hot_fixed_speed_strategy.CopertHotFixedSpeedStrategy.CopertHotFixedSpeedStrategy"
        return self.cold_strategy.calculate_emissions(
            traffic_and_link_data_row, vehicle_dict, pollutants, **kwargs)

    def initialize_if_necessary(self, **kwargs):

        if self.hot_strategy is None or self.cold_strategy is None:

            if kwargs.get("fixed_speed") is True:
                self.hot_strategy = CopertHotFixedSpeedStrategy()
            else:
                self.hot_strategy = CopertHotStrategy()

            if "cold_strategy" in kwargs:
                self.cold_strategy = dynamic_import_from(kwargs["cold_strategy"])()
            else:
                self.cold_strategy = CopertColdStrategy()

    def calculate_hot_emissions(self, traffic_and_link_data_row, vehicle_dict, pollutants, **kwargs):

        kwargs_for_hot = drop_keys_starting_with("cold_", kwargs)
        kwargs_for_hot = remove_prefix_from_keys("hot_", kwargs_for_hot)

        hot_emissions = self.hot_strategy.calculate_emissions(
            traffic_and_link_data_row, vehicle_dict, pollutants, **kwargs_for_hot)

        hot_emissions = add_prefix_to_keys("hot", hot_emissions)

        return hot_emissions

    def calculate_cold_emissions(self, traffic_and_link_data_row, vehicle_dict, pollutants, kwargs):

        kwargs_for_cold = drop_keys_starting_with("hot_", kwargs)
        kwargs_for_cold = remove_prefix_from_keys("cold_", kwargs_for_cold)

        cold_emissions = self.cold_strategy.calculate_emissions(
            traffic_and_link_data_row, vehicle_dict, pollutants, **kwargs_for_cold)

        cold_emissions = add_prefix_to_keys("cold", cold_emissions)

        return cold_emissions
