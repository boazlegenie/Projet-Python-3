# Kart-Engine v2.3
from model.road_tile import RoadTile
from constants import TILE_SIZE
from constants import TILE_SIZE, VOID, CHECKPOINT, FINISH


class Circuit:

    def __init__(self,  grid: list[list[RoadTile]]):
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0]) if grid else 0
        self.passed_checkpoints = {}    #Pour retenir quels checkpoints chaque voiture a déjà traversés.
        self.laps = {}
        self.total_checkpoints = self._count_checkpoints()
        
    def _count_checkpoints(self) -> int:
        count = 0
        for row in self.grid:
            for tile in row:
                if tile.tile_type == CHECKPOINT:
                    count += 1
        return count

    def get_tile(self, col: int, row: int) -> RoadTile | None:
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.grid[row][col]
        return None

    def get_tile_at_pixel(self, px: float, py: float) -> RoadTile | None:
        col = int(px // TILE_SIZE)
        row = int(py // TILE_SIZE)
        return self.get_tile(col, row)
    
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
        return self.cols * TILE_SIZE

    def pixel_height(self) -> int:
        return self.rows * TILE_SIZE
