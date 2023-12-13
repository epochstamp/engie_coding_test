class PowerOutsideBounds(BaseException):
    pass

class Powerplant(object):
    """Base class for representsing dynamics production of power plants given efficiency, pmin, pmax
    """
    def __init__(self, efficiency: float, pmin: float, pmax: float):
        """ Provides efficiency, power min and power max

        Args:
            efficiency (float): Efficiency (value \in ]0;1])
            pmin (float): Power min (> 0)
            pmax (float): Power max (>= Power min)
        """
        self._efficiency = efficiency
        self._pmin = pmin
        self._pmax = pmax

    @property
    def pmin(self):
        return self._pmin
    
    @property
    def pmax(self):
        return self._pmax
    
    @property
    def efficiency(self):
        return self._efficiency
    
    def tCO2_per_MWh(self):
        return 0.0

    def fuel_key(self, is_cost=True) -> str:
        """_summary_

        Args:
            is_cost (bool): Whether it is the cost that is needed or availability
        Raises:
            NotImplementedError: If this method is not implemented in subclass

        Returns:
            str: Key of the fuel used by this powerplant (Empty string if no need)
        """
        raise NotImplementedError()

    def production(self, power: float, fuel: float) -> float:
        """Returns the energy produced by power and fuel availability

        Args:
            power (float): _description_
            fuel (float): _description_

        Raises:
            PowerOutsideBounds: _description_

        Returns:
            float: Energy produced by the powerplant with power
        """
        if power >= 1e-6 and (power < self._pmin or power > self._pmax):
            raise PowerOutsideBounds(f"Value {power} is outside bounds defined by min power {self._pmin} and max power {self._pmax}")
        return power*fuel


    def cost(self, power: float, unit_cost: float) -> float:
        """Returns the cost of energy produced by power

        Args:
            pow (float): _description_
            unit_cost (float): _description_

        Raises:
            PowerOutsideBounds: _description_

        Returns:
            float: Cost for producing energy by the powerplant with power
        """
        if power >= 1e-6 and (power < self._pmin or power > self._pmax):
            raise PowerOutsideBounds(f"Value {power} is outside bounds defined by min power {self._pmin} and max power {self._pmax}")
        return (power*unit_cost)/self.efficiency