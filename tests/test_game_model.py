import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import constants
from model.car import Car
from model.circuit import Circuit
from model.game_model import GameModel
from model.road_tile import RoadTile


def test_lap_selection_is_bounded_between_one_and_ten():
    model = GameModel()
    # Le nombre de tours proposé par défaut est 3.
    assert model.laps_to_win == 3

    # La sélection ne peut pas descendre sous 1.
    model.laps_to_win = 1
    model.select_previous_laps()
    assert model.laps_to_win == 1

    # La sélection ne peut pas dépasser 10.
    model.laps_to_win = 10
    model.select_next_laps()
    assert model.laps_to_win == 10


def test_lap_selection_can_be_adjusted():
    model = GameModel()

    # La flèche vers le haut ajoute un tour.
    model.select_next_laps()
    assert model.laps_to_win == 4

    # La flèche vers le bas retire un tour.
    model.select_previous_laps()
    assert model.laps_to_win == 3


def test_solo_race_ends_when_selected_lap_count_is_reached():
    model = GameModel()
    model.state = constants.GameState.RACING
    model.laps_to_win = 1
    model.circuit = Circuit([[
        RoadTile(0, 0, constants.CHECKPOINT),
        RoadTile(1, 0, constants.FINISH),
    ]])
    model.car = Car(0, 0)
    model.last_safe_pos = {id(model.car): (model.car.x, model.car.y)}

    # Le checkpoint est validé avant le passage sur la ligne d'arrivée.
    model.circuit.check_checkpoint(model.car)
    model.car.x = 1.5 * constants.TILE_SIZE
    model.update()

    assert model.state == constants.GameState.VICTOIRE
    assert model.winner == 1


def test_first_multiplayer_car_to_finish_wins():
    model = GameModel()
    model.state = constants.GameState.RACING
    model.mode = constants.GameMode.MULTIJOUEUR
    model.laps_to_win = 1
    model.circuit = Circuit([[
        RoadTile(0, 0, constants.CHECKPOINT),
        RoadTile(1, 0, constants.FINISH),
    ]])
    model.car = Car(0, 0)
    model.car2 = Car(0, 0)
    model.last_safe_pos = {
        id(model.car): (model.car.x, model.car.y),
        id(model.car2): (model.car2.x, model.car2.y),
    }

    # Le joueur 2 a validé le checkpoint et arrive sur la ligne d'arrivée.
    model.circuit.check_checkpoint(model.car2)
    model.car2.x = 1.5 * constants.TILE_SIZE
    model.update()

    assert model.state == constants.GameState.VICTOIRE
    assert model.winner == 2
