import pygame
from misc.logger import log
from objects.pos import Pos

from enum import IntFlag

class ObstacleID(IntFlag):
  """ Flag so can be used for efficient sending of multiple obstacles"""
  OBJ_NONE = (1<<0),
  OBJ_BOTTLE = (1<<1),
  OBJ_DRUNK = (1<<2),
  OBJ_SPOONS = (1<<3),
  OBJ_THUG = (1<<4),
  OBJ_POLICE = (1<<5),
  OBJ_PIGEON = (1<<6)

class Obstacle:

    def __init__(self, time, x, y, w, h, player, phys_rect: pygame.Rect = None):
        self.placementTime = time
        self.start_x, self.start_y = x, y
        self.width, self.height = w, h
        self._fade_in_time = 1e3
        self._fade_in_radius = 5
        self.player = player
        self.rect = pygame.Rect(x, y, w, h)
        if not phys_rect:
            self.phys_rect = self.rect
        else:
            self.phys_rect = phys_rect
        self.surf = pygame.Surface((w, h), pygame.SRCALPHA)
        self.rel = Pos(x, y)
        self.movement_amount = Pos(0, 0)
        self.damage_amount = 0
        self.last_damaged = -1
        # default damage every 1 second
        self.damage_time = 1e3

    def update(keys_pressed, time):
        raise NotImplementedError("Obstacle needs update method")
    
    def adjust_position(self):
        rel_x = self.player.obj_offset.x + self.start_x
        rel_y = self.player.obj_offset.y + self.start_y
        self.rect.x = rel_x + self.movement_amount.x
        self.rect.y = rel_y + self.movement_amount.y

        self.phys_rect.centerx = self.rect.centerx
        self.phys_rect.centery = self.rect.centery

    def move(self, x_amount, y_amount):
        self.movement_amount.x += x_amount
        self.movement_amount.y += y_amount
    
    def can_damage(self, time) -> bool:
        if not self.damage_amount:
            return False
        if time - self.last_damaged >= self.damage_time:
            return True
        return False
    
    def set_damaged(self, time):
        self.last_damaged = time

    def check_collision(self, color):
        """Check if obstacle collides with wall"""
        try:
            if self.player.bg_img.get_at((round(self.phys_rect.left - self.player.bg_tile[0]), round(self.phys_rect.top - self.player.bg_tile[1]))) == color:
                return True
            elif self.player.bg_img.get_at((round(self.phys_rect.left - self.player.bg_tile[0]), round(self.phys_rect.bottom - self.player.bg_tile[1]))) == color:
                return True
            elif self.player.bg_img.get_at((round(self.phys_rect.right - self.player.bg_tile[0]), round(self.phys_rect.top - self.player.bg_tile[1]))) == color:
                return True
            elif self.player.bg_img.get_at((round(self.phys_rect.right - self.player.bg_tile[0]), round(self.phys_rect.bottom - self.player.bg_tile[1]))) == color:
                return True
        except Exception as e:
            print(e)
        return False

    def fade_in(self, time) -> bool:
        if time - self.placementTime <= self._fade_in_time:
            self._fade_in_radius = min(15 * ((time - self.placementTime)/1e3)*2, 32)
            return True
        return False
