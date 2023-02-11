import pygame
from misc.settings import *
from misc.game_state import GameState
from loops.game_loop import GameLoop
from loops.home_loop import HomeLoop
from objects.player import Player
from pygame.locals import K_ESCAPE, KEYDOWN, QUIT, K_p, K_o

class MainLoop:
    """Main game loop"""

    def __init__(self, screen: pygame.Surface, bg_img: pygame.Surface) -> None:
        self.current_game_state = GameState.HOME
        self.screen = screen
        self.player = Player()
        self.game_loop = GameLoop(self.screen, self.player, bg_img)
        self.home_loop = HomeLoop(self.screen)

    def start(self):
        """Start the loop"""
        running = True
        while running:
            # Event loop
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    elif event.key == K_p:
                        self.current_game_state = GameState.HOME
                    elif event.key == K_o:
                        self.current_game_state = GameState.GAME
                elif event.type == QUIT:
                    running = False

            # Check game status
            if self.current_game_state == GameState.HOME:
                self.home_loop.tick()
            elif self.current_game_state == GameState.GAME:
                self.game_loop.tick()