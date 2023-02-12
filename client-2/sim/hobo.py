import random
import math
from pygame import gfxdraw as gx



class Hobo:
    
    def __init__(self, x, y, client):
        
        self.pos = [x, y]
        self._client = client
        self.speed = 0.45
        self.name = "hobo"
    
    def update(self):
        
        dist_to_player = ((self.pos[0] - self._client.pos.x)**2+(self.pos[1] - self._client.pos.y)**2)**0.5
        if dist_to_player < 281:
            if dist_to_player == 0:
                return
            
            # Vector from pigeon to player
            vec = (self._client.pos.x-self.pos[0], self._client.pos.y-self.pos[1])
            vec_normalized = (vec[0]/dist_to_player, vec[1]/dist_to_player)
            mov_x, mov_y = vec_normalized[0]*self.speed, vec_normalized[1]*self.speed
            self.pos[0] += mov_x
            self.pos[1] += mov_y
    
    def render(self, surface):
        gx.filled_circle(surface, int(self.pos[0]), int(self.pos[1]), 10, (255, 255, 0))
        gx.aacircle(surface, int(self.pos[0]), int(self.pos[1]), 10, (255, 255, 0))