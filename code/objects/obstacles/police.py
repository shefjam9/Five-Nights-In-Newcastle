from obstacle import Obstacle
import pygame

class Police(Obstacle):
    
    def __init__(self, time, x, y):
       super().__init__(time, x, y)
       self.fade_in_radius = 32
       self.rect = (x, y, 64, 64)
       self.surf = pygame.Surface((64, 64))
    
    def update(self, keys, time):
        if self.fade_in(time):
            return
    
        
    
