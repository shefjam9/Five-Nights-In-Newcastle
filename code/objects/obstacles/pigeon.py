import pygame
from objects.obstacles.obstacle import Obstacle
from pygame.locals import K_w, K_s, K_a, K_d
from misc.logger import log
from objects.animation import Animation
from enum import IntFlag

class PigeonState(IntFlag):
    STATE_PECKING = 1
    STATE_WALKING_LEFT = 2
    STATE_WALKING_RIGHT = 3

class Pigeon(Obstacle):
    """ITS A FUCKING pigeon."""
    def __init__(self, time: float, x: int, y: int,  w: int, h: int, player):
        super().__init__(time, x, y, w, h, player)
        self.filled = False
        self.player.add_ignore_entity_collision(self)

        self.anims = {PigeonState.STATE_WALKING_RIGHT: Animation("assets/pigeon_walking.png", 64, 64, 24, 5),
                      PigeonState.STATE_WALKING_LEFT: Animation("assets/pigeon_walking_left.png", 64, 64, 24, 5),
                      PigeonState.STATE_PECKING: Animation("assets/pigeon_pecking.png", 96, 64, 4, 40)}
        self.see_player_range = 400
        self.current_state = PigeonState.STATE_PECKING
        self.collision_direction = PigeonState.STATE_PECKING
        self.collided = False
        self.speed = 1

    def run_ai(self, time):
        dist_to_player = ((self.rect.centerx - self.player.rect.centerx)**2+(self.rect.centery - self.player.rect.centery)**2)**0.5
        if dist_to_player < self.see_player_range:
            # Avoid 0 division error
            self.current_state = PigeonState.STATE_WALKING_LEFT if self.player.rect.centerx < self.rect.centerx else PigeonState.STATE_WALKING_RIGHT
            if dist_to_player == 0:
                return
            
            # Vector from pigeon to player
            vec = (self.player.rect.centerx-self.rect.centerx, self.player.rect.centery-self.rect.centery)
            vec_normalized = (vec[0]/dist_to_player, vec[1]/dist_to_player)
            mov_x, mov_y = vec_normalized[0]*self.speed, vec_normalized[1]*self.speed

            # Move and check for collision
            print(self.collision_direction != self.current_state, self.collided)
            if self.collision_direction != self.current_state and self.collided:
                if self.collision_direction == PigeonState.STATE_WALKING_LEFT:
                    self.move(mov_x+5, mov_y+5)
                elif self.collision_direction == PigeonState.STATE_WALKING_RIGHT:
                    self.move(mov_x-5, mov_y-5)
                self.collided = False
            elif not self.collided:
                self.move(mov_x, mov_y)
                if self.check_collision(self.player.wall):
                    self.move(-(mov_x), -(mov_y))
                    self.collision_direction = self.current_state
                    self.collided = True
        else:
            self.current_state = PigeonState.STATE_PECKING

    def update(self, key_pressed, time):
        if super().fade_in(time):
           pygame.draw.circle(self.surf, (255, 0, 0, 50), (self.width/2, self.height/2), self._fade_in_radius)        
        else:
            self.surf.fill(0)
            self.anims[self.current_state].update(time)
            self.anims[self.current_state].render_frame(self.surf, 0, 0)
            self.run_ai(time)
        self.adjust_position()