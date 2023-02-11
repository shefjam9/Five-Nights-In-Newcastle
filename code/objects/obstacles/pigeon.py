import pygame
from objects.obstacles.obstacle import Obstacle
from pygame.locals import K_w, K_s, K_a, K_d
from misc.logger import log

class Pigeon(Obstacle):
    """ITS A FUCKING pigeon."""
    def __init__(self, time: float, x: int, y: int,  w: int, h: int, player):
        super().__init__(time, x, y, w, h, player)
        self.image = pygame.image.load("assets/Bottle.png").convert_alpha()
        self.texture = pygame.transform.scale(self.image, (w, h))
        self.filled = False
        self.player.add_ignore_entity_collision(self)

    def update(self, key_pressed, time):
        if super().fade_in(time):
           pygame.draw.circle(self.surf, (255, 0, 0, 50), (self.width/2, self.height/2), self._fade_in_radius)        
        elif not self.filled:
          self.surf.fill(0)
          self.surf.blit(self.texture, (0, 0))
          self.filled = True
        self.adjust_position()