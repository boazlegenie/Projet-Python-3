# Kart-Engine v2.3
from constants import GameState, GameMode, GRID_ROWS, GRID_COLS, VOID, TILE_SIZE
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
       # Circuit classique : Tracé Grand Prix (Route 0, Herbe 1, Boost 5, Arrivée 6, Checkpoints 7)
        layout = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 5, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
            [1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
            [1, 0, 1, 1, 0, 0, 7, 0, 0, 1, 1, 0, 0, 0, 0, 1],
            [1, 5, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
            [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
            [1, 7, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 6, 5, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ]
        
        if self.index_circuit == 1:
            # Circuit 1 : Route (0), Herbe (1), Terre (2), Glace (3), Boost (5), Arrivée (6), Checkpoint (7)
            layout = [
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 3, 3, 3, 3, 3, 3, 7, 3, 3, 3, 3, 3, 3, 3, 1],
                [1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1],
                [1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1],
                [1, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 1],
                [1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1],
                [1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1],
                [1, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 1],
                [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
                [1, 0, 0, 0, 0, 0, 6, 5, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            ]
            
        elif self.index_circuit == 2:
            # Circuit 2 : Piste au-dessus du Vide (4) avec Glace (3), Boosts (5) et 2 Checkpoints (7)
            layout = [
                [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
                [4, 0, 0, 0, 5, 0, 0, 7, 0, 0, 0, 5, 0, 0, 0, 4],
                [4, 0, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0, 4],
                [4, 0, 4, 4, 4, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 4],
                [4, 0, 0, 0, 0, 0, 4, 4, 4, 4, 3, 4, 4, 4, 4, 4],
                [4, 4, 4, 4, 4, 7, 4, 4, 4, 4, 3, 4, 4, 4, 4, 4],
                [4, 0, 0, 0, 0, 0, 4, 4, 4, 4, 0, 0, 0, 0, 0, 4],
                [4, 0, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0, 4],
                [4, 0, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0, 4],
                [4, 0, 0, 0, 0, 0, 6, 5, 0, 0, 0, 0, 0, 0, 0, 4],
                [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
                [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            ]
        
        grid = []
        for row_idx, row in enumerate(layout):
            grid_row = []
            for col_idx, tile_type in enumerate(row):
                grid_row.append(RoadTile(col_idx, row_idx, tile_type))
            grid.append(grid_row)
        
        
        # Création du circuit final
        self.circuit = Circuit(grid=grid)
        # On place la voiture sur la ligne de départ
        self.spawn_car()

    def spawn_car(self) -> None:
        # On place les voitures sur la route, juste avant la ligne d'arrivée    
        self.car = Car(5, 9)    
        self.last_safe_pos = {id(self.car): (self.car.x, self.car.y)}
        if self.mode == GameMode.MULTIJOUEUR:
            self.car2 = Car(4, 9)
            self.last_safe_pos[id(self.car2)] = (self.car2.x, self.car2.y)
            

    def update(self) -> None:
        if self.state != GameState.RACING or self.circuit is None:
            return
        self.update_car(self.car)

        if self.mode == GameMode.MULTIJOUEUR and hasattr(self, 'car2'):
            self.update_car(self.car2)

    def update_car(self, car: Car) -> None:    
        """Met à jour une voiture avec les propriétés de la case où elle roule."""
        tile = self.circuit.get_tile_at_pixel(car.x, car.y)

        # Chute dans le vide ou sortie de la carte -> respawn sur la dernière case sûre
        if tile is None or tile.tile_type == VOID:
            safe_x, safe_y = self.last_safe_pos.get(id(car), (car.x, car.y))
            car.x, car.y = safe_x, safe_y
            car.vx = 0.0
            car.vy = 0.0
            car.steer_angle = 0.0
            car.drifting = False
            return

        # Mémorise le centre de la dernière case sûre
        self.last_safe_pos[id(car)] = (
            tile.col * TILE_SIZE + TILE_SIZE // 2,
            tile.row * TILE_SIZE + TILE_SIZE // 2,
        )
        car.update(tile.friction, tile.speed_multiplier)
        self.circuit.check_checkpoint(car)