from typing import Any, Dict, List


class Strategy:
    """
    The common superclass for all Strategies.

    This class defines 'calculate_emissions(...)' as the public interface that all Strategies should
    implement.
    It also implements a default behaviour for 'calculates_hot_and_cold_emissions(..)'. For details on this function
    see the function docstring below.
    """

    def calculate_emissions(self,
                            traffic_and_link_data_row: Dict[str, Any],
                            vehicle_dict: Dict[str, str],
                            pollutants: List[str],
                            **kwargs):

        raise NotImplementedError("Subclasses should override this method.")

    def calculates_hot_and_cold_emissions(self):
        """ Determine if a Strategy calculates hot **and** cold emissions.

        By default Strategies only calculate one kind of emissions. In most cases these
        are hot exhaust emissions **or** cold start exhaust emissions. Some Strategies (like the
        CopertColdStrategy) calculate and return both types of emissions.

        This method can be used by 'meta Strategies' that rely on other
        Strategies to calculate hot and cold emissions (like the HbefaStrategy) to find out if a given
        Strategy calculates hot and cold emissions. If yes the 'meta Strategy' will not have to call
        any more Strategies. If no the 'meta Strategy' will need to call another Strategy to calculate
        the missing emissions (hot/cold).

        Override this method in a subclass if the subclass calculates and returns both hot and cold emissions.
        """
        return False
