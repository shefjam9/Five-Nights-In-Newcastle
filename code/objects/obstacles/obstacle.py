import pygame
from misc.logger import log
from objects.pos import Pos

class Obstacle:

    def __init__(self, time, x, y, player):
        self.placementTime = time
        self.start_x, self.start_y = x, y
        self._fade_in_time = 1e3
        self._fade_in_radius = 5
        self.player = player
        self.rect = pygame.Rect(x, y, 64, 64)
        self.surf = pygame.Surface((64, 64), pygame.SRCALPHA)
        self.rel = Pos(x, y)

    def update(keys_pressed, time):
        raise NotImplementedError("Obstacle needs update method")
    
    def adjust_position(self):
        self.rect.x = self.player.obj_offset.x + self.start_x
        self.rect.y = self.player.obj_offset.y + self.start_y

    def fade_in(self, time) -> bool:
        if time - self.placementTime <= self._fade_in_time:
            self._fade_in_radius = min(15 * ((time - self.placementTime)/1e3)*2, 32)
            return True
        return False
