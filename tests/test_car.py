"""Tests de la physique de la voiture.

Lancer depuis la racine du projet : python -m pytest tests
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from model.car import Car

# (friction, speed_multiplier) des terrains définis dans RoadTile
ROAD = (1.0, 1.0)
GRASS = (0.5, 0.4)
ICE = (0.05, 1.0)


def run(car, frames, terrain=ROAD, accelerate=False, brake=False, left=False):
    """Simule plusieurs frames avec les touches indiquées maintenues."""
    for _ in range(frames):
        if accelerate:
            car.accelerate()
        if brake:
            car.brake()
        if left:
            car.turn_left()
        car.update(*terrain)


def test_accelerate_moves_forward():
    car = Car(5, 5)
    x0, y0 = car.x, car.y
    run(car, 30, accelerate=True)
    assert car.y < y0                 # angle 0 = vers le haut
    assert abs(car.x - x0) < 1e-6
    assert car.speed > 0


def test_brake_then_reverse():
    car = Car(5, 5)
    y0 = car.y
    run(car, 60, brake=True)
    assert car.speed < 0
    assert car.y > y0


def test_steering_is_progressive():
    car = Car(5, 5)
    run(car, 1, left=True)
    first = car.steer_angle
    run(car, 20, left=True)
    assert 0 < first < car.steer_angle
    run(car, 20)
    assert car.steer_angle == 0.0


def test_no_turn_when_stopped_and_inverted_in_reverse():
    car = Car(5, 5)
    run(car, 30, left=True)
    assert car.angle == 0
    run(car, 60, brake=True)
    run(car, 30, brake=True, left=True)
    assert 180 < car.angle < 360      # en reculant, l'avant part à droite


def drifts_in_turn(terrain):
    """Arrive lancé depuis la route puis tourne à fond sur le terrain."""
    car = Car(5, 5)
    run(car, 400, accelerate=True)
    drifted = False
    for _ in range(60):
        car.accelerate()
        car.turn_left()
        car.update(*terrain)
        drifted = drifted or car.drifting
    return drifted


def test_drift_depends_on_terrain():
    assert not drifts_in_turn(ROAD)
    assert drifts_in_turn(GRASS)
    assert drifts_in_turn(ICE)


def test_ice_keeps_sliding_after_turn():
    car = Car(5, 5)
    run(car, 400, accelerate=True)
    run(car, 60, terrain=ICE, accelerate=True, left=True)
    run(car, 60, terrain=ICE, accelerate=True)
    assert car.drifting


def test_grass_slows_car_down():
    car = Car(5, 5)
    run(car, 400, accelerate=True)
    fast = car.speed
    run(car, 200, terrain=GRASS, accelerate=True)
    assert car.speed < fast * 0.6


if __name__ == "__main__":
    for name, func in list(globals().items()):
        if name.startswith("test_"):
            func()
            print("OK", name)
