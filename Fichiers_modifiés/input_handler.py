import pygame


MAPPING = {
    pygame.K_UP:     "accelerate",
    
    pygame.K_DOWN:   "brake", #Ajout de la commande de freinage avec "brake" une méthode pour freiner qui va implémenter dans la class Car.
}


class InputHandler:

    def __init__(self):
        self.mapping = MAPPING

    def get_inputs(self) -> dict:
        keys = pygame.key.get_pressed()
        p = {action: False for action in self.mapping.values()}

        for key, action in self.mapping.items():
            if keys[key]:
                p[action] = True

        return p
