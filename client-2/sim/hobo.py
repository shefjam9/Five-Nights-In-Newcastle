import random
import math
from pygame import gfxdraw as gx



class Hobo:
    
    def __init__(self, x, y, client):
        
        self.pos = [x, y]
        self._client = client
    
    def update(self):
        
        pass
    
    def render(self, surface):
        gx.filled_circle(surface, self.pos[0], self.pos[1], 10, (255, 255, 0))
        gx.aacircle(surface, self.pos[0], self.pos[1], 10, (255, 255, 0))