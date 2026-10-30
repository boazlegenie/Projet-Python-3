# Kart-Engine v2.3
import pygame
from constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, TILE_SIZE,
    COLOR_BG, COLOR_TEXT, COLOR_ACCENT, COLOR_PANEL, COLOR_PANEL_BORDER,
    GameState
)
from model.game_model import GameModel


class GameView:

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 24)

    def draw(self, model: GameModel) -> None:
        self.screen.fill(COLOR_BG)
        if model.state == GameState.MENU:
            self._draw_menu(model)
        elif model.state == GameState.SELECT_CIRCUIT:
            self._draw_select_circuit(model)
        elif model.state == GameState.RACING:
            self._draw_racing(model)
        pygame.display.flip()

    def _draw_select_circuit(self, model: GameModel) -> None:
        """ L'interface de sélection des circuits """
        cx = WINDOW_WIDTH // 2

        # Titre de la page
        title_surf = self.font.render("Sélectionnez un Circuit", True, COLOR_ACCENT)
        self.screen.blit(title_surf, title_surf.get_rect(center=(cx, 120)))

        # Affichage des cartes/boutons de chaque circuit
        # Utilisation de model.choix_circuits et model.index_circuit
        for i, circuit_name in enumerate(model.choix_circuits):
            y = 240 + i * 80
            rect = pygame.Rect(cx - 180, y - 25, 360, 50)

            # Surligner le circuit sélectionné
            is_selected = (i == model.index_circuit)
            bg_color = COLOR_ACCENT if is_selected else COLOR_PANEL
            text_color = (0, 0, 0) if is_selected else COLOR_TEXT

            pygame.draw.rect(self.screen, bg_color, rect, border_radius=8)
            pygame.draw.rect(self.screen, COLOR_PANEL_BORDER, rect, 2, border_radius=8)

            text_surf = self.font.render(circuit_name, True, text_color)
            self.screen.blit(text_surf, text_surf.get_rect(center=rect.center))

        # Instructions en bas de l'écran
        info = self.font.render("Flèches: Naviguer | Entrée: Valider | Echap: Retour", True, COLOR_TEXT)
        self.screen.blit(info, info.get_rect(center=(cx, WINDOW_HEIGHT - 80)))

    def _draw_menu(self, model: GameModel) -> None:
        cx = WINDOW_WIDTH // 2

        title_surf = self.font.render(
            "Jeu de course 2D", True, COLOR_ACCENT)
        self.screen.blit(title_surf, title_surf.get_rect(center=(cx, 160)))

        options = [("JOUER (Enter)", GameState.RACING),
                   ("QUITTER (Escape)", None)]
        for i, (label, _) in enumerate(options):
            y = 320 + i * 80
            rect = pygame.Rect(cx - 140, y - 25, 280, 50)
            pygame.draw.rect(self.screen, COLOR_PANEL, rect, border_radius=8)
            pygame.draw.rect(self.screen, COLOR_PANEL_BORDER,
                             rect, 2, border_radius=8)
            text_surf = self.font.render(
                label, True, COLOR_ACCENT if i == 0 else COLOR_TEXT)
            self.screen.blit(text_surf, text_surf.get_rect(center=rect.center))

    def _draw_racing(self, model: GameModel) -> None:
        if model.circuit is None:
            return

        for row_idx, row in enumerate(model.circuit.grid):
            for col_idx, tile in enumerate(row):
                sprite = tile.get_sprite(TILE_SIZE)
                self.screen.blit(
                    sprite, (col_idx * TILE_SIZE, row_idx * TILE_SIZE))

        surf, rect = model.car.get_rotated_sprite()
        self.screen.blit(surf, rect)