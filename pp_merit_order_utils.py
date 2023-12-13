from typing import Dict, List, Tuple, Callable

from .powerplant import Powerplant
from . import powerplants_class_map 
import numpy as np

class NotFeasibleException(BaseException):
    pass


def create_production_key_sorting(fuels: Dict[str, float], activate_CO2:bool = False, criterion_type: int=0) -> Callable[[Powerplant], Tuple[float, float, float, float]]:
    """ Create the function sorting the power plants in the following lexicographic order:
        Cost of generation taking into account efficiency(ASC), then minimum power (ASC), then maximum power (DESC) 

    Args:
        fuels (Dict[str, float]): Mapping between fuel cost/availability name and value
        activate_CO2 (bool): Whether to activate CO2 criterion
        criterion_type (int): Whether to sort first by efficiency after accounting cost per MWh (=0) of by power min (=1, in case 0 fails to fulfill the load)

    Returns
        Callable[[Powerplant], Tuple[float, float, float]]
        A function that returns the lexicographic values as explained in the synopsis
    """
    def production_key_sorting(powerplant_tuple: Tuple[str, Powerplant]) -> Tuple[float, float, float]:
        powerplant_name, powerplant = powerplant_tuple
        CO2_term = activate_CO2 * fuels.get("co2(euro/ton)", 0.0) * powerplant.tCO2_per_MWh()
        if criterion_type in (0,1):
            criterion_1 = (1*((fuels.get(powerplant.fuel_key(is_cost=True), 0.0) + CO2_term)))
        else:
            criterion_1 = 0
        if criterion_type in (0, 2):
            criterion_2 = -powerplant.efficiency
            criterion_3 = powerplant.pmin
        elif criterion_type == 1:
            criterion_3 = -powerplant.efficiency
            criterion_2 = powerplant.pmin
        return criterion_1, criterion_2, criterion_3
    return production_key_sorting

def production_plan(load:float, fuels:Dict[str, float], powerplants:Dict[str, Powerplant], powerplants_names=List[str], debug:bool = False, activate_CO2:bool = False) -> Dict[str, float]:
    """Return the electricity production power for each powerplant

    Args:
        load (float): The load consumption to satisfy with the powerplants
        fuels (Dict[str, float]): Cost(fossil) or availability(renewable) of fuels
        powerplants (Dict[str, Powerplant]): Powerplants objects with names
        debug (bool): Whether to be verbose in this function
        activate_co2: Whether to also optimise on Co2

    Returns:
        Dict[str, float]: The electricity power produced by each powerplant
    """
    #First consider wind 
    remaining_load = 1
    
    
    k = 0
    while remaining_load > 1e-6:
        remaining_load = load
        d_production_plan = []
        if debug:
            print("Criterion type", k)
        greedy_sorting_power_plants:List[Tuple[str, Powerplant]] = sorted(list(powerplants.items()), key=create_production_key_sorting(fuels, activate_CO2=activate_CO2, criterion_type=k))
        for powerplant_name, powerplant_obj in greedy_sorting_power_plants:
            fuel = fuels.get(powerplant_obj.fuel_key(is_cost=False), 1.0)
            pmax = powerplant_obj.pmax
            pmin = powerplant_obj.pmin
            max_prod = powerplant_obj.production(pmax, fuel)
            min_prod = powerplant_obj.production(pmin, fuel)
            if remaining_load == 0 or min_prod > remaining_load:
                prod = 0.0
                energy_prod = 0.0
            elif max_prod > remaining_load:
                curr_min_prod, curr_max_prod = pmin, pmax
                while curr_max_prod - curr_min_prod >= 1e-6:
                    prod = (curr_min_prod + curr_max_prod)/2
                    energy_prod = powerplant_obj.production(prod, fuel)
                    if energy_prod > remaining_load:
                        curr_max_prod = prod
                    else:
                        curr_min_prod = prod
                    
            else:
                prod = pmax
                energy_prod = max_prod
            prod = float(np.round(prod, 1))
            energy_prod = float(np.round(energy_prod, 1))
            remaining_load = remaining_load - energy_prod
            d_production_plan += [{
                "name": powerplant_name, "p":energy_prod
            }]
            if debug:
                print(f"Fuel amount of {powerplant_obj.fuel_key(is_cost=False)} is", fuel)
                print(f"Energy prod of {powerplant_name} is {energy_prod}")
                print(f"Prod of {powerplant_name} is {prod}")
                print("Remaining load", remaining_load)
        k += 1
    #while remaining_load >= 0.1:
        #i = 0
        #len_d_production_plan = len(d_production_plan)
        #while i != len_d_production_plan // 2:
            #j = len(len_d_production_plan) - i


            #i += 1
    if remaining_load >= 0.1:
        raise NotFeasibleException(f"Powerplants cannot entirely satisfy the whole load")
    return d_production_plan