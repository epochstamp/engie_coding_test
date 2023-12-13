from .gasfired import Gasfired
from .turbojet import Turbojet
from .windturbine import Windturbine

powerplants_class_map = {
    "gasfired": Gasfired,
    "turbojet": Turbojet,
    "windturbine": Windturbine
}