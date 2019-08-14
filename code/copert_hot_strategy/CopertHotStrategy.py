"""
CopertHotStrategy

This module implements emission calculation with the COPERT methodology for hot emissions.
It uses speed-dependent emission factors based on
- each street link's attributes (road type, area type, and maximum speed),
- the los percentages and
- the los speeds attributed to the links.
"""
from typing import Any, Dict, List
import collections

import pandas as pd


class CopertHotStrategy:
    """
    Calculates hot emissions using the COPERT methodology.

    Attributes
    ----------
    los_speeds_dict : Dict
        Holds los speeds data in the format ``(LinkID, VehicleCategory) ->
            {'LOS1Speed': .., LOS2Speed': .., LOS3Speed': .., LOS4Speed': ..}``
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
        a single emissions row for each pollutant.

    """

    def __init__(self, **kwargs):

        self.los_speeds_dict = None
        self.ef_dict = None

        self.emissions = collections.defaultdict(dict)

    def calculate_emissions(self,
                            traffic_and_link_data_row: Dict[str, Any],
                            vehicle_dict: Dict[str, str],
                            pollutants: List[str],
                            **kwargs):

        self.initialize_if_necessary(kwargs)
        self.delete_emissions_from_last_call_to_this_function()

        for pollutant in pollutants:
            for vehicle_name, vehicle_category in vehicle_dict.items():
                self.calculate_emissions_for_vehicle(
                    traffic_and_link_data_row, vehicle_name, vehicle_category, pollutant, **kwargs)

        return self.emissions

    def initialize_if_necessary(self, kwargs):

        if self.is_not_initialized():
            self.initialize(**kwargs)

    def is_not_initialized(self):

        return self.los_speeds_dict is None or self.ef_dict is None

    def initialize(self, **kwargs):

        los_speeds_data = kwargs["los_speeds_data"]
        ef_data = kwargs["emission_factor_data"]

        self.los_speeds_dict = self.get_los_speeds_dict(los_speeds_data)
        self.ef_dict = self.get_ef_dict(ef_data)

    def get_los_speeds_dict(self, los_speeds_data):

        return los_speeds_data.set_index(["LinkID", "VehicleCategory"]).to_dict(orient="index")

    def get_ef_dict(self, ef_data: pd.DataFrame):

        ef_data[["Slope", "Load"]] = ef_data[["Slope", "Load"]].fillna(0.0)
        return{
            (row["VehicleName"], row["Pollutant"], row["Slope"], row["Load"]): row.to_dict()
            for _, row in ef_data.iterrows()
        }

    def delete_emissions_from_last_call_to_this_function(self):

        self.emissions = collections.defaultdict(dict)

    def calculate_emissions_for_vehicle(
            self, traffic_and_link_data_row, vehicle_name, vehicle_category, pollutant, **kwargs):
        """ Calculate emissions for the given vehicle_name.

        This function will set self.emissions[vehicle_name] to the
        emissions value for vehicle_name.
        """

        los_speeds = self.los_speeds_dict[(traffic_and_link_data_row["LinkID"], vehicle_category)]

        ef = self.get_ef(traffic_and_link_data_row, vehicle_name, pollutant, los_speeds)
        link_length = float(traffic_and_link_data_row["Length"])
        vehicle_count = traffic_and_link_data_row[vehicle_name]
        emissions = ef * link_length * vehicle_count

        self.emissions[pollutant][vehicle_name] = emissions

    def get_ef(self, row: Dict[str, Any], vehicle_name: str, pollutant: str, los_speeds: Dict[str, float]) -> float:

        ef_from_config = row.get("EF")
        if pd.isna(ef_from_config) is False and ef_from_config is not None:
            return ef_from_config
        return self.get_ef_copert(row, vehicle_name, pollutant, los_speeds)

    def get_ef_copert(self, row: Dict[str, Any], vehicle_name: str, pollutant: str, los_speeds: Dict[str, float]) -> float:

        efs_for_los = []
        ef_dict_for_vehicle = self.get_ef_dict_for_vehicle(vehicle_name, pollutant)
        max_speed, min_speed = float(ef_dict_for_vehicle["MaxSpeed"]), float(ef_dict_for_vehicle["MinSpeed"])

        for los_speed_col in ["LOS1Speed", "LOS2Speed", "LOS3Speed", "LOS4Speed"]:

            speed = float(los_speeds[los_speed_col])
            if speed > max_speed:
                speed = max_speed
            elif speed < min_speed:
                speed = min_speed

            ef_for_speed = self.calculate_ef_copert(speed, ef_dict_for_vehicle)
            efs_for_los.append(ef_for_speed)

        los_weighted_speed_dependant_ef = 0

        for los_perc_col, ef in zip(["LOS1Percentage", "LOS2Percentage", "LOS3Percentage", "LOS4Percentage"],
                                    efs_for_los):
            los_weighted_speed_dependant_ef += float(row[los_perc_col]) * ef

        return los_weighted_speed_dependant_ef

    def get_ef_dict_for_vehicle(self, vehicle_name: str, pollutant: str) -> Dict[str, float]:
        
        # If you ever want to use load or slope values other than zero, include the following line of code.
        # Also make sure that load and slope are input arguments to this function.
        #
        # return self.ef_dict[(vehicle_name, pollutant, slope, load)]
        
        return self.ef_dict[(vehicle_name, pollutant, 0.0, 0.0)]

    def calculate_ef_copert(self, speed: float, concrete_ef_dict: Dict[str, float]) -> float:

            numerator = (
                    float(concrete_ef_dict["Alpha"]) * speed ** 2
                    + float(concrete_ef_dict["Beta"]) * speed
                    + float(concrete_ef_dict["Gamma"])
                    + float(concrete_ef_dict["Delta"]) / speed
            )
            denominator = (
                    float(concrete_ef_dict["Epsilon"]) * speed ** 2
                    + float(concrete_ef_dict["Zita"]) * speed
                    + float(concrete_ef_dict["Hta"])
            )
            reduction_factor = float(concrete_ef_dict["ReductionPerc"])
            ef = numerator / denominator * (1 - reduction_factor)
            return ef

