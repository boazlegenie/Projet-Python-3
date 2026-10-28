# Kart-Engine v2.3
import math
import pygame
from constants import (
    CAR_ACCELERATION, CAR_BRAKE_FORCE, CAR_DRAG, CAR_ROLLING_FRICTION,
    CAR_MAX_SPEED, CAR_MAX_REVERSE_SPEED, CAR_TURN_RATE, CAR_TURN_SPEED_REF,
    CAR_WIDTH, CAR_HEIGHT, TILE_SIZE
)


class Car:
    """Voiture : position, vitesse, orientation et dynamique de base.

    Convention d'angle : en degrés, sens trigonométrique (anti-horaire).
    angle = 0 -> la voiture regarde vers le haut de l'écran,
    angle = 90 -> vers la gauche.
    Une vitesse négative correspond à la marche arrière.
    """

    def __init__(self, start_col: int, start_row: int):
        self.x = start_col * TILE_SIZE + TILE_SIZE // 2
        self.y = start_row * TILE_SIZE + TILE_SIZE // 2
        self.speed: float = 0.0
        self.angle: float = 0.0
        # Commandes du joueur pour la frame courante (remises à zéro après update)
        self.acceleration: float = 0.0
        self.steering: int = 0
        self.sprite = self.build_sprite()

    # --- Commandes (appelées par le contrôleur) ---

    def accelerate(self) -> None:
        """Accélération longitudinale positive."""
        self.acceleration = CAR_ACCELERATION

    def brake(self) -> None:
        """Accélération longitudinale négative : freine, puis recule."""
        self.acceleration = -CAR_BRAKE_FORCE

    def turn_left(self) -> None:
        """Braquage à gauche (augmente l'angle)."""
        self.steering += 1

    def turn_right(self) -> None:
        """Braquage à droite (diminue l'angle)."""
        self.steering -= 1

    # --- Mise à jour ---

    def update(self) -> None:
        """Met à jour vitesse, orientation puis position pour une frame."""
        self.update_speed()
        self.update_angle()
        self.update_position()
        self.acceleration = 0.0
        self.steering = 0

    def update_speed(self) -> None:
        """Applique l'accélération, les frottements et les limites de vitesse."""
        self.speed += self.acceleration
        # Frottements de l'air, proportionnels à la vitesse
        self.speed -= CAR_DRAG * self.speed
        # Sans accélération, un frottement constant arrête la voiture
        if self.acceleration == 0.0:
            self.speed -= math.copysign(
                min(abs(self.speed), CAR_ROLLING_FRICTION), self.speed)
        self.speed = max(-CAR_MAX_REVERSE_SPEED,
                         min(CAR_MAX_SPEED, self.speed))

    def update_angle(self) -> None:
        """Fait tourner la voiture.

        La capacité à tourner dépend de la vitesse : nulle à l'arrêt et
        inversée en marche arrière, comme sur une vraie voiture.
        """
        turn_factor = max(-1.0, min(1.0, self.speed / CAR_TURN_SPEED_REF))
        self.angle = (self.angle
                      + self.steering * CAR_TURN_RATE * turn_factor) % 360

    def update_position(self) -> None:
        """Déplace la voiture dans la direction de son orientation."""
        rad = math.radians(self.angle)
        self.x += -math.sin(rad) * self.speed
        self.y += -math.cos(rad) * self.speed

    # --- Affichage ---

    def build_sprite(self) -> pygame.Surface:
        """Sprite provisoire : rectangle rouge avec un pare-brise à l'avant."""
        surf = pygame.Surface((CAR_WIDTH, CAR_HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(surf, (255, 0, 0), (0, 0, CAR_WIDTH,
                         CAR_HEIGHT), border_radius=5)
        pygame.draw.rect(surf, (255, 180, 180),
                         (4, 6, CAR_WIDTH - 8, 12), border_radius=3)
        return surf

    def get_rotated_sprite(self) -> tuple[pygame.Surface, pygame.Rect]:
        """Retourne le sprite tourné selon l'angle, et son rectangle centré."""
        rotated = pygame.transform.rotate(self.sprite, self.angle)
        rect = rotated.get_rect(center=(int(self.x), int(self.y)))
        return rotated, rect
