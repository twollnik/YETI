import numpy as np
import pandas as pd


def load_copert_hot_yeti_format_data(**kwargs):
    """ Load data from file. """

    emission_factor_data_file = kwargs.get('yeti_format_emission_factors')
    los_speeds_data_file = kwargs.get('yeti_format_los_speeds')
    vehicle_data_file = kwargs.get('yeti_format_vehicle_data')
    link_data_file = kwargs.get('yeti_format_link_data')
    traffic_data_file = kwargs.get('yeti_format_traffic_data')
    traffic_data_n_rows = kwargs.get('use_n_traffic_data_rows')

    emission_factor_data = pd.read_csv(emission_factor_data_file,
                                       dtype={"Pollutant": "category", "VehicleName": str})

    vehicle_data = pd.read_csv(vehicle_data_file,
                               dtype={"VehicleName": str, "VehicleCategory": "category",
                                      "RoadType": "category", "AreaType": "category"})

    link_data = pd.read_csv(link_data_file,
                            dtype={"LinkID": str})

    vehicle_names = list(vehicle_data.VehicleName)

    traffic_data = pd.read_csv(
        traffic_data_file,
        dtype={"LinkID": str, "Dir": "category", "DayType": "category", "Hour": np.int8,
               **{veh_name: np.float32 for veh_name in vehicle_names},
               **{f"LOS{i}Percentage": np.float32 for i in range(1, 5)}},
        nrows=traffic_data_n_rows
    )

    los_speeds_data = pd.read_csv(los_speeds_data_file,
                                  dtype={"LinkID": str, "VehicleCategory": "category", "LOSType": "category",
                                         "LOS1": float, "LOS2": float, "LOS3": float, "LOS4": float})

    return {
        "link_data": link_data,
        "vehicle_data": vehicle_data,
        "traffic_data": traffic_data,
        "los_speeds_data": los_speeds_data,
        "emission_factor_data": emission_factor_data
    }