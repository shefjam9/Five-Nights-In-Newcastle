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
        self.movement_amount = Pos(0, 0)
        self.damage_amount = 0
        self.has_damaged = False

    def update(keys_pressed, time):
        raise NotImplementedError("Obstacle needs update method")
    
    def adjust_position(self):
        rel_x = self.player.obj_offset.x + self.start_x
        rel_y = self.player.obj_offset.y + self.start_y
        self.rect.x = rel_x + self.movement_amount.x
        self.rect.y = rel_y + self.movement_amount.y

    def move(self, x_amount, y_amount):
        self.movement_amount.x += x_amount
        self.movement_amount.y += y_amount

    def fade_in(self, time) -> bool:
        if time - self.placementTime <= self._fade_in_time:
            self._fade_in_radius = min(15 * ((time - self.placementTime)/1e3)*2, 32)
            return True
        return False
