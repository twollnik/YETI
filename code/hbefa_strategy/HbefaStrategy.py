from typing import Any, Dict, List

from code.copert_strategy.CopertStrategy import CopertStrategy
from code.hbefa_cold_strategy.HbefaColdStrategy import HbefaColdStrategy
from code.hbefa_hot_strategy.HbefaHotStrategy import HbefaHotStrategy
from code.script_helpers.dynamic_import_from import dynamic_import_from
from code.strategy_helpers.helpers import remove_prefix_from_keys


class HbefaStrategy(CopertStrategy):

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
