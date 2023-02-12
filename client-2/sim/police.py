from pygame import gfxdraw as gx
import pygame

_NUM_POLICE = 0


class Police:
    
    

    def __init__(self, x, y, client) -> None:
        self.pos = [x, y]
        self._client = client
        global _NUM_POLICE
        _NUM_POLICE +=1
        self.speed = 0.45
        self.name = f"copper{_NUM_POLICE}"
        self.font = pygame.font.SysFont("serif", 16)
        self.text = self.font.render(self.name, True, (100, 255, 100))

    def update(self):
        dist_to_player = ((self.pos[0] - self._client.pos.x)**2+(self.pos[1] - self._client.pos.y)**2)**0.5
        if dist_to_player < 375:
            if dist_to_player == 0:
                return
            
            # Vector from pigeon to player
            vec = (self._client.pos.x-self.pos[0], self._client.pos.y-self.pos[1])
            vec_normalized = (vec[0]/dist_to_player, vec[1]/dist_to_player)
            mov_x, mov_y = vec_normalized[0]*self.speed, vec_normalized[1]*self.speed
            self.pos[0] += mov_x
            self.pos[1] += mov_y
    
    def render(self, surface):
        gx.filled_circle(surface, int(self.pos[0]), int(self.pos[1]), 10, (100, 255, 100))
        gx.aacircle(surface, int(self.pos[0]), int(self.pos[1]), 10, (100, 255, 100))
        text_x = self.pos[0] - self.text.get_width()/2
        text_y = self.pos[1] + 15
        surface.blit(self.text, (text_x, text_y))