import pygame
from objects.obstacles.obstacle import Obstacle
from pygame.locals import K_w, K_s, K_a, K_d
from misc.logger import log

class Glass(Obstacle):

    def __init__(self, time: float, x: int, y: int, player):
        super().__init__(time, x, y, player)
        self.image = pygame.image.load("assets/Bottle.png").convert_alpha()
        self.texture = pygame.transform.scale(self.image, (64, 64))
        self.filled = False

    def update(self, key_pressed, time):
        if super().fade_in(time):
           self.surf.fill(0)
           pygame.draw.circle(self.surf, (255, 0, 0, 50), (32, 32), self._fade_in_radius)
           return
        
        if not self.filled:
          self.surf.blit(self.texture, (0, 0))
          self.filled = True
        else:
            self.rect.x = self.player.obj_offset.x + self.start_x
            self.rect.y = self.player.obj_offset.y + self.start_y