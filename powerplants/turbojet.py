from ..powerplant import Powerplant

class Turbojet(Powerplant):
    """Produce electricity by firing kerosine (always available but costly)
    """

    def fuel_key(self, is_cost=True) -> str:
        if is_cost:
            return "kerosine(euro/MWh)"
        return None