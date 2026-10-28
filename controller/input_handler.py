# Kart-Engine v2.3
import pygame

# Actions possibles pour un joueur
ACTIONS = ("accelerate", "brake", "left", "right")

# Touches de chaque joueur (Z/W et Q/A pour couvrir AZERTY et QWERTY)
MAPPINGS = {
    1: {
        pygame.K_z: "accelerate",
        pygame.K_w: "accelerate",
        pygame.K_s: "brake",
        pygame.K_q: "left",
        pygame.K_a: "left",
        pygame.K_d: "right",
    },
    2: {
        pygame.K_UP: "accelerate",
        pygame.K_DOWN: "brake",
        pygame.K_LEFT: "left",
        pygame.K_RIGHT: "right",
    },
}


class InputHandler:
    """Traduit l'état du clavier en actions de jeu pour un joueur donné."""

    def __init__(self):
        self.mappings = MAPPINGS

    def get_inputs(self, player: int = 1) -> dict:
        """Retourne {action: bool} pour le joueur (1 ou 2)."""
        keys = pygame.key.get_pressed()
        inputs = {action: False for action in ACTIONS}

        for key, action in self.mappings[player].items():
            if keys[key]:
                inputs[action] = True

        return inputs
