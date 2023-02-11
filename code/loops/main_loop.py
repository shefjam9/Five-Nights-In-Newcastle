import pygame
from misc.settings import *
from misc.logger import log
from misc.game_state import GameState
from loops.game_loop import GameLoop
from loops.home_loop import HomeLoop
from objects.player import Player
from pygame.locals import K_ESCAPE, KEYDOWN, QUIT, K_LSHIFT, MOUSEBUTTONDOWN, KEYUP

class MainLoop:
    """Main game loop"""

    def __init__(self, screen: pygame.Surface, bg_img: pygame.Surface) -> None:
        self.current_game_state = GameState.HOME
        self.screen = screen
        self.player = Player(bg_img)
        self.bg_img = bg_img
        self.game_loop = GameLoop(self.screen, self.player, bg_img)
        self.home_loop = HomeLoop(self.screen, self)
        self.clock = pygame.time.Clock()

    def start(self):
        """Start the loop"""
        running = True
        while running:
            # Event loop
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        if self.current_game_state == GameState.GAME:
                            self.current_game_state = GameState.HOME
                        elif self.current_game_state == GameState.HOME:
                            running = False
                    if event.key == K_LSHIFT:
                        self.player.set_sprint(True)
                elif event.type == KEYUP:
                    if event.key == K_LSHIFT:
                        self.player.set_sprint(False)
                elif event.type == QUIT:
                    running = False
                elif event.type == MOUSEBUTTONDOWN:
                    if self.current_game_state == GameState.HOME:
                        self.home_loop.check_pressed(event)

            # Check game status
            if self.current_game_state == GameState.HOME:
                self.home_loop.tick()
                self.home_loop.check_hover()
            elif self.current_game_state == GameState.GAME:
                self.game_loop.tick()
            elif self.current_game_state == GameState.QUIT:
                running = False

            # Tick clock
            self.clock.tick()
            # log(self.clock.get_fps(), "info")