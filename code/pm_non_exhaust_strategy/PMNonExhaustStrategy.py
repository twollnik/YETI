"""
PMNonExhaustStrategy

This module implements emission calculation for PM from non-exhaust emissions.
Sources for PM non-exhaust emissions are tyre wear, brake wear and road surface emissions.
"""
from typing import Any, Dict, Iterable, Tuple, List

from code.Strategy import Strategy


class PMNonExhaustStrategy(Strategy):
    """
    Calculates PM non-exhaust emissions.

    Output of this Strategy are three datasets. One with total suspended particles (TSP), one
    with PM10 emissions, and one with PM25 emissions.

    The Strategy will calculate TSP, PM10, and PM25 emissions independently for tyre wear, brake wear,
    and road surface emissions. Then it will add up the emissions from all sources to obtain total
    PM non-exhaust emissions for TSP, PM10, and PM25.

    Attributes
    ----------
    los_speeds_dict : Dict
        Holds los speeds data in the format ``(LinkID, VehicleCategory) ->
            {'LOS1Speed': .., LOS2Speed': .., LOS3Speed': .., LOS4Speed': ..}``
    vehicle_dict : Dict
        Maps vehicle names to the corresponding vehicle category.
            E.g. "PC Petrol Euro-1": "VehicleCategory.PC"
    load_factor : float
        The load factor as specified in the configuration file.
    number_of_axles_per_vehicle : Dict
        Maps vehicle names to the corresponding number of axles.
            E.g. "RT >14-20t Euro-II": 4

    Methods
    -------
    calculate_emissions
        The main interface for this Strategy. calculate_emissions is called over and over during
        a model run. Its job is to take a single traffic row (and some other parameters) and output
        a single row of the TSP emissions data, the PM10 emissions data, and PM25 emissions data.
    """

    def __init__(self):

        self.vehicle_dict = None
        self.number_of_axles_per_vehicle = None
        self.load_factor = None
        self.los_speeds_dict = None

    def calculate_emissions(self,
                            traffic_and_link_data_row: Dict[str, Any],
                            vehicle_dict: Dict[str, str],
                            pollutants: List[str],
                            **kwargs) -> Dict[str, Dict[str, float]]:

        self.initialize_if_necessary(vehicle_dict, **kwargs)

        emissions = self.calculate_pm_non_exhaust_emissions_for_all_vehicles(traffic_and_link_data_row)
        emissions_in_right_output_format = self.reformat_emissions_to_right_output_format(emissions)

        return emissions_in_right_output_format

    def initialize_if_necessary(self, vehicle_dict: Dict[str, str], **kwargs):

        if self.is_not_initialized():
            self.initialize_load_factor(**kwargs)
            self.initialize_los_speeds_dict(**kwargs)
            self.initialize_vehicle_dict(vehicle_dict)
            self.initialize_number_of_axles_per_vehicle(**kwargs)

    def is_not_initialized(self):

        return any(
            att is None for att in [
                self.vehicle_dict, self.load_factor, self.los_speeds_dict, self.number_of_axles_per_vehicle
            ]
        )

    def initialize_load_factor(self, **kwargs):

        self.load_factor = kwargs["load_factor"]

    def initialize_los_speeds_dict(self, **kwargs):

        los_speeds_data = kwargs["los_speeds_data"]
        self.los_speeds_dict = los_speeds_data.set_index(["LinkID", "VehicleCategory"]).to_dict(orient="index")

    def initialize_vehicle_dict(self, vehicle_dict: Dict[str, str]):

        self.vehicle_dict = vehicle_dict

    def initialize_number_of_axles_per_vehicle(self, **kwargs):

        number_of_axles_per_vehicle_dict = {}
        vehicle_data = kwargs["vehicle_data"]

        for vehicle in self.vehicles():
            vehicle_data_row_for_vehicle = vehicle_data[vehicle_data["VehicleName"] == vehicle]
            num_axles_for_vehicle = vehicle_data_row_for_vehicle["NumberOfAxles"].item()
            number_of_axles_per_vehicle_dict[vehicle] = num_axles_for_vehicle

        self.number_of_axles_per_vehicle = number_of_axles_per_vehicle_dict


    def calculate_pm_non_exhaust_emissions_for_all_vehicles(
            self, traffic_and_link_data_row: Dict[str, Any]) -> Dict[str, Tuple[float, float, float]]:

        emissions_for_vehicles = {
            vehicle: self.calculate_emissions_for_vehicle(traffic_and_link_data_row, vehicle)
            for vehicle in self.vehicles()
        }
        return emissions_for_vehicles

    def calculate_emissions_for_vehicle(
            self, traffic_and_link_data_row: Dict[str, Any], vehicle: str) -> Tuple[float, float, float]:

        break_emissions = self.calculate_break_wear_emissions(vehicle, traffic_and_link_data_row)
        tyre_emissions = self.calculate_tyre_wear_emissions(vehicle, traffic_and_link_data_row)
        road_surface_emissions = self.calculate_road_surface_wear_emissions(vehicle, traffic_and_link_data_row)

        vehicle_emissions = self.add_emission_dicts(break_emissions, tyre_emissions, road_surface_emissions)
        vehicle_emissions_tuple = self.emissions_dict_to_tuple(vehicle_emissions)

        return vehicle_emissions_tuple

    def vehicles(self) -> Iterable[str]:
        return self.vehicle_dict.keys()

    def add_emission_dicts(
            self, dict1: Dict[str, float], dict2: Dict[str, float], dict3: Dict[str, float]) -> Dict[str, float]:

        return {
            "TSP": dict1["TSP"] + dict2["TSP"] + dict3["TSP"],
            "PM10": dict1["PM10"] + dict2["PM10"] + dict3["PM10"],
            "PM25": dict1["PM25"] + dict2["PM25"] + dict3["PM25"]
        }

    def emissions_dict_to_tuple(self, emissions_dict: Dict[str, float]) -> Tuple[float, float, float]:

        return (emissions_dict["TSP"], emissions_dict["PM10"], emissions_dict["PM25"])

    def reformat_emissions_to_right_output_format(
            self, emissions: Dict[str, Tuple[float, float, float]]) -> Dict[str, Dict[str, float]]:

        tsp_dict = {
            veh_name: values[0] for veh_name, values in emissions.items()
        }
        pm10_dict = {
            veh_name: values[1] for veh_name, values in emissions.items()
        }
        pm25_dict = {
            veh_name: values[2] for veh_name, values in emissions.items()
        }

        return {
            "TSP": tsp_dict,
            "PM10": pm10_dict,
            "PM25": pm25_dict
        }

    def emissions_formula(self, number_of_vehicles: float, link_length: float, ef: float, mass_fraction: float, speed_factor: float):

        return number_of_vehicles * link_length * ef * mass_fraction * speed_factor

    #
    # *** tyre wear emission calculation functions ***
    #

    def calculate_tyre_wear_emissions(self, vehicle_name: str, traffic_and_link_data_row: Dict[str, Any]) -> Dict[str, float]:

        total_pm_emissions = 0

        for los_type in range(1,5):
            weighted_emissions_for_los_type = self.calculate_emissions_for_los_type(
                los_type, vehicle_name, traffic_and_link_data_row)
            total_pm_emissions += weighted_emissions_for_los_type

        pm_emissions_by_pm_type = self.split_tyre_wear_emissions_into_mass_fractions(total_pm_emissions)
        return pm_emissions_by_pm_type

    def calculate_emissions_for_los_type(
            self, los_type: int, vehicle_name: str, traffic_and_link_data_row: Dict[str, Any]) -> float:

        ef = self.get_tyre_wear_ef_for_vehicle(vehicle_name)
        num_vehicles = traffic_and_link_data_row[vehicle_name]
        link_length = traffic_and_link_data_row["Length"]
        los_percentage = traffic_and_link_data_row[f"LOS{los_type}Percentage"]

        los_speed = self.get_los_speed_for_vehicle_and_link(los_type, traffic_and_link_data_row, vehicle_name)
        speed_factor = self.calculate_tyre_wear_speed_factor(los_speed)

        emissions_for_speed = self.emissions_formula(num_vehicles, link_length, ef, 1, speed_factor)
        return emissions_for_speed * los_percentage

    def split_tyre_wear_emissions_into_mass_fractions(self, total_pm_emissions: float) -> Dict[str, float]:

        return {
            "TSP": total_pm_emissions,
            "PM10": total_pm_emissions * self.pm10_tyre_wear_mass_fraction(),
            "PM25": total_pm_emissions * self.pm25_tyre_wear_mass_fraction()
        }

    def pm10_tyre_wear_mass_fraction(self) -> float:

        return 0.6

    def pm25_tyre_wear_mass_fraction(self) -> float:

        return 0.42

    def get_los_speed_for_vehicle_and_link(
            self, los_type: int, traffic_and_link_data_row: Dict[str, Any], vehicle_name: str) -> Dict[str, float]:

        link_id = traffic_and_link_data_row["LinkID"]
        vehicle_category = self.vehicle_dict[vehicle_name]
        los_speeds = self.los_speeds_dict[(link_id, vehicle_category)]
        los_speed = los_speeds[f"LOS{los_type}Speed"]
        return los_speed

    def get_tyre_wear_ef_for_vehicle(self, vehicle_name: str) -> float:

        if self.vehicle_category_is_pc(vehicle_name):
            return self.ef_tyre_wear_pc()
        elif self.vehicle_category_is_lcv(vehicle_name):
            return self.ef_tyre_wear_lcv()
        elif self.vehicle_category_is_mc_or_moped(vehicle_name):
            return self.ef_tyre_wear_two_wheel()
        elif self.vehicle_category_is_hdv_or_ubus_or_coach(vehicle_name):
            return self.ef_tyre_wear_hdv_ubus_coach(vehicle_name, self.load_factor)

        raise RuntimeError(f"Vehicle {vehicle_name} does not have a valid category."
                           f"The category is: {self.vehicle_dict[vehicle_name]}")

    def vehicle_category_is_pc(self, vehicle_name: str) -> bool:

        vehicle_category_lowercase = self.vehicle_dict[vehicle_name].lower()
        return "pc" in vehicle_category_lowercase

    def vehicle_category_is_lcv(self, vehicle_name: str) -> bool:

        vehicle_category_lowercase = self.vehicle_dict[vehicle_name].lower()
        return "lcv" in vehicle_category_lowercase

    def vehicle_category_is_mc_or_moped(self, vehicle_name: str) -> bool:

        vehicle_category_lowercase = self.vehicle_dict[vehicle_name].lower()
        return any(cat in vehicle_category_lowercase for cat in ["mc", "moped"])

    def vehicle_category_is_hdv_or_ubus_or_coach(self, vehicle_name: str) -> bool:

        vehicle_category_lowercase = self.vehicle_dict[vehicle_name].lower()
        return any(cat in vehicle_category_lowercase for cat in ["hdv", "ubus", "coach"])

    def ef_tyre_wear_two_wheel(self) -> float:

        return 0.0046

    def ef_tyre_wear_pc(self) -> float:

        return 0.0107

    def ef_tyre_wear_lcv(self) -> float:

        return 0.0169

    def ef_tyre_wear_hdv_ubus_coach(self, vehicle_name: str, load_factor: float) -> float:

        number_of_axles = self.number_of_axles_per_vehicle[vehicle_name]
        load_correction_factor = 1.41 + 1.38 * load_factor
        ef = number_of_axles / 2 * load_correction_factor * self.ef_tyre_wear_pc()
        return ef

    def calculate_tyre_wear_speed_factor(self, speed: float) -> float:

        if speed < 40:
            return 1.39
        elif 40 <= speed <= 90:
            return -0.00974 * speed + 1.78
        elif speed > 90:
            return 0.902

    #
    # *** break wear emission calculation functions ***
    #

    def calculate_break_wear_emissions(
            self, vehicle_name: str, traffic_and_link_data_row: Dict[str, Any]) -> Dict[str, float]:

        total_pm_emissions = 0

        for los_type in range(1,5):
            weighted_emissions_for_los_type = self.calculate_break_wear_emissions_for_los_type(
                los_type, vehicle_name, traffic_and_link_data_row)
            total_pm_emissions += weighted_emissions_for_los_type

        pm_emissions_by_pm_type = self.split_break_wear_emissions_into_mass_fractions(total_pm_emissions)
        return pm_emissions_by_pm_type

    def calculate_break_wear_emissions_for_los_type(
            self, los_type: int, vehicle_name: str, traffic_and_link_data_row: Dict[str, Any]) -> float:

        ef = self.get_break_wear_ef_for_vehicle(vehicle_name)
        num_vehicles = traffic_and_link_data_row[vehicle_name]
        link_length = traffic_and_link_data_row["Length"]
        los_percentage = traffic_and_link_data_row[f"LOS{los_type}Percentage"]

        los_speed = self.get_los_speed_for_vehicle_and_link(los_type, traffic_and_link_data_row, vehicle_name)
        speed_factor = self.calculate_break_wear_speed_factor(los_speed)

        emissions_for_speed = self.emissions_formula(num_vehicles, link_length, ef, 1, speed_factor)
        return emissions_for_speed * los_percentage

    def split_break_wear_emissions_into_mass_fractions(self, total_pm_emissions: float) -> Dict[str, float]:

        return {
            "TSP": total_pm_emissions,
            "PM10": total_pm_emissions * self.pm10_break_wear_mass_fraction(),
            "PM25": total_pm_emissions * self.pm25_break_wear_mass_fraction()
        }

    def pm10_break_wear_mass_fraction(self) -> float:

        return 0.98

    def pm25_break_wear_mass_fraction(self) -> float:

        return 0.39

    def get_break_wear_ef_for_vehicle(self, vehicle_name: str) -> float:

        if self.vehicle_category_is_pc(vehicle_name):
            return self.ef_break_wear_pc()
        elif self.vehicle_category_is_lcv(vehicle_name):
            return self.ef_break_wear_lcv()
        elif self.vehicle_category_is_mc_or_moped(vehicle_name):
            return self.ef_break_wear_two_wheel()
        elif self.vehicle_category_is_hdv_or_ubus_or_coach(vehicle_name):
            return self.ef_break_wear_hdv_ubus_coach(self.load_factor)

        raise RuntimeError(f"Vehicle {vehicle_name} does not have a valid category."
                           f"The category is: {self.vehicle_dict[vehicle_name]}")

    def ef_break_wear_two_wheel(self) -> float:

        return 0.0037

    def ef_break_wear_pc(self) -> float:

        return 0.0075

    def ef_break_wear_lcv(self) -> float:

        return 0.0117

    def ef_break_wear_hdv_ubus_coach(self, load_factor: float) -> float:

        load_correction_factor = 1 + 0.79 * load_factor
        return 3.13 * load_correction_factor * self.ef_break_wear_pc()

    def calculate_break_wear_speed_factor(self, speed: float) -> float:

        if speed < 40:
            return 1.67
        elif 40 <= speed <= 95:
            return -0.027 * speed + 2.75
        elif speed > 95:
            return 0.185

    #
    # *** road surface wear emission calculation functions ***
    #

    def calculate_road_surface_wear_emissions(
            self, vehicle_name: str, traffic_and_link_data_row: Dict[str, Any]) -> Dict[str, float]:

        num_veh = traffic_and_link_data_row[vehicle_name]
        link_length = traffic_and_link_data_row["Length"]
        ef = self.get_road_surface_wear_ef_for_vehicle(vehicle_name)

        total_pm_emissions = self.emissions_formula(num_veh, link_length, ef, 1, 1)
        pm_emissions_by_pm_type = self.split_road_surface_wear_emissions_into_mass_fractions(total_pm_emissions)

        return pm_emissions_by_pm_type

    def get_road_surface_wear_ef_for_vehicle(self, vehicle_name: str) -> float:

        if self.vehicle_category_is_pc(vehicle_name):
            return self.ef_road_surface_wear_pc()
        elif self.vehicle_category_is_lcv(vehicle_name):
            return self.ef_road_surface_wear_lcv()
        elif self.vehicle_category_is_mc_or_moped(vehicle_name):
            return self.ef_road_surface_wear_two_wheel()
        elif self.vehicle_category_is_hdv_or_ubus_or_coach(vehicle_name):
            return self.ef_road_surface_wear_hdv()

        raise RuntimeError(f"Vehicle {vehicle_name} does not have a valid category."
                           f"The category is: {self.vehicle_dict[vehicle_name]}")

    def ef_road_surface_wear_two_wheel(self) -> float:

        return 0.006

    def ef_road_surface_wear_pc(self) -> float:

        return 0.015

    def ef_road_surface_wear_lcv(self) -> float:

        return 0.015

    def ef_road_surface_wear_hdv(self) -> float:

        return 0.076

    def split_road_surface_wear_emissions_into_mass_fractions(self, total_pm_emissions: float) -> Dict[str, float]:

        return {
            "TSP": total_pm_emissions,
            "PM10": total_pm_emissions * self.pm10_road_surface_wear_mass_fraction(),
            "PM25": total_pm_emissions * self.pm25_road_surface_wear_mass_fraction()
        }

    def pm10_road_surface_wear_mass_fraction(self) -> float:

        return 0.5

    def pm25_road_surface_wear_mass_fraction(self) -> float:

        return 0.27
