from obstacle import Obstacle
from enum import IntFlag
import pygame


class PoliceState(IntFlag):
    STATE_PATROL = 1,
    STATE_CHASE = 2


class Police(Obstacle):
    
    def __init__(self, time, x, y, player):
       super().__init__(time, x, y, player)
       self.fade_in_radius = 32
       self.rect = (x, y, 64, 64)
       self.surf = pygame.Surface((64, 64))
       self.current_state = PoliceState.STATE_PATROL
       # x axis
       self.current_axis = 0
    
    def run_ai(self, time):
        dist_to_player = ((self.rect.centerx - self.player.rect.centerx)**2+(self.rect.centery - self.player.rect.centery)**2)**0.5
        if self.current_state == PoliceState.STATE_PATROL:
            if dist_to_player < 200:
                self.current_state == PoliceState.STATE_CHASE
        elif self.current_state == PoliceState.STATE_CHASE:
            #TODO move up and accross - AI can only move in horizontals
            pass
                
              

    def update(self, key_pressed, time):
        if super().fade_in(time):
           pygame.draw.circle(self.surf, (255, 0, 0, 50), (self.width/2, self.height/2), self._fade_in_radius)  
           self.adjust_position()
           return   
        
        # Draw frame
        self.surf.fill(0)
        self.anims[self.current_state].update(time)
        self.anims[self.current_state].render_frame(self.surf, 0, 0)
        self.tick_counter += 1
        
        self.run_ai(time)
        # Move after adjusting position
        self.adjust_position()

    
        
    
