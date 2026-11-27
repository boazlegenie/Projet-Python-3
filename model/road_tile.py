# Kart-Engine v2.3
import pygame
import constants
from constants import TILE_SIZE


class RoadTile:
    """Représente une case du circuit avec son terrain et ses propriétés physiques."""
    def __init__(self, col: int, row: int, tile_type: int = constants.ROAD):
        """Initialise une case à sa position sur la grille et applique ses effets de terrain."""
        self.col = col
        self.row = row
        self.tile_type = tile_type 
        self.sprite: pygame.Surface | None = None
        
        # Propriétés physiques de base (route)
        self.friction = 1.0           
        self.speed_multiplier = 1.0   
        
        self._apply_terrain_effects()

    def _apply_terrain_effects(self):
        """Ajuste l'adhérence et la vitesse selon le type de terrain."""
        if self.tile_type == constants.GRASS:
            self.friction = 0.5
            self.speed_multiplier = 0.4 
        elif self.tile_type == constants.ICE:
            self.friction = 0.05         
            self.speed_multiplier = 1.0
        elif self.tile_type == constants.DIRT:
            self.friction = 0.7
            self.speed_multiplier = 0.8
        elif self.tile_type == constants.BOOST:
            self.friction = 1.0
            self.speed_multiplier = 2.0  

    def get_sprite(self, tile_size: int = TILE_SIZE) -> pygame.Surface:
        """Génère (et met en cache) la surface Pygame correspondant au type de case."""
        if self.sprite and self.sprite.get_width() == tile_size:
            return self.sprite
        surface = pygame.Surface((tile_size, tile_size))
        
        if self.tile_type == constants.GRASS:
            surface.fill((34, 139, 34))    
        elif self.tile_type == constants.DIRT:
            surface.fill((139, 69, 19))    
        elif self.tile_type == constants.ICE:
            surface.fill((173, 216, 230))  
        elif self.tile_type == constants.BOOST:
            surface.fill((255, 215, 0))    
        elif self.tile_type == constants.VOID:
            surface.fill((0, 0, 0))        
        elif self.tile_type == constants.FINISH:
            surface.fill((255, 255, 255))
            pygame.draw.rect(surface, (0, 0, 0), (0, 0, tile_size//2, tile_size//2))
            pygame.draw.rect(surface, (0, 0, 0), (tile_size//2, tile_size//2, tile_size//2, tile_size//2))
        elif self.tile_type == constants.CHECKPOINT:
            surface.fill((80, 80, 90))
            pygame.draw.rect(surface, (0, 200, 255), surface.get_rect(), 6)
            
        elif self.tile_type in (constants.START_1, constants.START_2):
            surface.fill((80, 80, 90))
            border_color = (220, 60, 60) if self.tile_type == constants.START_1 else (60, 140, 255)
            pygame.draw.rect(surface, border_color, (6, 6, tile_size - 12, tile_size - 12), 4)
        else:
           surface.fill((80, 80, 90))
           pygame.draw.rect(surface, (60, 60, 70), surface.get_rect(), 2)

        self.sprite = surface
        return self.sprite
           
