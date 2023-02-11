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
        
        key_results = {K_w: (0, -self.player.speed), K_s: (0, self.player.speed), 
                        K_a: (-self.player.speed, 0), K_d: (self.player.speed, 0)}
        for key in key_results:
            if key_pressed[key] and self.player.collision:
                self.rect.x -= key_results[key][0]
                self.rect.y -= key_results[key][1]       