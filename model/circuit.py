# Kart-Engine v2.3
from model.road_tile import RoadTile
from constants import TILE_SIZE, CHECKPOINT, FINISH, START_1, START_2


class Circuit:
    """Gère la grille de cases du circuit, les checkpoints et le comptage des tours."""
    def __init__(self,  grid: list[list[RoadTile]]):
        """Initialise le circuit à partir d'une grille 2D de RoadTile."""
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0]) if grid else 0
        self.passed_checkpoints = {}    
        self.laps = {}
        self.total_checkpoints = self._count_checkpoints()
        
    def _count_checkpoints(self) -> int:
        """Compte le nombre total de cases de checkpoint présentes sur le circuit."""
        count = 0
        for row in self.grid:
            for tile in row:
                if tile.tile_type == CHECKPOINT:
                    count += 1
        return count

    def get_tile(self, col: int, row: int) -> RoadTile | None:
        """Retourne la case située sous les coordonnées pixels (px, py)."""
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.grid[row][col]
        return None

    def get_tile_at_pixel(self, px: float, py: float) -> RoadTile | None:
        """Retourne les coordonnées (col, row) du bloc de départ du joueur 1 ou 2."""
        col = int(px // TILE_SIZE)
        row = int(py // TILE_SIZE)
        return self.get_tile(col, row)
    
    def get_start_position(self, player: int) -> tuple[int, int]:
        """Retourne les coordonnées (col, row) du bloc de départ du joueur 1 ou 2."""
        target = START_1 if player == 1 else START_2
        for row in self.grid:
            for tile in row:
                if tile.tile_type == target:
                    return (tile.col, tile.row)
        return (5, 9) if player == 1 else (4, 9)
    
    def check_checkpoint(self, car) -> bool:
        """Enregistre un checkpoint et indique si un tour vient d'être validé."""
        tile = self.get_tile_at_pixel(car.x, car.y)
        if tile is not None and tile.tile_type == CHECKPOINT:
            car_id = id(car)
            if car_id not in self.passed_checkpoints:
                self.passed_checkpoints[car_id] = set()

            pos = (tile.col, tile.row)
            if pos not in self.passed_checkpoints[car_id]:
                self.passed_checkpoints[car_id].add(pos)
                print("Checkpoint validé !")
        elif tile is not None and tile.tile_type == FINISH:
            car_id = id(car)
            passed = self.passed_checkpoints.get(car_id, set())
            if len(passed) == self.total_checkpoints and self.total_checkpoints > 0:
                self.laps[car_id] = self.laps.get(car_id, 0) + 1
                self.passed_checkpoints[car_id].clear()
                print(f"Tour {self.laps[car_id]} terminé !")
                return True
        return False

    def pixel_width(self) -> int:
        """Retourne la largeur totale du circuit en pixels."""
        return self.cols * TILE_SIZE

    def pixel_height(self) -> int:
        """Retourne la hauteur totale du circuit en pixels."""
        return self.rows * TILE_SIZE
