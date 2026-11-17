# Kart-Engine v2.3
import math
import pygame
from constants import (
    CAR_ACCELERATION, CAR_BRAKE_FORCE, CAR_DRAG, CAR_ROLLING_FRICTION,
    CAR_MAX_SPEED, CAR_MAX_REVERSE_SPEED, CAR_WHEELBASE, CAR_MAX_STEER,
    CAR_MIN_STEER, CAR_STEER_SPEED, CAR_STEER_RETURN, CAR_GRIP,
    CAR_SLIDE_FRICTION, CAR_MIN_TRACTION, DRIFT_EXIT_RATIO, DRIFT_SPEED_LOSS,
    SPEED_LIMIT_RECOVERY, BOOST_PUSH, CAR_WIDTH, CAR_HEIGHT, TILE_SIZE
)


class Car:
    """Voiture : position, vitesse, orientation, braquage et dérapage.

    Convention d'angle : en degrés, sens trigonométrique (anti-horaire).
    angle = 0 -> la voiture regarde vers le haut de l'écran,
    angle = 90 -> vers la gauche.

    La vitesse est un vecteur (vx, vy). Elle n'est pas forcément alignée
    avec l'orientation de la voiture : la partie perpendiculaire
    (vitesse latérale) correspond au dérapage.
    """

    def __init__(self, start_col: int, start_row: int):
        self.x = start_col * TILE_SIZE + TILE_SIZE // 2
        self.y = start_row * TILE_SIZE + TILE_SIZE // 2
        self.vx = 0.0
        self.vy = 0.0
        self.angle: float = 0.0
        # Angle des roues avant par rapport à la voiture (+ = vers la gauche)
        self.steer_angle: float = 0.0
        self.drifting = False
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

    # --- Repère lié à la voiture ---

    def forward_vector(self) -> tuple[float, float]:
        """Vecteur unitaire dans la direction où regarde la voiture."""
        rad = math.radians(self.angle)
        return -math.sin(rad), -math.cos(rad)

    def right_vector(self) -> tuple[float, float]:
        """Vecteur unitaire vers la droite de la voiture."""
        rad = math.radians(self.angle)
        return math.cos(rad), -math.sin(rad)

    @property
    def speed(self) -> float:
        """Vitesse dans l'axe de la voiture (négative en marche arrière)."""
        fx, fy = self.forward_vector()
        return self.vx * fx + self.vy * fy

    # --- Mise à jour ---

    def update(self, friction: float = 1.0,
               speed_multiplier: float = 1.0) -> None:
        """Avance la simulation d'une frame.

        friction et speed_multiplier viennent de la case sous la voiture
        (RoadTile). Par défaut, la voiture se comporte comme sur la route.
        """
        self.update_steering()
        self.update_angle()

        # On exprime la vitesse dans le repère de la voiture (après rotation)
        fx, fy = self.forward_vector()
        rx, ry = self.right_vector()
        v_long = self.vx * fx + self.vy * fy
        v_lat = self.vx * rx + self.vy * ry

        v_long = self.update_longitudinal(v_long, friction, speed_multiplier)
        v_lat, v_long = self.update_lateral(v_lat, v_long, friction)

        self.vx = v_long * fx + v_lat * rx
        self.vy = v_long * fy + v_lat * ry
        self.x += self.vx
        self.y += self.vy

        self.acceleration = 0.0
        self.steering = 0

    def max_steer_angle(self) -> float:
        """Angle de braquage maximal, plus faible quand on roule vite.

        Comme sur une vraie voiture, on ne peut pas braquer à fond à haute
        vitesse : l'angle max passe de CAR_MAX_STEER à l'arrêt à
        CAR_MIN_STEER à la vitesse maximale.
        """
        ratio = min(1.0, abs(self.speed) / CAR_MAX_SPEED)
        return CAR_MAX_STEER - (CAR_MAX_STEER - CAR_MIN_STEER) * ratio

    def update_steering(self) -> None:
        """Tourne les roues progressivement vers l'angle demandé.

        Le volant ne passe pas instantanément de 0 à fond : il tourne de
        CAR_STEER_SPEED degrés par frame, et revient vers le centre
        (un peu plus vite) quand on lâche les touches.
        """
        if self.steering != 0:
            target = self.steering * self.max_steer_angle()
            step = CAR_STEER_SPEED
        else:
            target = 0.0
            step = CAR_STEER_RETURN
        difference = target - self.steer_angle
        self.steer_angle += max(-step, min(step, difference))

    def update_angle(self) -> None:
        """Fait tourner la voiture avec le modèle « bicyclette ».

        Avec des roues braquées d'un angle d, la voiture suit un cercle de
        rayon R = empattement / tan(d). En avançant de v pixels, elle tourne
        donc de v / R radians. Conséquences :
        - à l'arrêt (v = 0) la voiture ne tourne pas ;
        - en marche arrière (v < 0) elle tourne dans l'autre sens ;
        - plus on va vite, plus on tourne vite, ce qui demande plus
          d'adhérence et peut faire déraper (voir update_lateral).
        """
        turn = (self.speed * math.tan(math.radians(self.steer_angle))
                / CAR_WHEELBASE)
        self.angle = (self.angle + math.degrees(turn)) % 360

    def update_longitudinal(self, v_long: float, friction: float,
                            speed_multiplier: float) -> float:
        """Accélération, frottements et limites de vitesse dans l'axe.

        - La traction dépend de la friction du terrain : on accélère et on
          freine moins bien sur la glace que sur la route.
        - La vitesse max est multipliée par speed_multiplier. Si la voiture
          arrive trop vite (ex. route -> herbe), elle ralentit progressivement.
        - Sur une case de boost (speed_multiplier > 1), elle est poussée vers
          l'avant.
        """
        traction = CAR_MIN_TRACTION + (1 - CAR_MIN_TRACTION) * friction
        v_long += self.acceleration * traction
        if speed_multiplier > 1:
            v_long += BOOST_PUSH

        # Frottements de l'air, proportionnels à la vitesse
        v_long -= CAR_DRAG * v_long
        # Sans accélération, un frottement constant arrête la voiture
        if self.acceleration == 0.0:
            v_long -= math.copysign(
                min(abs(v_long), CAR_ROLLING_FRICTION), v_long)

        max_speed = CAR_MAX_SPEED * speed_multiplier
        if v_long > max_speed:
            v_long -= (v_long - max_speed) * SPEED_LIMIT_RECOVERY
        return max(-CAR_MAX_REVERSE_SPEED * speed_multiplier, v_long)

    def update_lateral(self, v_lat: float, v_long: float,
                       friction: float) -> tuple[float, float]:
        """Gère l'adhérence et le dérapage. Renvoie (v_lat, v_long).

        Quand la voiture tourne, sa vitesse n'est plus tout à fait dans l'axe :
        il apparaît une vitesse latérale. Les pneus peuvent l'annuler tant
        qu'elle reste sous le seuil d'adhérence (CAR_GRIP * friction).
        Au-delà, ils décrochent et la voiture dérape :
        - la vitesse latérale n'est plus annulée d'un coup, elle diminue
          petit à petit avec le frottement de glisse du terrain ;
        - ce frottement freine aussi la voiture.
        La voiture arrête de déraper quand la vitesse latérale est redevenue
        nettement plus petite que le seuil (DRIFT_EXIT_RATIO).
        """
        grip = CAR_GRIP * friction
        slide_friction = CAR_SLIDE_FRICTION * friction

        v_lat -= CAR_DRAG * v_lat
        if not self.drifting and abs(v_lat) > grip:
            self.drifting = True

        if not self.drifting:
            # Adhérence : les pneus empêchent tout glissement sur le côté
            return 0.0, v_long

        v_lat *= 1 - slide_friction
        v_long *= 1 - slide_friction * DRIFT_SPEED_LOSS
        if abs(v_lat) < grip * DRIFT_EXIT_RATIO:
            self.drifting = False
        return v_lat, v_long

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
