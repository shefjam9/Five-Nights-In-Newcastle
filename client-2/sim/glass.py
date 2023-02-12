import pygame.gfxdraw as gx
import pygame

_NUM_GLASS = 0

class Glass:
    
    def __init__(self, x, y, client):
        self.pos = (x, y)
        global _NUM_GLASS
        _NUM_GLASS += 1
        self.name = f"glass{_NUM_GLASS}"
        self.font = pygame.font.SysFont("serif", 16)
        self.text = self.font.render(self.name, True, (0, 255, 255))
    
    def update(self):
        pass
    
    def render(self, surface):
        gx.filled_circle(surface, int(self.pos[0]), int(self.pos[1]), 10, (0, 255, 255))
        gx.aacircle(surface, int(self.pos[0]), int(self.pos[1]), 10, (0, 255, 255))
        text_x = self.pos[0] - self.text.get_width()/2
        text_y = self.pos[1] + 15
        surface.blit(self.text, (text_x, text_y))