import pygame
from misc.settings import *

class HomeLoop:
    """Home loop class"""

    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen

    def tick(self):
        """Tick home screen"""
        # Render background
        self.screen.fill((22, 22, 22))
        pygame.display.flip()