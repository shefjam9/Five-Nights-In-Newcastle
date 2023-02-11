import pygame
from objects.obstacles.obstacle import Obstacle
from pygame.locals import K_w, K_s, K_a, K_d
from objects.animation import Animation

class Hobo(Obstacle):
    """ITS A FUCKING Homeless man :(!!"""
    def __init__(self, time: float, x: int, y: int,  w: int, h: int, player):
        super().__init__(time, x, y, w, h, player)
        self.filled = False
        self.player.add_ignore_entity_collision(self)
        self.damage_amount = 50
        self.walking_animation = {"R": Animation("assets/Hobo_Walking_Right.png", 64, 64, 7, 60, 100),
                                  "L": Animation("assets/Hobo_Walking_Left.png", 64, 64, 7, 60, 100)}
        self.current_animation = self.walking_animation["L"]

    def update(self, key_pressed, time):
        if super().fade_in(time):
           pygame.draw.circle(self.surf, (255, 0, 0, 50), (self.width/2, self.height/2), self._fade_in_radius)        
        else:
            self.surf.fill(0)
            self.current_animation.update(time)
            self.current_animation.render_frame(self.surf, 0, 0)
        self.adjust_position()