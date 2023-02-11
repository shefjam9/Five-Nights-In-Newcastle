import pygame
import time
from misc.settings import *
from objects.player import Player

class GameLoop:
    """Game loop class"""

    def __init__(self, screen: pygame.Surface, player: Player, bg_img: pygame.Surface) -> None:
        """Initialize the game loop"""
        self.screen = screen
        self.player = player
        self.bg_img = bg_img
        self.entities = []
        self.tile = [0, 0]

        # Add entities
        self.add_entity(self.player)

    def add_entity(self, entity: pygame.sprite.Sprite):
        """Add an entity to the game (needs update method)"""
        self.entities.append(entity)

    def remove_entity(self,entity: pygame.sprite.Sprite):
        """Removes entity"""
        self.entities.remove(entity)
    
    @staticmethod
    def get_current_time() -> float:
        """Return current time in ms"""
        return time.perf_counter() * 1e3

    def tick(self):
        """Main game loop tick"""
        # Update pressed keys
        pressed_keys = pygame.key.get_pressed()
        
        # update entities
        for ent in self.entities:
            ent.update(pressed_keys, self.get_current_time())

        # Render background
        self.screen.fill((255, 0, 0))
        tile_x = self.tile[0]
        tile_y = self.tile[1]

        if tile_x > -self.bg_img.get_width() - self.player.rel.x:
            self.screen.blit(self.bg_img, (tile_x, tile_y))

        tile_x = -self.player.rel.x
        tile_y = -self.player.rel.y
        self.tile = [tile_x, tile_y]

        # Render entities
        for ent in self.entities:
            self.screen.blit(ent.surf, ent.rect)
        pygame.display.flip()