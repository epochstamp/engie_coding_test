from flask import Flask, request, jsonify
from .pp_merit_order_utils import production_plan
from typing import Dict
from .powerplant import Powerplant
from . import powerplants_class_map
import json
import os

app = Flask(__name__)

@app.post("/productionplan")
def productionplan():
    if request.is_json:
        data = request.get_json()
        if "load" not in data:
            return {"error": "load data must be in the request"}, 415
        if "fuels" not in data:
            return {"error": "fuels data must be in the request"}, 415
        if "powerplants" not in data:
            return {"error": "powerplants data must be in the request"}, 415
        activate_co2 = os.environ.get("ACTIVATE_CO2", "0") == "1"
        load = data["load"]
        fuels = {
            fuel_name:(fuel/100 if "(%)" in fuel_name else fuel) for fuel_name, fuel in data["fuels"].items()
        }
        power_plants: Dict[str, Powerplant] = {
            powerplant["name"]:powerplants_class_map[powerplant["type"]](powerplant["efficiency"], powerplant["pmin"], powerplant["pmax"]) for powerplant in data["powerplants"]
        }
        try:
            prod_per_power_plant = production_plan(load, fuels, power_plants, debug=app.debug, activate_CO2=activate_co2)
        except BaseException as e:
            return {"error": f"Some issue happened when computing production plan (details:{type(e)}, {e})"}, 415
        for power_plant in prod_per_power_plant:
            power_plant_name = power_plant["name"]
            power_plant_obj = power_plants[power_plant_name]
            power_plant_power = power_plant["p"]
            if power_plant_power >= 1e-6 and (
                power_plant_power < power_plant_obj.pmin
                or power_plant_power > power_plant_obj.pmax
            ):
                return {"error": f"Requested non-zero electricity production power for power plant {power_plant_name} with power {power_plant_power} is outside bounds [pmin={power_plant_obj.pmin}, pmax={power_plant_obj.pmax}]"}, 421


        total_production = sum(
            [
                power_plant["p"] for power_plant in prod_per_power_plant
            ]
        )
        if abs(data["load"] - total_production) >= 0.1:
            return {"error": f"Total production {total_production} MWh does not match load of {load} MWh"}, 321
        
        
        
        if app.debug:
            for power_plant in prod_per_power_plant:
                power_plant["cost"] = power_plants[power_plant["name"]].cost(
                    power_plant["p"], fuels.get(power_plants[power_plant["name"]].fuel_key(
                        is_cost=True
                    ), 0.0)   
                ) + (activate_co2*power_plant["p"]*fuels.get("co2(euro/ton)", 0.0)*power_plants[power_plant["name"]].tCO2_per_MWh()/power_plants[power_plant["name"]].efficiency)
        return prod_per_power_plant, 200
    return {"error": "Request must be JSON"}, 415