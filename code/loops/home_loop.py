import pygame
from misc.settings import *
from objects.pos import Pos
from text.text import HeaderText, ButtonText

class HomeLoop:
    """Home loop class"""

    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.header_text = HeaderText(self.screen)
        self.button_text = ButtonText(self.screen)

    def tick(self):
        """Tick home screen"""
        # Render background
        self.screen.fill((22, 22, 22))
        
        # Render title
        title_position = Pos(SCREEN_WIDTH / 2, round(SCREEN_HEIGHT * 0.15))
        self.header_text.render("Five Nights at Newcastle", HeaderText.white, title_position)
        
        # Render buttons
        button_position = Pos(SCREEN_WIDTH / 2, round(SCREEN_HEIGHT * 0.5))
        self.button_text.render("Play", ButtonText.white, button_position)

        # Reload screen
        pygame.display.flip()