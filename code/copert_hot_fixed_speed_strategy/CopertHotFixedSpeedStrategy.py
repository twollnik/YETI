"""
CopertHotFixedSpeedStrategy

This module implements emission calculation with the COPERT methodology for hot emissions.
It uses speed-dependent emission factors based on eather
- a fixed speed given in the configuration file or
- a fixed speed for each link given in the link data
"""
from typing import Any, Dict

from code.copert_hot_strategy.CopertHotStrategy import CopertHotStrategy


class CopertHotFixedSpeedStrategy(CopertHotStrategy):
    """
        Calculates hot emissions for fixed speeds using the COPERT methodology.

        Attributes
        ----------
        ef_dict : Dict
            Holds emission factor data in the format ``(VehicleName, Pollutant, Slope, Load) ->
                {'Alpha': .., 'Beta': .., ...}``
        emissions : Dict
            Contains emission values and is used to assemble the output of ``calculate_emissions``.

        Methods
        -------
        calculate_emissions
            The main interface for this Strategy. calculate_emissions is called over and over during
            a model run. Its job is to take a single traffic row (and some other parameters) and output
            a single emissions row.

        """

    def __init__(self, **kwargs):

        ef_data = kwargs.get("emission_factor_data")
        if ef_data is not None:
            self.ef_dict = self.get_ef_dict(ef_data)

        self.emissions = {}

    def calculate_emissions(self,
                            traffic_and_link_data_row: Dict[str, Any],
                            vehicle_dict: Dict[str, str],
                            pollutant: str,
                            **kwargs):

        self.initialize_if_necessary(kwargs)
        self.delete_emissions_from_last_call_to_this_function()

        for vehicle_name, vehicle_category in vehicle_dict.items():
            self.calculate_emissions_for_vehicle(
                traffic_and_link_data_row, vehicle_name, vehicle_category, pollutant, **kwargs)

        return self.emissions

    def initialize_if_necessary(self, kwargs):

        if hasattr(self, "ef_dict") is False:
            self.__init__(**kwargs)

    def delete_emissions_from_last_call_to_this_function(self):

        self.emissions = {}

    def calculate_emissions_for_vehicle(
            self, traffic_and_link_data_row, vehicle_name, vehicle_category, pollutant, **kwargs):
        """ Calculate emissions for the given vehicle_name.

        This function will set self.emissions[vehicle_name] to the
        emissions value for vehicle_name.
        """

        ef_dict_for_vehicle = self.get_ef_dict_for_vehicle(vehicle_name, pollutant)

        # if "v" is given in config, use "v". If not, use the "Speed" from the given row.
        speed = float(kwargs.get("v", traffic_and_link_data_row.get("Speed")))

        max_speed, min_speed = float(ef_dict_for_vehicle["MaxSpeed"]), float(ef_dict_for_vehicle["MinSpeed"])
        if speed > max_speed:
            speed = max_speed
        elif speed < min_speed:
            speed = min_speed

        ef = self.calculate_ef_copert(speed, ef_dict_for_vehicle)

        emissions = ef * float(traffic_and_link_data_row["Length"]) * float(traffic_and_link_data_row[vehicle_name])

        self.emissions[vehicle_name] = emissions
