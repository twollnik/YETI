from itertools import product

import pandas as pd

from code.constants.column_names import *
from code.constants.enumerations import PollutantType


class EmissionFactorDataLoader:

    def __init__(self, use_nh3_tier2_ef: bool = True, **kwargs):
        """ Initialize an EmissionFactorDataLoader instance.

        :param use_nh3_tier2_ef: Whether or not to use tier 2 emission factor values for the pollutant NH3.
                                 If this parameter is True, you need to pass the additional keyword arguments
                                 'nh3_ef_data' and 'nh3_mapping_data' (more infos below).

        You need to pass the following keyword arguments:

        - fleet_comp_data: a pd.DataFrame containing the names of the vehicles to load the emission factor
                           data for.
        - ef_data : a pd.DataFrame containing emission factor data. It needs
                    to contain all the columns that are specified under
                    '# emission factor data' in 'column_names.py'.
        - vehicle_mapping_data : a pd.DataFrame mapping vehicle names to the
                                 vehicle categries, classes, ... as used in
                                 the emission factors dataset. It needs to
                                 contain all the columns that are specified
                                 under '# vehicle name to copert categories mapping data'

        These keyword arguments are only needed if use_nh3_tier2_ef is True:

        - nh3_ef_data : a pd.DataFrame with tier 2 nh3 emission factors. It needs to contain the
                        columns specified under '# NH3 Tier 2 emission factor data' in 'column_names.py'.
        - nh3_mapping_data : a pd.DataFrame mapping vehicle names to the keys of nh3_ef_data. It needs to
                        contain the columns specified under '# vehicle names to NH3 ef categories mapping data'
                        in 'column_names.py'.
        """

        self.use_nh3_tier2_ef = use_nh3_tier2_ef

        self.fleet_comp_data = kwargs['fleet_comp_data']
        self.vehicle_mapping_data = kwargs['vehicle_mapping_data']
        self.ef_data = kwargs['ef_data']

        if self.use_nh3_tier2_ef is True:
            self.nh3_ef_data = kwargs['nh3_ef_data']
            self.nh3_mapping = kwargs['nh3_mapping_data']

    def load_data(self):
        """ Get emission factor data.

        This method uses the dataframes that were previously passed to the constructor method. It also depends on
        the parameter 'use_nh3_tier2_ef' from the constructor method.

        Note that only rows with a pollutant that is in the PollutantType enumeration will be part
        of the output dataframe.

        :return: a 2-tuple with these elements:
            - emission_factor_data : a pd.DataFrame containing the emission factor data in yeti_format
            - vehicles_without_ef_data : a pd.DataFrame containing the vehicle name, pollutant combinations
                                         that have no associated ef data.
        """

        speed_dependent_ef_data = self.load_speed_dependent_ef_data()

        if self.use_nh3_tier2_ef is True:

            nh3_ef_data = self.load_nh3_ef_data()
            ef_data = pd.merge(speed_dependent_ef_data, nh3_ef_data,
                               on=["VehicleName", "Pollutant"], how='outer')

        else:

            ef_data = speed_dependent_ef_data

        missing_ef_data = self.determine_missing_ef_data(ef_data)

        return ef_data, missing_ef_data

    def load_speed_dependent_ef_data(self):

        # consider vehicles whose mapping relies on Technology
        emission_factor_data_with_tech = pd.merge(
            self.vehicle_mapping_data[~pd.isna(self.vehicle_mapping_data["Technology"])],
            self.ef_data,
            left_on=[MAP_EURO, MAP_FUEL, MAP_TECHNOLOGY, MAP_VEH_CAT, MAP_VEH_SEG],
            right_on=[EF_EURO, EF_FUEL, EF_TECHNOLOGY, EF_VEH_CAT, EF_VEH_SEG])

        # consider vehicles whose mapping does not contain a value for Technology
        emission_factor_data_no_tech = pd.merge(
            self.vehicle_mapping_data[pd.isna(self.vehicle_mapping_data["Technology"])],
            self.ef_data,
            left_on=[MAP_EURO, MAP_FUEL, MAP_VEH_CAT, MAP_VEH_SEG],
            right_on=[EF_EURO, EF_FUEL, EF_VEH_CAT, EF_VEH_SEG])

        emission_factor_data = pd.concat([emission_factor_data_no_tech, emission_factor_data_with_tech],
                                         sort=False)

        emission_factor_data = emission_factor_data[[
            MAP_VEH_NAME, EF_POLL, EF_MODE, EF_LOAD, EF_SLOPE, EF_MIN_SPEED, EF_MAX_SPEED,
            EF_ALPHA, EF_BETA, EF_DELTA, EF_EPSILON, EF_GAMMA, EF_HTA, EF_THITA, EF_ZITA, EF_REDUC_FAC
        ]]

        emission_factor_data = emission_factor_data.rename({
            MAP_VEH_NAME: "VehicleName", EF_POLL: "Pollutant", EF_MODE: "Mode", EF_LOAD: "Load", EF_SLOPE: "Slope",
            EF_MIN_SPEED: "MinSpeed", EF_MAX_SPEED: "MaxSpeed", EF_ALPHA: "Alpha", EF_BETA: "Beta", EF_DELTA: "Delta",
            EF_EPSILON: "Epsilon", EF_GAMMA: "Gamma", EF_HTA: "Hta", EF_THITA: "Thita", EF_ZITA: "Zita",
            EF_REDUC_FAC: "ReductionPerc"
        }, axis='columns')

        # convert pollutants to PollutantType objects
        emission_factor_data["Pollutant"] = emission_factor_data["Pollutant"].apply(
            lambda poll: PollutantType.from_val(poll))

        return emission_factor_data

    def load_nh3_ef_data(self):

        nh3_efs_for_vehicle_names = pd.merge(self.nh3_mapping, self.nh3_ef_data,
                                             left_on=[NH3_EF_EURO, NH3_EF_FUEL, NH3_EF_VEH_CAT, NH3_EF_VEH_SEG],
                                             right_on=[NH3_MAP_EURO, NH3_MAP_FUEL, NH3_MAP_VEH_CAT, NH3_MAP_VEH_SEG])

        nh3_efs_for_vehicle_names = nh3_efs_for_vehicle_names[[NH3_MAP_VEH_NAME, NH3_EF_EF]]
        nh3_efs_for_vehicle_names = nh3_efs_for_vehicle_names.rename({
            NH3_MAP_VEH_NAME: "VehicleName",
            NH3_EF_EF: "EF"
        }, axis='columns')

        nh3_efs_for_vehicle_names["Pollutant"] = PollutantType.NH3

        return nh3_efs_for_vehicle_names

    def determine_missing_ef_data(self, ef_data):

        missing_ef_data = []

        vehicle_names = self.fleet_comp_data[FLEET_COMP_VEH_NAME]
        pollutants = list(PollutantType)

        for veh_name, poll in product(vehicle_names, pollutants):
            ef_data_reduce = ef_data[(ef_data["VehicleName"] == veh_name) &
                                     (ef_data["Pollutant"] == poll)]
            if ef_data_reduce.empty:
                missing_ef_data.append({"VehicleName": veh_name, "Pollutant": poll})

        return pd.DataFrame(missing_ef_data)


class HbefaEmissionFactorDataLoader:

    def __init__(self, **kwargs):
        """ Initialize a HbefaEmissionFactorDataLoader instance.

        You need to pass the following keyword argument:
        - ef_data : a pd.DataFrame containing emission factor data. It needs
                    to contain all the columns that are specified under
                    '# hbefa emission factor data' in 'column_names.py'.
        """

        self.ef_data = kwargs['ef_data']

    def load_data(self):

        yeti_format_ef_data = self.ef_data.rename(columns={
            HBEFA_EF_VEH_NAME: "VehicleName",
            HBEFA_EF_TRAFFIC_SIT: "TrafficSituation",
            HBEFA_EF_POLL: "Pollutant",
            HBEFA_EF_EF: "EF"
        })

        yeti_format_ef_data.loc[:,"Pollutant"] = yeti_format_ef_data["Pollutant"].apply(
            lambda poll: PollutantType.PM_Exhaust if str(poll) == "PM" else PollutantType.from_val(poll))

        return yeti_format_ef_data, None  # add None to return value for interchangability with EmissionFactorDataLoader
