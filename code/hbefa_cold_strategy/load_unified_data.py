import pandas as pd


def load_hbefa_cold_unified_data(**kwargs):

    return {
        "link_data": pd.read_csv(kwargs["unified_link_data"]),
        "vehicle_data": pd.read_csv(kwargs["unified_vehicle_data"]),
        "cold_starts_data": pd.read_csv(kwargs["unified_cold_starts_data"]),
        "emission_factor_data": pd.read_csv(kwargs["unified_emission_factors"])
    }