"""
HbefaStrategy

This module provides an interface to calculate hot and (optionally) cold emissions.

Regarding the hot emissions:
The Hbefa methodology for hot emissions is used to calculate hot emissions. The HbefaStrategy relies
on other Strategies to do the actual calculation. By default it uses the HbefaHotStrategy.

Regarding the cold emissions:
By default the HbfeaColdStrategy is used to calculate cold emissions. In the config file the argument
'cold_strategy' may be used to specify the path to a different Strategy. If a cold_strategy is
given in the config file it will be used instead of the CopertColdStrategy. Note that cold emissions are only
calculated if the config argument 'only_hot' is not set to True.

Possible config arguments:
- only_hot (Calculate only hot emissions. Don't calculate cold emissions.)
- cold_strategy (Path to a Strategy class to be used for the cold emission calculation. Defaults to HbefaColdStrategy.)

Output
The output of this Strategy depends on the config arguments. There are three cases:
1. only_hot is set to True. Then the output is the same as for the HbefaHotStrategy.
2. only_hot is not set to True and no cold_strategy is given in the config. Then the output consists of the
   output from the HbefaHotStrategy (prefixed with 'hot_') and the output from the HbefaColdStrategy
   (prefixed with 'cold_').
3. only_hot is not set to True and a cold_strategy is given in the config. Then the output consists of the files
   generated by the HbefaHotStrategy (prefixed with 'hot_') and the files produced by the cold_strategy
   (prefixed with 'cold_').
"""
from typing import Any, Dict, List

from code.copert_strategy.CopertStrategy import CopertStrategy
from code.hbefa_cold_strategy.HbefaColdStrategy import HbefaColdStrategy
from code.hbefa_hot_strategy.HbefaHotStrategy import HbefaHotStrategy
from code.script_helpers.dynamic_import_from import dynamic_import_from
from code.strategy_helpers.helpers import remove_prefix_from_keys


class HbefaStrategy(CopertStrategy):
    """
    Calculates hot and (optionally) cold emissions focusing on calculation with the hbefa methodology.

    Attributes
    ----------
    hot_strategy
        A HbefaHotStrategy instance. It is used to calculate hot emissions.
    cold_strategy
        The Strategy used to calculate cold emissions. Defaults to HbefaColdStrategy. If 'cold_strategy'
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

        self.hot_strategy = HbefaHotStrategy()
        self.cold_strategy = None

    def calculate_emissions(self,
                            traffic_and_link_data_row: Dict[str, Any],
                            vehicle_dict: Dict[str, str],
                            pollutants: List[str],
                            **kwargs):

        self.initialize_cold_strategy_if_necessary(**kwargs)

        if kwargs.get("only_hot") is True:
            kwargs = remove_prefix_from_keys("hot_", kwargs)
            return self.hot_strategy.calculate_emissions(traffic_and_link_data_row, vehicle_dict, pollutants, **kwargs)

        hot_emissions = self.calculate_hot_emissions(traffic_and_link_data_row, vehicle_dict, pollutants, **kwargs)
        cold_emissions = self.calculate_cold_emissions(traffic_and_link_data_row, vehicle_dict, pollutants, kwargs)
        return {**hot_emissions, **cold_emissions}

    def initialize_cold_strategy_if_necessary(self, **kwargs):

        if self.cold_strategy is None:
            if "cold_strategy" in kwargs:
                self.cold_strategy = dynamic_import_from(kwargs["cold_strategy"])()
            else:
                self.cold_strategy = HbefaColdStrategy()