from ..powerplant import Powerplant

class Gasfired(Powerplant):
    """Produce electricity by firing gas (always available but costly)
    """

    def fuel_key(self, is_cost=True) -> str:
        if is_cost:
            return "gas(euro/MWh)"
        return None
    
    def tCO2_per_MWh(self):
        return 0.3