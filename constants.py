# Kart-Engine v2.3
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768
FPS = 60

TILE_SIZE = 64
GRID_COLS = 16
GRID_ROWS = 12

# --- Dynamique de la voiture (unités : pixels et degrés, par frame) ---
CAR_ACCELERATION = 0.05         # accélération longitudinale en avançant
CAR_BRAKE_FORCE = 0.12          # décélération (négative) en freinant / reculant
CAR_DRAG = 0.01                 # frottements de l'air (proportionnels à la vitesse)
CAR_ROLLING_FRICTION = 0.02     # ralentissement quand aucune touche n'est pressée
CAR_MAX_SPEED = 6.0             # vitesse maximale en marche avant
CAR_MAX_REVERSE_SPEED = 2.5     # vitesse maximale en marche arrière
CAR_TURN_RATE = 3.0             # rotation maximale par frame (degrés)
CAR_TURN_SPEED_REF = 2.0        # vitesse à partir de laquelle on tourne à fond

CAR_WIDTH = 30
CAR_HEIGHT = 50


class GameState:
    MENU = "menu"
    RACING = "racing"


# --- Couleurs UI ---
COLOR_BG = (15, 15, 25)
COLOR_TEXT = (240, 240, 240)
COLOR_ACCENT = (255, 200, 0)
COLOR_PANEL = (30, 30, 50)
COLOR_PANEL_BORDER = (60, 60, 100)
