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
    STATE_IDLE = 4
    STATE_SLEEP_LEFT = 5
    STATE_SLEEP_RIGHT = 6

class Hobo(Obstacle):
    """ITS A FUCKING Homeless man :(!!"""
    def __init__(self, time: float, x: int, y: int,  w: int, h: int, player):
        super().__init__(time, x, y, w, h, player)
        self.filled = False
        self.player.add_ignore_entity_collision(self)
        self.damage_amount = 50
        self.anims = {HoboState.STATE_WALK_LEFT: Animation("assets/Hobo_Walking_Left.png", w, h, 7, 60, 100),
                      HoboState.STATE_WALK_RIGHT: Animation("assets/Hobo_Walking_Right.png", w, h, 7, 60, 100),
                      HoboState.STATE_IDLE: Animation("assets/Hobo_Blinking_Center.png", w, h, 3, 150),
                      HoboState.STATE_SLEEP_RIGHT : Animation("assets/Hobo_Sitting_Right.png", w, h, 5, 100),
                      HoboState.STATE_SLEEP_LEFT : Animation("assets/Hobo_Sitting_Left.png", w, h, 5, 100)
                      }
        self.tick_counter = 0
        self.speed = 0.1
        self.current_state = random.choice([HoboState.STATE_SLEEP_LEFT, HoboState.STATE_SLEEP_RIGHT])

    def run_ai(time):
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
        
        self.run_ai()
        # Move after adjusting position
        self.adjust_position()
        if self.current_state == HoboState.STATE_WALK_LEFT:
            self.move(-self.speed, 0)
        elif self.current_state == HoboState.STATE_WALK_RIGHT:
            self.move(self.speed, 0)
