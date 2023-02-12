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
       self.player.add_ignore_entity_collision(self)
       self.anims = {PoliceState.MOVE_DOWN: Animation("assets/Police_Down.png", 80, 80, 2, 20),
                     PoliceState.MOVE_UP: Animation("assets/Police_Up.png", 80, 80, 2, 20),
                     PoliceState.MOVE_RIGHT: Animation("assets/Police_Right.png", 80, 80, 2, 20),
                     PoliceState.MOVE_LEFT: Animation("assets/Police_Left.png", 80, 80, 2, 20)}
       # x axis
       self.current_axis = 0
       self.view_dist = 1000
       self.speed = 1.2
    
    def run_ai(self, time):
        dist_to_player = ((self.rect.centerx - self.player.rect.centerx)**2+(self.rect.centery - self.player.rect.centery)**2)**0.5
        if dist_to_player < self.view_dist:
            if dist_to_player == 0:
                return
            
            # Vector from pigeon to player
            vec = (self.player.rect.centerx-self.rect.centerx, self.player.rect.centery-self.rect.centery)
            vec_normalized = (vec[0]/dist_to_player, vec[1]/dist_to_player)
            mov_x, mov_y = vec_normalized[0]*self.speed, vec_normalized[1]*self.speed
            self.move(mov_x, mov_y)
                
              

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

    
        
    
