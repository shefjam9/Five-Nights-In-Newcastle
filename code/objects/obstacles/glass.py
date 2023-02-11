import pygame
from objects.obstacles.obstacle import Obstacle
from misc.logger import log

class Glass(Obstacle):

    def __init__(self, time: float, x: int, y: int):
        super().__init__(time, x, y)
        self.image = pygame.image.load("assets/Bottle.png").convert()
        self.texture = pygame.transform.scale(self.image, (64, 64))
        self.filled = False

    def update(self, keys, time):
       if super().fade_in(time):
           self.surf.fill(0)
           pygame.draw.circle(self.surf, (255, 0, 0, 50), (32, 32), self._fade_in_radius)
           return
       if not self.filled:
          self.surf.blit(self.texture)
          self.filled = True
       