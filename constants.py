# Kart-Engine v2.3
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768
FPS = 60

TILE_SIZE = 64
GRID_COLS = 16
GRID_ROWS = 12

# --- TYPES DE TERRAINS ---
#On code les types de terrains avec un entier
ROAD = 0
GRASS = 1
DIRT = 2
ICE = 3
VOID = 4
BOOST = 5
FINISH = 6
CHECKPOINT = 7   #Vérifie que le jouer à bien fait le tour.
START_1 = 8      #On ajoute les 2 nouveaux types de blocs
START_2 = 9

# --- Dynamique de la voiture (unités : pixels et degrés, par frame) ---
CAR_ACCELERATION = 0.05         # accélération longitudinale en avançant
CAR_BRAKE_FORCE = 0.12          # décélération (négative) en freinant / reculant
CAR_DRAG = 0.01                 # frottements de l'air (proportionnels à la vitesse)
CAR_ROLLING_FRICTION = 0.02     # ralentissement quand aucune touche n'est pressée
CAR_MAX_SPEED = 6.0             # vitesse maximale en marche avant
CAR_MAX_REVERSE_SPEED = 2.5     # vitesse maximale en marche arrière

# --- Braquage (modèle « bicyclette ») ---
CAR_WHEELBASE = 34.0            # distance entre les essieux (pixels)
CAR_MAX_STEER = 32.0            # angle max des roues à l'arrêt (degrés)
CAR_MIN_STEER = 14.0            # angle max des roues à vitesse max (degrés)
CAR_STEER_SPEED = 3.0           # vitesse à laquelle on tourne le volant (degrés/frame)
CAR_STEER_RETURN = 5.0          # vitesse de retour du volant au centre (degrés/frame)

# --- Adhérence et dérapage (multipliés par la friction du terrain) ---
CAR_GRIP = 0.35                 # vitesse latérale max avant de déraper, sur route
CAR_SLIDE_FRICTION = 0.15       # part de la vitesse latérale perdue par frame en dérapage
CAR_MIN_TRACTION = 0.3          # traction minimale, même sur la glace
DRIFT_EXIT_RATIO = 0.5          # on sort du dérapage sous grip * ce ratio
DRIFT_SPEED_LOSS = 0.1          # part du frottement de glisse qui freine la voiture
SPEED_LIMIT_RECOVERY = 0.05     # vitesse à laquelle on revient sous la vitesse max du terrain
BOOST_PUSH = 0.2                # poussée par frame sur une case de boost

CAR_WIDTH = 30
CAR_HEIGHT = 50


class GameState:
    MENU = "menu"           # écran principal
    SELECT_CIRCUIT = "select_circuit"  # choix du circuit
    SELECT_LAPS = "select_laps"  # choix du nombre de tours
    RACING = "racing"       # partie en cours
    VICTOIRE = "victoire"   # course terminée
    


class GameMode:
    SOLO = "solo"           # mode solo
    MULTIJOUEUR = "multijoueur"  # mode multijoueur


# --- Couleurs UI ---
COLOR_BG = (15, 15, 25)
COLOR_TEXT = (240, 240, 240)
COLOR_ACCENT = (255, 200, 0)
COLOR_PANEL = (30, 30, 50)
COLOR_PANEL_BORDER = (60, 60, 100)
