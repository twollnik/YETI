"""
CopertColdStrategy

This module implements emission calculation with the COPERT methodology for cold start emissions.
"""
from collections import defaultdict
from typing import Any, Dict, Iterable, Tuple, Union

import pandas as pd

from code.copert_hot_strategy.CopertHotStrategy import CopertHotStrategy


class CopertColdStrategy:
    """
    Calculates cold start emissions using the COPERT methodology.

    Output of this Strategy are three datasets. One with cold emissions, one with hot emissions and
    one with total emissions. To calculate hot emissions, the CopertHotStrategy is used.

    Methods
    -------
    calculate_emissions
        The main interface for this Strategy. calculate_emissions is called over and over during
        a model run. Its job is to take a single traffic row (and some other parameters) and output
        a single row of the cold emissions data, the hot emissions data, and the total emissions data.

    """

    def __init__(self):

        self.cold_ef_table = None
        self.veh_mapping = None
        self.los_speeds_dict = None
        self.los_speeds_data = None
        self.hot_emission_factor_data = None
        self.vehicle_dict = None

        self.vehicles_pc_petrol_pre_euro = []
        self.vehicles_pc_petrol_euro = []
        self.vehicles_pc_diesel = []
        self.vehicles_pc_lpg_pre_euro = []
        self.vehicles_pc_lpg_euro = []
        self.vehicles_pc_cng = []
        self.vehicles_lcv_petrol_pre_euro = []
        self.vehicles_lcv_petrol_euro = []
        self.vehicles_lcv_diesel = []
        self.vehicles_other = []

        self.hot_strategy = CopertHotStrategy()
        self.ltrip = None  # average length of a trip as specified in config
        self.temperature= None
        self.ABC_dict = None
        self.corresponding_euro1_vehicles = None
        self.euro_category_for_vehicles = None
        self.segment_for_vehicles = None
        self.max_speed_in_cold_ef = None
        self.min_speed_in_cold_ef = None
        self.min_temp_in_cold_ef = None

        self.row = None
        self.hot_ef_dict = {}

    def calculate_emissions(self,
                            traffic_and_link_data_row: Dict[str, Any],
                            vehicle_dict: Dict[str, str],
                            pollutant: str,
                            **kwargs):
        """
        required kwargs:
        - unified_cold_ef_table
        - unified_los_speeds
        - unified_emission_factors
        - unified_vehicle_mapping
        - ltrip
        - temperature
        - exclude_road_types
        - exclude_area_types

        Returns a Dict with:
            - "hot" : hot emissions data frame
            - "cold" : cold emissions data frame
            - "total" : total emissions data frame
        """

        self.initialize_if_necessary(kwargs, vehicle_dict)
        self.store_row_data_in_attribute(traffic_and_link_data_row)

        hot_emissions = self.calculate_hot_emissions(pollutant)
        hot_ef_dict = self.get_hot_ef_from_hot_emissions(hot_emissions)

        if self.should_exclude_link_from_cold_emission_calculation(**kwargs) or self.temperature_is_very_high():
            cold_emissions = self.zero_emissions_for_all_vehicles()
        else:
            cold_emissions = self.calculate_cold_emissions(pollutant, hot_ef_dict)

        total_emissions = self.calculate_total_emissions(hot_emissions, cold_emissions)
        emissions = self.join_emissions_into_one_dict(hot_emissions, cold_emissions, total_emissions)

        return emissions

    def initialize_if_necessary(self, kwargs, vehicle_dict):

        if self.is_not_initialized():
            self.store_data_in_attributes(vehicle_dict, **kwargs)
            self.split_vehicles_into_groups(vehicle_dict)

    def is_not_initialized(self) -> bool:

        data_attributes = [self.cold_ef_table, self.veh_mapping, self.los_speeds_dict,
                           self.los_speeds_data, self.hot_emission_factor_data, self.ltrip, self.temperature]
        return any(att is None for att in data_attributes)

    def store_data_in_attributes(self, vehicle_dict: Dict[str, str], **kwargs):

        self.vehicle_dict = vehicle_dict

        self.initialize_cold_ef_table(kwargs["unified_cold_ef_table"])
        self.veh_mapping = kwargs["unified_vehicle_mapping"].set_index("VehName")
        self.los_speeds_data = kwargs["unified_los_speeds"]
        self.hot_emission_factor_data = kwargs["unified_emission_factors"]
        self.los_speeds_dict = self.los_speeds_data.set_index(["LinkID", "VehicleCategory"]).to_dict(orient="index")

        self.ltrip = kwargs["ltrip"]
        self.temperature = kwargs["temperature"]
        self.initialize_ABC_dict_if_necessary(kwargs["unified_cold_ef_table"])
        self.initialize_max_min_cold_ef_stats_if_necessary()
        self.initialize_corresponding_euro1_vehicles_if_necessary()
        self.initialize_euro_category_for_vehicles_if_necessary()
        self.initialize_segment_for_vehicles_if_necessary()

    def initialize_cold_ef_table(self, cold_ef_table: pd.DataFrame):

        cold_ef_table = cold_ef_table.astype({
            "MinSpeed": float,
            "MaxSpeed": float,
            "MinTemp": float,
            "MaxTemp": float,
            "A": float,
            "B": float,
            "C": float
        })
        cold_ef_table["MaxTemp"] = cold_ef_table["MaxTemp"].fillna(1000)
        self.cold_ef_table = cold_ef_table

    def initialize_max_min_cold_ef_stats_if_necessary(self):

        if self.max_speed_in_cold_ef is None:
            self.max_speed_in_cold_ef = self.cold_ef_table["MaxSpeed"].max()
            self.min_speed_in_cold_ef = self.cold_ef_table["MinSpeed"].min()
            self.min_temp_in_cold_ef = self.cold_ef_table["MinTemp"].min()

    def initialize_ABC_dict_if_necessary(self, cold_ef_table: pd.DataFrame):

        if self.ABC_dict is None:
            ABC_dict = defaultdict(list)
            for row in cold_ef_table.fillna(1000).itertuples():
                if row.MinTemp <= self.temperature <= row.MaxTemp:
                    ABC_dict[(row.VehSegment, row.Pollutant)].append(row)
            self.ABC_dict = ABC_dict

    def initialize_euro_category_for_vehicles_if_necessary(self):

        if self.euro_category_for_vehicles is None:
            self.euro_category_for_vehicles = {}
            for veh_name in self.vehicles():
                self.euro_category_for_vehicles[veh_name] = self.veh_mapping.loc[veh_name]["EuroStandard"]

    def initialize_segment_for_vehicles_if_necessary(self):

        if self.segment_for_vehicles is None:
            self.segment_for_vehicles = {}
            for veh_name in self.vehicles():
                self.segment_for_vehicles[veh_name] = self.veh_mapping.loc[veh_name]["VehSegment"]

    def initialize_corresponding_euro1_vehicles_if_necessary(self):

        if self.corresponding_euro1_vehicles is None:
            corresponding_euro1_vehicles = {}
            for veh_name in self.vehicles():
                corresponding_euro1_vehicles[veh_name] = self.get_corresponding_euro1_for_vehicle(veh_name)
            self.corresponding_euro1_vehicles = corresponding_euro1_vehicles

    def temperature_is_very_high(self) -> bool:

        return self.temperature > 30

    def get_corresponding_euro1_for_vehicle(self, veh_name) -> Union[str, None]:

        mapping_row_for_veh_name = self.veh_mapping.loc[veh_name]
        veh_cat = mapping_row_for_veh_name["VehCat"]
        fuel = mapping_row_for_veh_name["Fuel"]
        segment = mapping_row_for_veh_name["VehSegment"]

        corresponding_euro1_veh_name = self.veh_mapping[
            (self.veh_mapping["VehCat"] == veh_cat) &
            (self.veh_mapping["Fuel"] == fuel) &
            (self.veh_mapping["VehSegment"] == segment) &
            (self.veh_mapping["EuroStandard"] == "Euro 1")
        ].index
        try:
            return corresponding_euro1_veh_name.item()
        except:
            return None

    def store_row_data_in_attribute(self, row: Dict[str, Any]):

        self.row = row

    def get_hot_ef_from_hot_emissions(self, hot_emissions: Dict[str, float]) -> Dict[str, float]:
        """Calculate the hot ef using the formula 'hot ef = hot emissions / link length / vehicle count' """

        hot_ef = self.hot_ef_dict if self.hot_ef_dict is not None else {}
        for veh_name, emissions in hot_emissions.items():
            try:
                hot_ef[veh_name] = (emissions / self.row["Length"] / self.row[veh_name])
            except ZeroDivisionError:
                # If length or vehicle count is 0, the hot ef value does not matter.
                # Emissions will be zero in any case. Set hot_ef to 1 to avoid further errors.
                hot_ef[veh_name] = 1

        return hot_ef

    def join_emissions_into_one_dict(
            self, hot_emissions: Dict[str, float],
            cold_emissions: Dict[str, float],
            total_emissions: Dict[str, float]) -> Dict[str, Dict[str, float]]:

        return {
            "cold": cold_emissions,
            "hot": hot_emissions,
            "total": total_emissions
        }

    def should_exclude_link_from_cold_emission_calculation(self, **kwargs) -> bool:

        road_types_to_exclude = kwargs.get("exclude_road_types", [])
        area_types_to_exclude = kwargs.get("exclude_area_types", [])
        link_road_type = self.row["RoadType"]
        link_area_type = self.row["AreaType"]

        if link_area_type in area_types_to_exclude or link_road_type in road_types_to_exclude:
            return True
        return False

    def zero_emissions_for_all_vehicles(self) -> Dict[str, float]:

        return {veh_name: 0 for veh_name in self.vehicles()}

    def split_vehicles_into_groups(self, vehicle_dict: Dict[str, str]):

        for veh_name, veh_category in vehicle_dict.items():
            veh_euro, veh_fuel = self.determine_euro_and_fuel_for_vehicle(veh_name)
            self.add_vehicle_to_correct_group(veh_name, veh_category, veh_euro, veh_fuel)

    def determine_euro_and_fuel_for_vehicle(self, veh_name) -> Tuple[str, str]:

        veh_data = self.veh_mapping.loc[veh_name]
        return veh_data["EuroStandard"], veh_data["Fuel"]

    def add_vehicle_to_correct_group(self, veh_name: str, veh_category: str, veh_euro: str, veh_fuel: str):

        if veh_category == "VehicleCategory.PC":
            self.add_vehicle_to_correct_pc_group(veh_euro, veh_fuel, veh_name)
        elif veh_category == "VehicleCategory.LCV":
            self.add_vehicle_to_correct_lcv_group(veh_euro, veh_fuel, veh_name)
        else:
            self.vehicles_other.append(veh_name)

    def add_vehicle_to_correct_pc_group(self, veh_euro: str, veh_fuel: str, veh_name: str):

        veh_fuel = veh_fuel.lower()
        if veh_fuel == "petrol":
            if "Euro" in veh_euro:
                self.vehicles_pc_petrol_euro.append(veh_name)
            else:
                self.vehicles_pc_petrol_pre_euro.append(veh_name)
        elif veh_fuel == "diesel":
            self.vehicles_pc_diesel.append(veh_name)
        elif "cng" in veh_fuel:
            self.vehicles_pc_cng.append(veh_name)
        elif "lpg" in veh_fuel:
            if "Euro" in veh_euro:
                self.vehicles_pc_lpg_euro.append(veh_name)
            else:
                self.vehicles_pc_lpg_pre_euro.append(veh_name)
        else:
            raise RuntimeError(f"Vehicle {veh_name} could not be associated with a vehicle group.")

    def add_vehicle_to_correct_lcv_group(self, veh_euro: str, veh_fuel: str, veh_name: str):

        if veh_fuel == "Petrol":
            if "Euro" in veh_euro:
                self.vehicles_lcv_petrol_euro.append(veh_name)
            else:
                self.vehicles_lcv_petrol_pre_euro.append(veh_name)
        else:
            self.vehicles_lcv_diesel.append(veh_name)

    def calculate_hot_emissions(self, pollutant: str) -> Dict[str, float]:

        return self.hot_strategy.calculate_emissions(
            self.row, self.vehicle_dict, pollutant, los_speeds_data=self.los_speeds_data,
            emission_factor_data=self.hot_emission_factor_data
        )

    def calculate_cold_emissions(self, pollutant: str, hot_ef: Dict[str, float]) -> Dict[str, float]:

        self.hot_ef_dict = hot_ef  # store in attribute for use by called functions

        cold_emissions_petrol_pc_pre_euro = self.calculate_cold_emissions_for_petrol_pc_pre_euro_vehicles(pollutant)
        cold_emissions_petrol_pc_past_euro1 = self.calculate_cold_emissions_for_petrol_pc_euro_vehicles(pollutant)
        cold_emissions_diesel_pc = self.calculate_cold_emissions_for_diesel_pc_vehicles(pollutant)
        cold_emissions_lpg_pc_pre_euro = self.calculate_cold_emissions_for_lpg_pc_pre_euro_vehicles(pollutant)
        cold_emissions_lpg_pc_euro = self.calculate_cold_emissions_for_lpg_pc_euro_vehicles(pollutant)
        cold_emissions_cng_pc = self.calculate_cold_emissions_for_cng_pc_vehicles(pollutant)

        cold_emissions_petrol_lcv_pre_euro = self.calculate_cold_emissions_for_petrol_lcv_pre_euro_vehicles(pollutant)
        cold_emissions_petrol_lcv_past_euro1 = self.calculate_cold_emissions_for_petrol_lcv_euro_vehicles(pollutant)
        cold_emissions_diesel_lcv = self.calculate_cold_emissions_for_diesel_lcv_vehicles(pollutant)

        cold_emissions_other_vehicles = self.calculate_cold_emissions_for_other_vehicles()

        cold_emissions = {
            **cold_emissions_petrol_pc_pre_euro,
            **cold_emissions_petrol_pc_past_euro1,
            **cold_emissions_diesel_pc,
            **cold_emissions_lpg_pc_pre_euro,
            **cold_emissions_lpg_pc_euro,
            **cold_emissions_cng_pc,
            **cold_emissions_petrol_lcv_pre_euro,
            **cold_emissions_petrol_lcv_past_euro1,
            **cold_emissions_diesel_lcv,
            **cold_emissions_other_vehicles
        }
        return cold_emissions

    def calculate_total_emissions(
            self, hot_emissions: Dict[str, float], cold_emissions: Dict[str, float]) -> Dict[str, float]:

        total_emissions = {
            vehicle: hot_emissions[vehicle] + cold_emissions[vehicle]
            for vehicle in self.vehicles()
        }
        return total_emissions

    def calculate_cold_emissions_for_petrol_pc_pre_euro_vehicles(self, pollutant: str) -> Dict[str, float]:

        cold_emissions_petrol_pc_pre_euro = {
            veh_name: self.calculate_cold_emissions_petrol_pc_pre_euro(pollutant, veh_name)
            for veh_name in self.vehicles_pc_petrol_pre_euro
        }
        return cold_emissions_petrol_pc_pre_euro

    def calculate_cold_emissions_for_petrol_pc_euro_vehicles(self, pollutant: str) -> Dict[str, float]:

        cold_emissions_petrol_pc_euro = {
            veh_name: self.calculate_cold_emissions_petrol_pc_euro(pollutant, veh_name)
            for veh_name in self.vehicles_pc_petrol_euro
        }
        return cold_emissions_petrol_pc_euro

    def calculate_cold_emissions_for_diesel_pc_vehicles(self, pollutant: str) -> Dict[str, float]:

        cold_emissions_diesel_pc = {
            veh_name: self.calculate_cold_emissions_diesel_pc(pollutant, veh_name)
            for veh_name in self.vehicles_pc_diesel
        }
        return cold_emissions_diesel_pc

    def calculate_cold_emissions_for_lpg_pc_pre_euro_vehicles(self, pollutant: str) -> Dict[str, float]:

        cold_emissions_lpg_pc_pre_euro = {
            veh_name: self.calculate_cold_emissions_lpg_pc_pre_euro(pollutant, veh_name)
            for veh_name in self.vehicles_pc_lpg_pre_euro
        }
        return cold_emissions_lpg_pc_pre_euro

    def calculate_cold_emissions_for_lpg_pc_euro_vehicles(self, pollutant: str) -> Dict[str, float]:

        cold_emissions_lpg_pc_euro = {
            veh_name: self.calculate_cold_emissions_lpg_pc_euro(pollutant, veh_name)
            for veh_name in self.vehicles_pc_lpg_euro
        }
        return cold_emissions_lpg_pc_euro

    def calculate_cold_emissions_for_cng_pc_vehicles(self, pollutant: str) -> Dict[str, float]:

        cold_emissions_cng_pc = {
            veh_name: self.calculate_cold_emissions_cng_pc(pollutant, veh_name)
            for veh_name in self.vehicles_pc_cng
        }
        return cold_emissions_cng_pc

    def calculate_cold_emissions_for_petrol_lcv_pre_euro_vehicles(self, pollutant: str) -> Dict[str, float]:

        return {
            veh_name: self.calculate_cold_emissions_petrol_lcv_pre_euro(pollutant, veh_name)
            for veh_name in self.vehicles_lcv_petrol_pre_euro
        }

    def calculate_cold_emissions_for_petrol_lcv_euro_vehicles(self, pollutant: str) -> Dict[str, float]:

        return {
            veh_name: self.calculate_cold_emissions_petrol_lcv_euro(pollutant, veh_name)
            for veh_name in self.vehicles_lcv_petrol_euro
        }

    def calculate_cold_emissions_for_diesel_lcv_vehicles(self, pollutant: str) -> Dict[str, float]:

        return {
            veh_name: self.calculate_cold_emissions_diesel_lcv(pollutant, veh_name)
            for veh_name in self.vehicles_lcv_diesel
        }

    def calculate_cold_emissions_for_other_vehicles(self) -> Dict[str, float]:

        return {veh_name: 0 for veh_name in self.vehicles_other}

    def calculate_cold_emissions_petrol_pc_pre_euro(self, pollutant: str, vehicle_name: str) -> float:

        cold_hot_quotient = self.get_cold_hot_quotient_petrol_pc_pre_euro(pollutant)
        ef_hot = self.hot_ef_dict[vehicle_name]
        emissions = self.cold_emissions_formula(
            ltrip=self.ltrip, temp=self.temperature, beta_correction_factor=1, num_cars=self.row[vehicle_name],
            link_length=self.row["Length"], ef_hot=ef_hot, cold_hot_quotient=cold_hot_quotient)
        return emissions

    def get_cold_hot_quotient_petrol_pc_pre_euro(self, pollutant: str) -> float:

        if pollutant == "PollutantType.CO":
            return 3.7 - 0.09 * self.temperature
        elif pollutant == "PollutantType.NOx":
            return 1.14 - 0.006 * self.temperature
        elif pollutant == "PollutantType.VOC":
            return 2.8 - 0.06 * self.temperature
        raise RuntimeError(f"Unexpected pollutant: {pollutant}. Pass 'PollutantType.NOx', "
                           f"'PollutantType.CO', or 'PollutantType.VOC'.")

    def calculate_cold_emissions_petrol_pc_euro(self, pollutant: str, vehicle_name: str) -> float:

        vehicle_category = self.vehicle_dict[vehicle_name]
        los_speeds_for_link_and_vehicle_category = self.los_speeds_dict[self.row["LinkID"], vehicle_category]

        cold_emissions = 0

        for los in range(1, 5):

            speed = los_speeds_for_link_and_vehicle_category[f"LOS{los}Speed"]
            emis = self.calculate_cold_emissions_petrol_pc_past_euro1_for_speed(
                pollutant, vehicle_name, speed
            )
            los_percentage = self.row[f"LOS{los}Percentage"]

            weighted_emis = emis * los_percentage
            cold_emissions += weighted_emis

        return cold_emissions

    def calculate_cold_emissions_diesel_pc(self, pollutant: str, vehicle_name: str) -> float:

        beta_correction_factor = 1
        hot_ef = self.hot_ef_dict[vehicle_name]
        cold_hot_quotient = self.get_cold_hot_quotient_for_diesel_vehicle(pollutant)

        cold_emissions = self.cold_emissions_formula(
            ltrip=self.ltrip, temp=self.temperature, beta_correction_factor=beta_correction_factor,
            num_cars=self.row[vehicle_name], link_length=self.row["Length"], ef_hot=hot_ef,
            cold_hot_quotient=cold_hot_quotient)

        return cold_emissions

    def calculate_cold_emissions_petrol_pc_past_euro1_for_speed(
            self, pollutant: str, vehicle_name: str, speed: float) -> float:

        if speed > 45:
            return 0

        beta_correction_factor = self.get_beta_correction_factor(vehicle_name, pollutant)
        ef_hot_euro1 = self.get_euro1_hot_ef(vehicle_name)
        cold_hot_quotient = self.get_cold_hot_quotient_ABC_method(vehicle_name, pollutant, speed)

        cold_emissions = self.cold_emissions_formula(
            ltrip=self.ltrip, temp=self.temperature, beta_correction_factor=beta_correction_factor,
            num_cars=self.row[vehicle_name], link_length=self.row["Length"], ef_hot=ef_hot_euro1,
            cold_hot_quotient=cold_hot_quotient
        )

        return cold_emissions

    def calculate_cold_emissions_lpg_pc_pre_euro(self, pollutant: str, vehicle_name: str) -> float:

        num_cars = self.row[vehicle_name]
        beta_correction_factor = 1
        link_length = self.row["Length"]
        cold_hot_quotient = self.get_cold_hot_quotient_lpg_pc_pre_euro(pollutant)
        ef_hot = self.get_hot_ef_lpg_and_cng_pc(vehicle_name)

        cold_emissions = self.cold_emissions_formula(
            ltrip=self.ltrip, temp=self.temperature, beta_correction_factor=beta_correction_factor,
            num_cars=num_cars, link_length=link_length, ef_hot=ef_hot, cold_hot_quotient=cold_hot_quotient
        )
        return cold_emissions

    def calculate_cold_emissions_lpg_pc_euro(self, pollutant: str, vehicle_name: str):

        vehicle_category = self.vehicle_dict[vehicle_name]
        los_speeds_for_link_and_vehicle_category = self.los_speeds_dict[self.row["LinkID"], vehicle_category]

        cold_emissions = 0

        for los in range(1, 5):
            speed = los_speeds_for_link_and_vehicle_category[f"LOS{los}Speed"]
            emis = self.calculate_cold_emissions_lpg_pc_euro_for_speed(
                pollutant, vehicle_name, speed
            )
            los_percentage = self.row[f"LOS{los}Percentage"]

            weighted_emis = emis * los_percentage
            cold_emissions += weighted_emis

        return cold_emissions

    def calculate_cold_emissions_lpg_pc_euro_for_speed(
            self, pollutant: str, vehicle_name: str, speed: float) -> float:

        if speed > 45:
            return 0

        beta_correction_factor = self.get_beta_correction_factor(vehicle_name, pollutant)
        ef_hot_euro1 = self.get_hot_ef_lpg_and_cng_pc(vehicle_name)
        cold_hot_quotient = self.get_cold_hot_quotient_ABC_method(vehicle_name, pollutant, speed)

        cold_emissions = self.cold_emissions_formula(
            ltrip=self.ltrip, temp=self.temperature, beta_correction_factor=beta_correction_factor,
            num_cars=self.row[vehicle_name], link_length=self.row["Length"], ef_hot=ef_hot_euro1,
            cold_hot_quotient=cold_hot_quotient
        )

        return cold_emissions

    def calculate_cold_emissions_cng_pc(self, pollutant: str, vehicle_name: str) -> float:

        vehicle_category = self.vehicle_dict[vehicle_name]
        los_speeds_for_link_and_vehicle_category = self.los_speeds_dict[self.row["LinkID"], vehicle_category]

        cold_emissions = 0

        for los in range(1, 5):
            speed = los_speeds_for_link_and_vehicle_category[f"LOS{los}Speed"]
            emis = self.calculate_cold_emissions_cng_pc_for_speed(
                pollutant, vehicle_name, speed
            )
            los_percentage = self.row[f"LOS{los}Percentage"]

            weighted_emis = emis * los_percentage
            cold_emissions += weighted_emis

        return cold_emissions

    def calculate_cold_emissions_cng_pc_for_speed(self, pollutant: str, vehicle_name: str, speed: float) -> float:

        if speed > 45:
            return 0

        ef_hot_euro1 = self.get_hot_ef_lpg_and_cng_pc(vehicle_name)
        cold_hot_quotient = self.get_cold_hot_quotient_ABC_method_for_cng(vehicle_name, pollutant, speed)

        cold_emissions = self.cold_emissions_formula(
            ltrip=self.ltrip, temp=self.temperature, beta_correction_factor=1,
            num_cars=self.row[vehicle_name], link_length=self.row["Length"], ef_hot=ef_hot_euro1,
            cold_hot_quotient=cold_hot_quotient
        )
        return cold_emissions

    def calculate_cold_emissions_petrol_lcv_pre_euro(self, pollutant: str, vehicle_name: str) -> float:

        num_cars = self.row[vehicle_name]
        beta_correction_factor = 1
        link_length = self.row["Length"]
        ef_hot = self.hot_ef_dict[vehicle_name]
        cold_hot_quotient = self.get_hot_cold_quotient_petrol_lcv_pre_euro(pollutant)

        cold_emissions = self.cold_emissions_formula(
            ltrip=self.ltrip, temp=self.temperature, beta_correction_factor=beta_correction_factor,
            num_cars=num_cars, link_length=link_length, ef_hot=ef_hot, cold_hot_quotient=cold_hot_quotient
        )
        return cold_emissions

    def get_hot_cold_quotient_petrol_lcv_pre_euro(self, pollutant: str) -> float:

        if "NOx" in pollutant:
            return 1.14 - 0.006 * self.temperature
        elif "CO" in pollutant:
            return 3.7 - 0.09 * self.temperature
        elif "VOC" in pollutant:
            return 2.8 - 0.06 * self.temperature
        else:
            raise RuntimeError(f"The pollutant {pollutant} is not recognized by the model. "
                               f"Use 'PollutantType.NOx', 'PollutantType.CO' or 'PollutantType.VOC'.")

    def calculate_cold_emissions_petrol_lcv_euro(self, pollutant: str, vehicle_name: str) -> float:

        vehicle_category = self.vehicle_dict[vehicle_name]
        los_speeds_for_link_and_vehicle_category = self.los_speeds_dict[self.row["LinkID"], vehicle_category]

        cold_emissions = 0

        for los in range(1, 5):
            speed = los_speeds_for_link_and_vehicle_category[f"LOS{los}Speed"]
            emis = self.calculate_cold_emissions_petrol_lcv_euro_for_speed(
                pollutant, vehicle_name, speed
            )
            los_percentage = self.row[f"LOS{los}Percentage"]

            weighted_emis = emis * los_percentage
            cold_emissions += weighted_emis

        return cold_emissions

    def calculate_cold_emissions_petrol_lcv_euro_for_speed(
            self, pollutant: str, vehicle_name: str, speed: float) -> float:

        if speed > 45:
            return 0

        beta_correction_factor = self.get_beta_correction_factor(vehicle_name, pollutant)
        num_cars = self.row[vehicle_name]
        link_length = self.row["Length"]
        ef_hot = self.get_euro1_hot_ef(vehicle_name)
        cold_hot_quotient = self.get_cold_hot_quotient_ABC_method(vehicle_name, pollutant, speed)

        cold_emissions = self.cold_emissions_formula(
            ltrip=self.ltrip, temp=self.temperature, beta_correction_factor=beta_correction_factor,
            num_cars=num_cars, link_length=link_length, ef_hot=ef_hot, cold_hot_quotient=cold_hot_quotient
        )
        return cold_emissions

    def calculate_cold_emissions_diesel_lcv(self, pollutant: str, vehicle_name: str) -> float:

        num_cars = self.row[vehicle_name]
        link_length = self.row["Length"]
        ef_hot = self.hot_ef_dict[vehicle_name]
        cold_hot_quotient = self.get_cold_hot_quotient_for_diesel_vehicle(pollutant)
        beta_correction_factor = 1

        cold_emissions = self.cold_emissions_formula(
            ltrip=self.ltrip, temp=self.temperature, beta_correction_factor=beta_correction_factor,
            num_cars=num_cars, link_length=link_length, ef_hot=ef_hot, cold_hot_quotient=cold_hot_quotient
        )
        return cold_emissions

    def get_hot_ef_lpg_and_cng_pc(self, vehicle_name: str) -> float:

        own_mapping_row = self.veh_mapping.loc[vehicle_name]

        if vehicle_name in self.vehicles_pc_lpg_pre_euro:
            euro = own_mapping_row["EuroStandard"]
        else:
            euro = "Euro 1"

        veh_name_for_hot_ef = self.veh_mapping[
            (self.veh_mapping["Fuel"] == "Petrol") &
            (self.veh_mapping["EuroStandard"] == euro) &
            (self.veh_mapping["VehSegment"] == own_mapping_row["VehSegment"]) &
            (self.veh_mapping.index != vehicle_name)
        ].index.item()

        ef_hot = self.hot_ef_dict[veh_name_for_hot_ef]
        return ef_hot

    def get_cold_hot_quotient_for_diesel_vehicle(self, pollutant: str) -> float:

        if pollutant == "PollutantType.CO":
            return 1.9 - 0.03 * self.temperature
        elif pollutant == "PollutantType.NOx":
            return 1.3 - 0.013 * self.temperature
        elif pollutant == "PollutantType.VOC":
            return 3.1 - 0.09 * self.temperature if self.temperature <= 29 else 0.5
        elif "PollutantType.PM" in pollutant:
            # condition differs from other conditions to capture all types of PM emissions
            return 3.1 - 0.1 * self.temperature if self.temperature <= 26 else 0.5
        else:
            raise RuntimeError(f"Unknown pollutant: {pollutant}")

    def get_cold_hot_quotient_lpg_pc_pre_euro(self, pollutant: str):

        pollutant_lowercase = pollutant.lower()

        if "co" in pollutant_lowercase:
            return 3.66 - 0.09 * self.temperature
        elif "nox" in pollutant_lowercase:
            return 0.98 - 0.006 * self.temperature
        elif "voc" in pollutant_lowercase:
            if self.temperature <= 29:
                return 2.24 - 0.06 * self.temperature
            else:
                return 0.5
        else:
            raise RuntimeError(f"The pollutant {pollutant} is not recognized by the model. "
                               f"Use 'PollutantType.NOx', 'PollutantType.CO' or 'PollutantType.VOC'.")

    def get_cold_hot_quotient_ABC_method_for_cng(self, veh_name: str, pollutant: str, speed: float) -> float:

        if "voc" in pollutant.lower():
            return self.get_cold_hot_quotient_ABC_method_for_cng_pollutant_voc(veh_name, speed)
        else:
            return self.get_cold_hot_quotient_ABC_method(veh_name, pollutant, speed)

    def get_cold_hot_quotient_ABC_method_for_cng_pollutant_voc(
            self, veh_name: str, speed: float) -> float:

        if -20 <= self.temperature <= 15:
            if speed <= 25:
                A, B, C = 0.118568, -0.15633, 5.538047
            else:
                A, B, C = 0.212969, -0.25526, 3.339635
        elif self.temperature > 15:
            A, B, C = 0.035948, -0.36023, 10.39479

        return self.cold_hot_quotient_A_B_C_formula(speed, self.temperature, A, B, C)

    def get_cold_hot_quotient_ABC_method(self, veh_name: str, pollutant: str, speed: float) -> float:

        veh_segment = self.get_veh_segment(veh_name)
        self.check_speed_and_temp_in_valid_range(speed, self.temperature)

        A, B, C = self.get_ABC_for_quotient_calculation(veh_segment, pollutant, speed)

        return self.cold_hot_quotient_A_B_C_formula(speed, self.temperature, A, B, C)

    def get_ABC_for_quotient_calculation(
            self, veh_segment: str, pollutant: str, speed: float) -> Tuple[float, float, float]:

        self.initialize_ABC_dict_if_necessary(self.cold_ef_table)

        pollutant_long_form = f"PollutantType.{pollutant}"
        pollutant_short_form = pollutant.split(".")[-1]

        cold_ef_data = self.ABC_dict.get((veh_segment, pollutant)) \
                       or self.ABC_dict.get((veh_segment, pollutant_short_form)) \
                       or self.ABC_dict.get((veh_segment, pollutant_long_form)) \
                       or []

        for item in cold_ef_data:
            if item.MinSpeed <= speed <= item.MaxSpeed:
                return item.A, item.B, item.C

        raise RuntimeError(f"No ABC values could be found for vehicle segment: {veh_segment}, "
                           f"pollutant: {pollutant} and speed: {speed}")

    def cold_hot_quotient_A_B_C_formula(self, speed: float, temp: float, A: float, B: float, C: float) -> float:

        return A * speed + B * temp + C

    def get_veh_segment(self, vehicle_name: str) -> str:

        self.initialize_segment_for_vehicles_if_necessary()

        vehicle_category = self.vehicle_dict[vehicle_name]

        if "PC" in vehicle_category:
            return self.segment_for_vehicles[vehicle_name]
        elif "LCV" in vehicle_category:
            return "Large-SUV-Executive"
        else:
            raise RuntimeError(f"Vehicle segment could not be determined for vehicle: {vehicle_name}")

    def check_speed_and_temp_in_valid_range(self, speed: float, temp: float):

        self.initialize_max_min_cold_ef_stats_if_necessary()

        if speed > self.max_speed_in_cold_ef \
                or speed < self.min_speed_in_cold_ef \
                or temp < self.min_temp_in_cold_ef:
            raise RuntimeError(f"No ABC data for Temp = {temp} and Speed = {speed}")

    def get_euro1_hot_ef(self, veh_name: str) -> float:

        self.initialize_corresponding_euro1_vehicles_if_necessary()

        corresponding_euro1_veh_name = self.corresponding_euro1_vehicles[veh_name]
        euro_1_hot_ef = self.hot_ef_dict[corresponding_euro1_veh_name]

        return euro_1_hot_ef

    def get_beta_correction_factor(self, vehicle_name: str, pollutant: str) -> float:

        self.initialize_euro_category_for_vehicles_if_necessary()

        euro = self.euro_category_for_vehicles[vehicle_name]

        if "Euro " not in euro or euro[-1].isdigit() is False:
            raise RuntimeError(f"Euro type not recognized: {euro}")
        elif pollutant not in {"PollutantType.NOx", "PollutantType.CO", "PollutantType.VOC"}:
            raise RuntimeError(f"Pollutant not recognized: {pollutant}")

        if euro == "Euro 1":
            return 1
        elif euro == "Euro 2" and pollutant in {"PollutantType.CO", "PollutantType.NOx"}:
            return 0.72
        elif euro == "Euro 2" and pollutant == "PollutantType.VOC":
            return 0.56
        elif euro == "Euro 3" and pollutant in {"PollutantType.VOC", "PollutantType.NOx"}:
            return 0.32
        elif euro == "Euro 3" and pollutant == "PollutantType.CO":
            return 0.62
        else:
            # Euro 4 and on
            return 0.18

    def cold_emissions_formula(
            self, ltrip: float, temp: float, beta_correction_factor: float, num_cars: float,
            link_length: float, ef_hot: float, cold_hot_quotient: float) -> float:

        beta = self.calculate_beta(ltrip, temp)
        if cold_hot_quotient < 1:
            cold_hot_quotient = 1
        return beta_correction_factor * beta * num_cars * link_length * ef_hot * (cold_hot_quotient - 1)

    def calculate_beta(self, ltrip: float, temp: float) -> float:
        return 0.6474 - 0.02545 * ltrip - (0.00974 - 0.000385 * ltrip) * temp

    def vehicles(self) -> Iterable[str]:

        return self.vehicle_dict.keys()