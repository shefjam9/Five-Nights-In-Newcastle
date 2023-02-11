import pygame
from objects.obstacles.obstacle import Obstacle
from pygame.locals import K_w, K_s, K_a, K_d
from objects.animation import Animation
from enum import IntFlag
import random

class HoboState(IntFlag):
    STATE_NONE = 1,
    STATE_WALK_LEFT = 2,
    STATE_WALK_RIGHT = 3,
    STATE_WALK_CENTER = 4
    STATE_IDLE_LEFT = 5
    STATE_IDLE_RIGHT = 6

class Hobo(Obstacle):
    """ITS A FUCKING Homeless man :(!!"""
    def __init__(self, time: float, x: int, y: int,  w: int, h: int, player):
        super().__init__(time, x, y, w, h, player)
        self.filled = False
        self.player.add_ignore_entity_collision(self)
        self.damage_amount = 50
        self.anims = {HoboState.STATE_WALK_LEFT: Animation("assets/Hobo_Walking_Left.png", 64, 64, 7, 60, 100),
                      HoboState.STATE_WALK_RIGHT: Animation("assets/Hobo_Walking_Right.png", 64, 64, 7, 60, 100),
                      HoboState.STATE_WALK_CENTER: Animation("assets/Hobo_Blinking_Center.png", 64, 64, 3, 50),
                      HoboState.STATE_IDLE_RIGHT : Animation("assets/Hobo_Sitting_Right.png", 64, 64, 3, 100),
                      HoboState.STATE_IDLE_LEFT : Animation("assets/Hobo_Sitting_Left.png", 64, 64, 3, 100)
                      }
        self.tick_counter = 0
        # self.current_state = random.choice([HoboState.STATE_IDLE_LEFT, HoboState.STATE_IDLE_RIGHT])
        self.current_state = HoboState.STATE_WALK_LEFT

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
        
        # if self.tick_counter >= random.randint(5000, 15000):
        #     self.tick_counter = 0
        #     self.current_state = random.choice([HoboState.STATE_WALK_CENTER, HoboState.STATE_WALK_LEFT, HoboState.STATE_WALK_RIGHT])

        # Move after adjusting position
        self.adjust_position()
        self.move(1, 0)