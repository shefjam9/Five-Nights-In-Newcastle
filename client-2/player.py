import globals
import pygame
import random

class Player:

  def __init__(self, net_message):
    self._x = 200
    self._y = 200
  
  def render(self, surface: pygame.Surface):
    pygame.draw.rect(surface, (150, 75, 0), (self._x, self._y, globals.TILE_SIZE/2, globals.TILE_SIZE/2))
  
  def update(self, time):
    self._x +=10*(random.random()-0.5)
    self._y += 10*(random.random()-0.5)