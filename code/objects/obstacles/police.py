from objects.obstacles.obstacle import Obstacle
from enum import IntFlag
import pygame
from objects.animation import Animation

class PoliceState(IntFlag):
    MOVE_UP = 1,
    MOVE_LEFT = 2,
    MOVE_RIGHT = 3,
    MOVE_DOWN = 4


class Police(Obstacle):
    
    def __init__(self, time, x, y, player):
       """ Crikey it's the rozzers """
       super().__init__(time, x, y, 80, 80, player)
       self.patrolling = True
       self.current_state = PoliceState.MOVE_LEFT
       self.anims = {PoliceState.MOVE_DOWN: Animation("assets/Police_Down.png", 80, 80, 2, 20),
                     PoliceState.MOVE_UP: Animation("assets/Police_Up.png", 80, 80, 2, 20),
                     PoliceState.MOVE_RIGHT: Animation("assets/Police_Right.png", 80, 80, 2, 20),
                     PoliceState.MOVE_LEFT: Animation("assets/Police_Left.png", 80, 80, 2, 20)}
       # x axis
       self.current_axis = 0
    
    def run_ai(self, time):
        dist_to_player = ((self.rect.centerx - self.player.rect.centerx)**2+(self.rect.centery - self.player.rect.centery)**2)**0.5
        if dist_to_player < 200:
            self.patrolling = False
        else:
            self.patrolling = True
        if self.patrolling:
            pass
        else:
            #TODO move up and accross - AI can only move in horizontals
            dist_vert = self.player.rect.centery - self.rect.centery
            dist_hor = self.player.rect.centerx - self.rect.centerx
            move_vector = None
            if dist_vert == 0:
                move_vector = (dist_hor/abs(dist_hor), 0)
            elif dist_hor == 0:
                move_vector = (0, dist_vert/abs(dist_vert))
            else:
                move_vector = (dist_hor/abs(dist_hor), 0) if abs(dist_hor)<abs(dist_vert) else (0, dist_vert/abs(dist_vert))
            self.move(move_vector[0]*10, move_vector[1]*10)
                
              

    def update(self, key_pressed, time):
        if super().fade_in(time):
           pygame.draw.circle(self.surf, (255, 0, 0, 50), (self.width/2, self.height/2), self._fade_in_radius)  
           self.adjust_position()
           return   
        
        # Draw frame
        self.surf.fill(0)
        self.anims[self.current_state].update(time)
        self.anims[self.current_state].render_frame(self.surf, 0, 0)
        
        self.run_ai(time)
        # Move after adjusting position
        self.adjust_position()

    
        
    
