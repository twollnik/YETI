from typing import Any, Dict, List

from code.Strategy import Strategy


class MockStrategy(Strategy):

    def calculate_emissions(self,
                            traffic_and_link_data_row: Dict[str, Any],
                            vehicle_dict: Dict[str, str],
                            pollutants: List[str],
                            **kwargs):

        return {"poll": {"vehA": 100}}
