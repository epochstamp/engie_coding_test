# Coding Challenge from ENGIE, completed by Samy Aittahar

## Description

Deliverable for the [coding test provided by ENGIE ](https://github.com/gem-spaas/powerplant-coding-challenge/tree/master). Given a target load and available power plants with constraints such as min power, max power and availability (for renewable energy), provide a control strategy of the power plant so as to minimise the overall electricity production bill while exactly matching the target load. Service available via a REST API as requested (see instructions below). Also optimise CO2 emissions if option activated (see instructions below).

## Getting started

### Prerequisites

Dependencies listed in requirements.txt. Runs on Python 3.8+, tested on Linux. Docker is available as well.

### Install and use

- Install Python 3.8+;
- Run the command `python -m pip install -r requirements.txt`;
- Either run `expose_api_debug.sh [activate_CO2]`, where the option `activate_CO2` can be either `1` (enabled) or `0`(disabled, default) to expose the RestAPI in a debug setting (also display the cost for each powerplant along with electricity production) or `expose_api_production.sh [activate_cO2]` to expose the RestAPI in a production setting (only display the electricity production for each powerplant);
- Running one of the abovementioned scripts provide the PID of the RestAPI, keep it to kill later;
- Test with `test_api_{n}.py` with `{n}` in `(1, 2, 3)` (Input : `payload{n}.json` injected in POST request, output json structured like `response.json` example).
- [RestAPI link (localhost)](http://127.0.0.1:8888/productionplan).

A Dockerfile is also available in this archive (but untested), and should perform the abovementioned steps.
