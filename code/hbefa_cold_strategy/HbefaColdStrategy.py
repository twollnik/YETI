from typing import Dict, Any, List, Tuple
import collections


class HbefaColdStrategy:

    def __init__(self):

        self.cold_start_ef_for_vehicle_and_pollutant = {}  # type: Dict[Tuple[str,str], float]
        self.emissions = collections.defaultdict(dict)

    def calculate_emissions(self,
                            cold_starts_and_link_data_row: Dict[str, Any],
                            vehicle_dict: Dict[str, str],
                            pollutants: List[str],
                            **kwargs):

        self.initialize_if_necessary(**kwargs)
        self.delete_emissions_from_last_call_to_this_function()

        for pollutant in pollutants:
            for vehicle_name in vehicle_dict.keys():
                self.calculate_emissions_for_vehicle(
                    cold_starts_and_link_data_row, vehicle_name, pollutant)

        return self.emissions

    def initialize_if_necessary(self, **kwargs):

        if self.is_not_initialized():
            self.initialize(**kwargs)

    def is_not_initialized(self):

        return self.cold_start_ef_for_vehicle_and_pollutant == {}

    def initialize(self, **kwargs):

        for _, row in kwargs["emission_factor_data"].iterrows():
            self.cold_start_ef_for_vehicle_and_pollutant[(row["VehicleName"], row["Pollutant"])] = row["EmissionsPerStart"]

    def delete_emissions_from_last_call_to_this_function(self):

        self.emissions = collections.defaultdict(dict)

    def calculate_emissions_for_vehicle(self,
                                        cold_starts_and_link_data_row: Dict[str, Any],
                                        vehicle_name: str,
                                        pollutant: str):

        starts_for_the_given_vehicle = cold_starts_and_link_data_row[vehicle_name]
        emissions_per_cold_start_for_the_given_vehicle = self.cold_start_ef_for_vehicle_and_pollutant[(vehicle_name, pollutant)]

        emissions = starts_for_the_given_vehicle * emissions_per_cold_start_for_the_given_vehicle

        self.emissions[pollutant][vehicle_name] = emissions
