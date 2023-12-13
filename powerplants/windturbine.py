from ..powerplant import Powerplant

class Windturbine(Powerplant):
    """Produce electricity from wind (no cost but not always available)
    """

    def fuel_key(self, is_cost=True) -> str:
        if not is_cost:
            return "wind(%)"
        return None