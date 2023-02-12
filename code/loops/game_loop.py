import pygame
import time
import threading
from misc.settings import *
from misc.colours import Colours
from text.text import ButtonText
from objects.pos import Pos
from objects.player import Player
from host import Server

class GameLoop:
    """Game loop class"""

    def __init__(self, screen: pygame.Surface, player: Player, bg_img: pygame.Surface) -> None:
        """Initialize the game loop"""
        self.screen = screen
        self.player = player
        self.bg_img = bg_img
        self.entities = []
        self.tile = [self.player.rect.x - (bg_img.get_width()/2), self.player.rect.y - (bg_img.get_height()/2)]
        self.background_image = pygame.image.load("assets/Background.png").convert()
        self.health_text = ButtonText(self.screen)
        self.camera = self.screen.get_rect().copy()

        # Add entities
        self.add_entity(self.player)

        # Server
        self.server = Server('127.0.0.1', 6969, self.player)
        self.server_thread = threading.Thread(target=self.server.run)
        self.server_thread.setDaemon(True)
        self.server_thread.start()

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
        
        # update player
        player_collision = self.player.check_collision(self.player.wall)
        has_moved = self.player.update(pressed_keys, self.get_current_time())
        self.camera.center = self.player.rect.center

        # update other entities
        for ent in self.entities:
            if ent != self.player:
                ent.update(pressed_keys, self.get_current_time())

        # Render background
        self.screen.fill(Colours.SECONDARY.value)
        tile_x = self.tile[0]
        tile_y = self.tile[1]

        if tile_x > -self.bg_img.get_width() - self.player.rel.x:
            self.screen.blit(self.bg_img, (tile_x, tile_y))
            self.screen.blit(self.background_image, (tile_x, tile_y))

        # Update health text
        self.display_health()

        # Render entities
        for ent in self.entities:
            if ent != self.player:
                self.screen.blit(ent.surf, ent.rect)
        self.screen.blit(self.player.surf, self.player.rect)
        # draw sprint meter
        pygame.draw.rect(self.screen, (10, 10, 10), (self.screen.get_width()/6, 
                                                     self.screen.get_height()-25,
                                                     4*self.screen.get_width()/6,
                                                     20))
        sprint_length = (self.player.sprint_left / 100) * (4 * self.screen.get_width()/6 - 10)
        pygame.draw.rect(self.screen, (240, 240, 240), (self.screen.get_width()/6 + 5,
                                                        self.screen.get_height()-20,
                                                        sprint_length,
                                                        10))
        self.player.set_entities(self.entities)
        if self.player.hurt_this_tick:
            print("Hurt overlay blit")
            self.screen.fill((255, 0, 0, 128))
        pygame.display.flip()

        # Send player data to server
        self.server.send_position()

    def display_health(self):
        """Display the health in the top right of the screen"""
        title_position = Pos(140, 40)
        self.health_text.render(f"Health: {self.player.health}%", self.health_text.primary, title_position, True)
