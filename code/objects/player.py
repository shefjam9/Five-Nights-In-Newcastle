import pygame
from settings import *
from pygame.locals import K_w, K_s, K_a, K_d

class Player(pygame.sprite.Sprite):
    def __init__(self):
        """Initialize the player"""
        super(Player, self).__init__()

        # Initialize the player surface
        self.surf = pygame.Surface((75, 25))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()
        self.speed = 1

        # Move the player
        self.rect.x = 100
        self.rect.y = 100

    def boundary_check(self):
        """Check if player is within screen bounds"""
        return (self.rect.left > 0 and self.rect.right < SCREEN_WIDTH 
                and self.rect.top > 0 and self.rect.bottom < SCREEN_HEIGHT)

    def update(self, key_pressed):
        """Update the player position based on key presses"""
        key_results = {K_w: (0, -self.speed), K_s: (0, self.speed), 
                       K_a: (-self.speed, 0), K_d: (self.speed, 0)}
        for key in key_results:
            if key_pressed[key] and self.boundary_check():
                self.rect.move_ip(key_results[key])

                # Make sure the player doesn't get stuck in the wall by moving
                # them back if they are
                if not self.boundary_check():
                    self.rect.move_ip(-key_results[key][0], -key_results[key][1])
