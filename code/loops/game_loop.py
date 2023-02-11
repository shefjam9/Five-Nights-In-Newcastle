import pygame
import time
from misc.settings import *
from misc.colours import Colours
from text.text import HeaderText
from objects.pos import Pos
from objects.player import Player
from objects.obstacles.glass import Glass

class GameLoop:
    """Game loop class"""

    def __init__(self, screen: pygame.Surface, player: Player, bg_img: pygame.Surface) -> None:
        """Initialize the game loop"""
        self.screen = screen
        self.player = player
        self.bg_img = bg_img
        self.entities = []
        self.tile = [self.player.rect.x - (bg_img.get_width()/2), self.player.rect.y - (bg_img.get_height()/2)]
        self.header_text = HeaderText(self.screen)
        self.camera = self.screen.get_rect().copy()

        # Add entities
        self.add_entity(self.player)
        self.add_entity(Glass(time.perf_counter()*1e3, 100, 100, self.player))

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
        # Update position of bg tile
        self.player.set_bg_tile(self.tile)

        # Update pressed keys
        pressed_keys = pygame.key.get_pressed()
        
        # update entities
        player_collision = self.player.check_collision(self.player.wall)
        has_moved = self.player.update(pressed_keys)
        self.camera.center = self.player.rect.center

        for ent in self.entities:
            if ent != self.player:
                ent.update(pressed_keys, self.get_current_time())

        # Render background
        self.screen.fill(Colours.SECONDARY.value)
        tile_x = self.tile[0]
        tile_y = self.tile[1]

        if tile_x > -self.bg_img.get_width() - self.player.rel.x:
            self.screen.blit(self.bg_img, (tile_x, tile_y))

        # tile_x = self.player.rect.x
        # tile_y = self.player.rect.y
        # self.tile = [tile_x, tile_y]

        title_position = Pos(SCREEN_WIDTH / 2, round(SCREEN_HEIGHT * 0.2))
        title_position_2 = Pos(SCREEN_WIDTH / 2, round(SCREEN_HEIGHT * 0.3))
        self.header_text.render(f"Collision: {player_collision}, ({self.player.rect.left},{self.player.rect.top})", self.header_text.primary, title_position, True)
        self.header_text.render(f"Has Move: {has_moved}, ({self.player.rel.x},{self.player.rel.y})", self.header_text.primary, title_position_2, True)

        # Render entities
        for ent in self.entities:
            self.screen.blit(ent.surf, ent.rect)
        pygame.display.flip()
