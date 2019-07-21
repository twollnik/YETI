import pandas as pd


def load_hbefa_cold_yeti_format_data(**kwargs):

    return {
        "link_data": pd.read_csv(kwargs["yeti_format_link_data"]),
        "vehicle_data": pd.read_csv(kwargs["yeti_format_vehicle_data"]),
        "traffic_data": pd.read_csv(kwargs["yeti_format_cold_starts_data"]),
        "emission_factor_data": pd.read_csv(kwargs["yeti_format_emission_factors"])
    }