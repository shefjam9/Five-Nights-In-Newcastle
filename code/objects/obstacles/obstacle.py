import pygame
from misc.logger import log
from objects.pos import Pos

class Obstacle:

    def __init__(self, time, x, y, w, h, player):
        self.placementTime = time
        self.start_x, self.start_y = x, y
        self.width, self.height = w, h
        self._fade_in_time = 1e3
        self._fade_in_radius = 5
        self.player = player
        self.rect = pygame.Rect(x, y, w, h)
        self.surf = pygame.Surface((w, h), pygame.SRCALPHA)
        self.rel = Pos(x, y)

    def update(keys_pressed, time):
        raise NotImplementedError("Obstacle needs update method")

    def fade_in(self, time) -> bool:
        if time - self.placementTime <= self._fade_in_time:
            self._fade_in_radius = min(15 * ((time - self.placementTime)/1e3)*2, 32)
            return True
        return False
