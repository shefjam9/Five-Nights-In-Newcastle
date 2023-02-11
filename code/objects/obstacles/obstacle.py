import pygame
from misc.logger import log

class Obstacle:

    def __init__(self, time, x, y):
        self.placementTime = time
        self.start_x, self.start_y = x, y
        self._fade_in_time = 1e3
        self._fade_in_radius = 5
        self.rect = pygame.Rect(x, y, 64, 64)
        self.surf = pygame.Surface((64, 64), pygame.SRCALPHA)

    def update(keys_pressed, time):
        raise NotImplementedError("Obstacle needs update method")

    def fade_in(self, time) -> bool:
        if time - self.placementTime <= self._fade_in_time:
            self._fade_in_radius = min(5 * ((time - self.placementTime)/1e3)*2, 32)
            return True
        return False