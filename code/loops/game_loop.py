import pygame
import time
import threading
from misc.settings import *
from misc.colours import Colours
from text.text import ButtonText
from objects.pos import Pos
from objects.player import Player
from host import Server
from pygame import gfxdraw as gx
from text.text import HeadingText
import math
from enum import IntFlag
from pygame import mixer

_SERVER_ADDR = '192.168.239.174'
_SERVER_PORT = 8888


class EndReason():
    END_NONE = 1,
    END_PLAYER_SURVIVE = 2,
    END_PLAYER_DEATH = 3

class GameLoop:
    """Game loop class"""

    def __init__(self, screen: pygame.Surface, player: Player, bg_img: pygame.Surface) -> None:
        """Initialize the game loop"""
        self.screen = screen
        self.player = player
        self.bg_img = bg_img
        self.entities = []
        # self.tile = [self.player.rect.x - (bg_img.get_width()/2), self.player.rect.y - (bg_img.get_height()/2)]
        self.tile = [0, 0]
        self.background_image = pygame.image.load("assets/Background.png").convert()
        self.health_text = ButtonText(self.screen)
        self.camera = self.screen.get_rect().copy()
        self.game_ended = EndReason.END_NONE

        # Add entities
        self.add_entity(self.player)

        # Server
        self.server = Server(_SERVER_ADDR, _SERVER_PORT, self.player, self)
        self.server_thread = threading.Thread(target=self.server.run)
        self.server_thread.setDaemon(True)
        self.server_thread.start()

        # Countdown timer
        self.start_time = GameLoop.get_current_time()
        self.run_time = 120e3
        self.time_header = HeadingText(self.screen)

        pygame.mixer.music.load("assets/music.wav")
        pygame.mixer.music.play(-1)
        self.is_game_running = True

    def end_game(self):
        self.is_game_running = False
        pygame.mixer.music.stop()

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
        _ = self.player.check_collision(self.player.wall)
        _ = self.player.update(pressed_keys, self.get_current_time())
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
        
        self.time_diff = GameLoop.get_current_time() - self.start_time
        mins = int(((self.run_time - self.time_diff)//60e3))
        secs = int(((self.run_time - self.time_diff)%60e3)/1000)
        text = f"0{mins}:{secs}" if secs > 10 else f"0{mins}:0{secs}"
        self.time_header.render(text, (255, 255, 255), Pos(self.screen.get_width()/2, 100), True)


        pygame.display.flip()

        # Send player data to server
        self.server.send_position()
        # check the timer
        
        self.check_death()
        if self.time_diff >= self.run_time:
            self.game_ended = EndReason.END_PLAYER_SURVIVE

    def check_death(self):
        """Check the death of the player"""
        if self.player.health <= 0:
            self.game_ended = EndReason.END_PLAYER_DEATH
            
            
            