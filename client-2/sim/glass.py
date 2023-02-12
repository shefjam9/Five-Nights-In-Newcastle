import pygame.gfxdraw as gx


class Glass:
    
    def __init__(self, x, y, client):
        self.pos = (x, y)
        self.name = "glass"
    
    def update(self):
        pass
    
    def render(self, surface):
        gx.filled_circle(surface, int(self.pos[0]), int(self.pos[1]), 10, (0, 255, 255))
        gx.aacircle(surface, int(self.pos[0]), int(self.pos[1]), 10, (0, 255, 255))