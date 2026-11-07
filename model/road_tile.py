# Kart-Engine v2.3
import pygame
import constants
from constants import TILE_SIZE


class RoadTile:
    # 1. On ajoute tile_type dans les paramètres 
    def __init__(self, col: int, row: int, tile_type: int = constants.ROAD):
        self.col = col
        self.row = row
        self.tile_type = tile_type #C'est une route par défaut.
        self.sprite: pygame.Surface | None = None
        
        # 2. Propriétés physiques de base (pour une route normale)
        self.friction = 1.0           
        self.speed_multiplier = 1.0   
        
        # On appelle une méthode pour modifier la physique selon le terrain
        self._apply_terrain_effects()

    def _apply_terrain_effects(self):
        """Ajuste l'adhérence et la vitesse selon le type de terrain."""
        if self.tile_type == constants.GRASS:
            self.friction = 0.5
            self.speed_multiplier = 0.4  # L'herbe ralentit la voiture
        elif self.tile_type == constants.ICE:
            self.friction = 0.05         # La glace fait glisser
            self.speed_multiplier = 1.0
        elif self.tile_type == constants.DIRT:
            self.friction = 0.7
            self.speed_multiplier = 0.8
        elif self.tile_type == constants.BOOST:
            self.friction = 1.0
            self.speed_multiplier = 2.0  # Le boost double la vitesse temporairement

    def get_sprite(self, tile_size: int = TILE_SIZE) -> pygame.Surface:
        if self.sprite and self.sprite.get_width() == tile_size:
            return self.sprite
        surface = pygame.Surface((tile_size, tile_size))
        
        # 3. Application de la couleur selon le type de terrain
        if self.tile_type == constants.GRASS:
            surface.fill((34, 139, 34))    # Vert forêt
        elif self.tile_type == constants.DIRT:
            surface.fill((139, 69, 19))    # Marron
        elif self.tile_type == constants.ICE:
            surface.fill((173, 216, 230))  # Bleu clair
        elif self.tile_type == constants.BOOST:
            surface.fill((255, 215, 0))    # Jaune
        elif self.tile_type == constants.VOID:
            surface.fill((0, 0, 0))        # Noir
        else:
        
        #Par défaut on a:
           surface.fill((80, 80, 90))
           pygame.draw.rect(surface, (60, 60, 70), surface.get_rect(), 2)

        self.sprite = surface
        return self.sprite
