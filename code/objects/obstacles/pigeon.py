import pygame
from objects.obstacles.obstacle import Obstacle
from pygame.locals import K_w, K_s, K_a, K_d
from misc.logger import log
from objects.animation import Animation

class Pigeon(Obstacle):
    """ITS A FUCKING pigeon."""
    def __init__(self, time: float, x: int, y: int,  w: int, h: int, player):
        super().__init__(time, x, y, w, h, player)
        self.filled = False
        self.player.add_ignore_entity_collision(self)

        self.walk_animation = Animation("assets/pigeon_walking.png", 64, 64, 24, 20)
        self.peck_animation = Animation("assets/pigeon_pecking.png", 96, 64, 4, 40)

        self.current_animation = self.peck_animation

    def update(self, key_pressed, time):
        if super().fade_in(time):
           pygame.draw.circle(self.surf, (255, 0, 0, 50), (self.width/2, self.height/2), self._fade_in_radius)        
        else:
            self.surf.fill(0)
            self.current_animation.update(time)
            self.current_animation.render_frame(self.surf, 0, 0)
        self.adjust_position()