from typing import Any, Dict, List

from code.copert_cold_strategy.CopertColdStrategy import CopertColdStrategy
from code.copert_hot_strategy.CopertHotStrategy import CopertHotStrategy
from code.copert_strategy.copert_helpers import remove_prefix_from_keys, add_prefix_to_keys, drop_keys_starting_with
from code.script_helpers.dynamic_import_from import dynamic_import_from


class CopertStrategy:

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

            return {
                **hot_emissions,
                **cold_emissions
            }

        return self.cold_strategy.calculate_emissions(
            traffic_and_link_data_row, vehicle_dict, pollutants, **kwargs)

    def initialize_if_necessary(self, **kwargs):

        if self.hot_strategy is None or self.cold_strategy is None:
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
