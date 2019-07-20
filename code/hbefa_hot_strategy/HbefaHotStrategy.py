"""
HbefaHotStrategy

This Module implements emission calculation with the HBEFA methodology for hot exhaust emissions.
It works with emission factors that are dependent on the vehicle and the traffic situation.
"""
from typing import Any, Dict, List
import collections

from code.constants.mappings import ROAD_CAT_FROM_ENUM


class HbefaHotStrategy:
    """
    Calculates hot emissions using the HBEFA methodology.

    Attributes
    ----------
    ef_dict : Dict
       Holds emission factor data in the format ``(Pollutant, TrafficSituation, VehicleName) -> emission factor
       E.g. ("PollutantType.NOx", "URB/MW-City/100/Freeflow", "PC petrol <1.4L Euro-1"): 0.76
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

        self.ef_dict = None
        self.emissions = collections.defaultdict(dict)

    def calculate_emissions(self,
                            traffic_and_link_data_row: Dict[str, Any],
                            vehicle_dict: Dict[str, str],
                            pollutants: List[str],
                            **kwargs):

        self.initialize_if_necessary(**kwargs)
        self.delete_emissions_from_last_call_to_this_function()

        traffic_situation = self.get_traffic_situation(traffic_and_link_data_row)

        for pollutant in pollutants:
            for vehicle_name in vehicle_dict.keys():
                self.calculate_emissions_for_vehicle(
                    traffic_and_link_data_row, vehicle_name, traffic_situation, pollutant, **kwargs)

        return self.emissions

    def initialize_if_necessary(self, **kwargs):

        if self.is_not_initialized():
            self.initialize_ef_data(kwargs)

    def is_not_initialized(self):

        return self.ef_dict is None

    def initialize_ef_data(self, kwargs):

        ef_data = kwargs.get("emission_factor_data")
        self.ef_dict = {
            (row["Pollutant"], row["TrafficSituation"], row["VehicleName"]): row["EF"]
            for _, row in ef_data.iterrows()
        }

    def delete_emissions_from_last_call_to_this_function(self):

        self.emissions = collections.defaultdict(dict)

    def get_traffic_situation(self, row) -> str:

        road_type_hbefa = ROAD_CAT_FROM_ENUM[row["RoadType"]]
        area_type_hbefa = "URB" if row["AreaType"] == "AreaType.Urban" else "RUR"

        return f"{area_type_hbefa}/{road_type_hbefa}/{row['MaxSpeed']}"

    def calculate_emissions_for_vehicle(self, traffic_and_link_data_row, vehicle_name, traffic_situation, pollutant,
                                        **kwargs):

        efs_for_los_types = [
            float(self.ef_dict[(pollutant, f"{traffic_situation}/Freeflow", vehicle_name)]),
            float(self.ef_dict[(pollutant, f"{traffic_situation}/Heavy", vehicle_name)]),
            float(self.ef_dict[(pollutant, f"{traffic_situation}/Satur.", vehicle_name)]),
            float(self.ef_dict[(pollutant, f"{traffic_situation}/St+Go", vehicle_name)])
        ]

        ef = 0
        for los_perc_col, ef_for_los in zip(
                ["LOS1Percentage", "LOS2Percentage", "LOS3Percentage", "LOS4Percentage"],
                efs_for_los_types):
            ef += traffic_and_link_data_row[los_perc_col] * ef_for_los

        emissions = ef * traffic_and_link_data_row["Length"] * traffic_and_link_data_row[vehicle_name]
        self.emissions[pollutant][vehicle_name] = emissions
