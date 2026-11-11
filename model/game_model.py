# Kart-Engine v2.3
from constants import GameState, GameMode, GRID_ROWS, GRID_COLS
from model.car import Car
from model.circuit import Circuit
from model.road_tile import RoadTile


class GameModel:

    def __init__(self):
        self.state: str = GameState.MENU
        self.mode: str = GameMode.SOLO      # mode sélectionné par défaut
        self.circuit: Circuit | None = None
        self.car: Car | None = None

        self.menu_index = 0                  # option du menu actuellement surlignée

        #Liste des circuits
        self.choix_circuits = ["Circuit classique", "Circuit 1", "Circuit 2"]
        self.index_circuit = 0

    def select_next_menu_option(self) -> None:
        self.menu_index = (self.menu_index + 1) % 3   # on passe à l'option suivante

    def select_previous_menu_option(self) -> None:
        self.menu_index = (self.menu_index - 1) % 3   # on revient à l'option précédente

    def get_selected_menu_mode(self) -> str:
        options = [GameMode.SOLO, GameMode.MULTIJOUEUR, None]   # 3 options du menu
        if self.menu_index >= len(options):
            return GameMode.SOLO
        return options[self.menu_index]

    def select_next_circuit(self) -> None:
        """Circuit suivant"""
        self.index_circuit = (self.index_circuit + 1) % len(self.choix_circuits)

    def select_previous_circuit(self) -> None:
        """Circuit précédent"""
        self.index_circuit = (self.index_circuit - 1) % len(self.choix_circuits)

    def load_circuit(self) -> None:
        # grid[row][col] : lignes en premier, colonnes ensuite
        grid = [[RoadTile(col=col_idx, row=row_idx)
                for col_idx in range(GRID_COLS)] for row_idx in range(GRID_ROWS)]
        self.circuit = Circuit(grid=grid)
        self.spawn_car()

    def spawn_car(self) -> None:
        # Départ en bas de la grille, voiture tournée vers le haut
        self.car = Car(1, 10)  # position initiale de la voiture

        if self.mode == GameMode.MULTIJOUEUR:
            self.car2 = Car(2, 4)  # ajouter une deuxième voiture pour le mode multijoueur

    def update(self) -> None:
        if self.state != GameState.RACING or self.circuit is None:
            return
        self.car.update()

        if self.mode == GameMode.MULTIJOUEUR and hasattr(self, 'car2'):
            self.car2.update()