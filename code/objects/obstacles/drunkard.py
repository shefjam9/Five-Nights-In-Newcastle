import pygame
from objects.obstacles.obstacle import Obstacle
from pygame.locals import K_w, K_s, K_a, K_d
from objects.animation import Animation
from enum import IntFlag
import random
import math

class HoboState(IntFlag):
    STATE_NONE = 1,
    STATE_WALK_LEFT = 2,
    STATE_WALK_RIGHT = 3,
    STATE_IDLE = 4
    STATE_SLEEP_LEFT = 5
    STATE_SLEEP_RIGHT = 6

_HOBO_WIDTH = 128
_HOBO_HEIGHT = 128

class Hobo(Obstacle):
    """ITS A FUCKING Homeless man :(!!"""
    def __init__(self, time: float, x: int, y: int,  player):
        w, h = _HOBO_WIDTH, _HOBO_HEIGHT
        super().__init__(time, x, y, w, h, player)
        self.filled = False
        self.player.add_ignore_entity_collision(self)
        self.damage_amount = 5
        self.anims = {HoboState.STATE_WALK_LEFT: Animation("assets/Hobo_Walking_Left.png", w, h, 7, 20, 30),
                      HoboState.STATE_WALK_RIGHT: Animation("assets/Hobo_Walking_Right.png", w, h, 7, 20, 30),
                      HoboState.STATE_IDLE: Animation("assets/Hobo_Blinking_Center.png", w, h, 3, 150),
                      HoboState.STATE_SLEEP_RIGHT : Animation("assets/Hobo_Sitting_Right.png", w, h, 5, 20),
                      HoboState.STATE_SLEEP_LEFT : Animation("assets/Hobo_Sitting_Left.png", w, h, 5, 20)
                      }
        self.tick_counter = 0
        self.speed = 0.1
        self.current_state = random.choice([HoboState.STATE_SLEEP_LEFT, HoboState.STATE_SLEEP_RIGHT])
        self.view_dist = 750
        self.current_arc = 1
        self.speed = 1.2

    def run_ai(self, time):
        dist_to_player = ((self.rect.centerx - self.player.rect.centerx)**2+(self.rect.centery - self.player.rect.centery)**2)**0.5
        if self.current_state == HoboState.STATE_SLEEP_RIGHT or self.current_state == HoboState.STATE_SLEEP_LEFT:
            awake_chance = 0.001
            mult = (self.view_dist-dist_to_player) / self.view_dist
            if random.random() < mult/1000+awake_chance:
                self.current_state = HoboState.STATE_IDLE
        elif dist_to_player < self.view_dist:
            if dist_to_player == 0:
                return
            
            # Vector from pigeon to player
            vec = (self.player.rect.centerx-self.rect.centerx, self.player.rect.centery-self.rect.centery)
            vec_normalized = (vec[0]/dist_to_player, vec[1]/dist_to_player)
            mov_x, mov_y = vec_normalized[0]*self.speed, vec_normalized[1]*self.speed
            if mov_x > 0:
                self.current_state = HoboState.STATE_WALK_RIGHT
            elif mov_x <= 0:
                self.current_state = HoboState.STATE_WALK_LEFT
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
        self.tick_counter += 1
        
        self.run_ai(time)
        # Move after adjusting position
        self.adjust_position()
