# Kart-Engine v2.3
from model.road_tile import RoadTile
from constants import TILE_SIZE
from constants import TILE_SIZE, VOID, CHECKPOINT


class Circuit:

    def __init__(self,  grid: list[list[RoadTile]]):
        self.passed_checkpoints = {}    #Pour retenir quels checkpoints chaque voiture a déjà traversés.
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0]) if grid else 0

    def get_tile(self, col: int, row: int) -> RoadTile | None:
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.grid[row][col]
        return None

    def get_tile_at_pixel(self, px: float, py: float) -> RoadTile | None:
        col = int(px // TILE_SIZE)
        row = int(py // TILE_SIZE)
        return self.get_tile(col, row)
    
    def check_checkpoint(self, car) -> None:
        """Enregistre le passage de la voiture sur un checkpoint."""
        tile = self.get_tile_at_pixel(car.x, car.y)
        if tile is not None and tile.tile_type == CHECKPOINT:
            car_id = id(car)
            if car_id not in self.passed_checkpoints:
                self.passed_checkpoints[car_id] = set()

            pos = (tile.col, tile.row)
            if pos not in self.passed_checkpoints[car_id]:
                self.passed_checkpoints[car_id].add(pos)
                print("Checkpoint validé !")

    def pixel_width(self) -> int:
        return self.cols * TILE_SIZE

    def pixel_height(self) -> int:
        return self.rows * TILE_SIZE
