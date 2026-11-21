"""Tests des terrains et de la logique du circuit.

Lancer depuis la racine du projet : python -m pytest tests
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import constants
from model.road_tile import RoadTile
from model.car import Car
from model.circuit import Circuit



def test_road_tile_terrain_effects():
    road = RoadTile(0, 0, constants.ROAD)
    grass = RoadTile(1, 0, constants.GRASS)
    ice = RoadTile(2, 0, constants.ICE)

    assert road.friction == 1.0 and road.speed_multiplier == 1.0
    assert grass.speed_multiplier < road.speed_multiplier
    assert ice.friction < road.friction

def test_checkpoint_and_lap_validation():
    # Mini circuit d'1 ligne : Route (col 0), Checkpoint (col 1), Arrivée (col 2)
    grid = [[
        RoadTile(0, 0, constants.ROAD),
        RoadTile(1, 0, constants.CHECKPOINT),
        RoadTile(2, 0, constants.FINISH),
    ]]
    circuit = Circuit(grid)
    car = Car(2, 0)

    # 1. Anti-triche : passer sur l'arrivée sans checkpoint ne valide pas de tour
    circuit.check_checkpoint(car)
    assert circuit.laps.get(id(car), 0) == 0

    # 2. Passage sur le checkpoint (col 1)
    car.x = 1.5 * constants.TILE_SIZE
    circuit.check_checkpoint(car)
    assert len(circuit.passed_checkpoints[id(car)]) == 1

    # 3. Retour sur l'arrivée (col 2) : le tour 1 est validé et les checkpoints remis à zéro
    car.x = 2.5 * constants.TILE_SIZE
    circuit.check_checkpoint(car)
    assert circuit.laps[id(car)] == 1
    assert len(circuit.passed_checkpoints[id(car)]) == 0



def test_multiple_checkpoints_and_two_cars():
    # Mini circuit avec 2 checkpoints (cols 0 et 1) et une ligne d'arrivée (col 2)
    grid = [[
        RoadTile(0, 0, constants.CHECKPOINT),
        RoadTile(1, 0, constants.CHECKPOINT),
        RoadTile(2, 0, constants.FINISH),
    ]]
    circuit = Circuit(grid)
    car1 = Car(0, 0)
    car2 = Car(2, 0)

    assert circuit.total_checkpoints == 2

    # Voiture 1 passe seulement sur le 1er checkpoint puis sur l'arrivée : tour non validé
    circuit.check_checkpoint(car1)
    car1.x = 2.5 * constants.TILE_SIZE
    circuit.check_checkpoint(car1)
    assert circuit.laps.get(id(car1), 0) == 0

    # Voiture 1 valide le 2e checkpoint puis repasse sur l'arrivée : tour 1 validé
    car1.x = 1.5 * constants.TILE_SIZE
    circuit.check_checkpoint(car1)
    car1.x = 2.5 * constants.TILE_SIZE
    circuit.check_checkpoint(car1)
    assert circuit.laps[id(car1)] == 1

    # Voiture 2 (restée sur l'arrivée) ne doit pas bénéficier des checkpoints de Voiture 1
    circuit.check_checkpoint(car2)
    assert circuit.laps.get(id(car2), 0) == 0
    
if __name__ == "__main__":
    for name, func in list(globals().items()):
        if name.startswith("test_"):
            func()
            print("OK", name)