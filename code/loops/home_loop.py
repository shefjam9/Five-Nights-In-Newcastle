import pygame
from misc.settings import *
from objects.pos import Pos
from text.text import HeaderText, ButtonText
from misc.colours import Colours

class HomeLoop:
    """Home loop class"""

    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.header_text = HeaderText(self.screen)
        self.button_text = ButtonText(self.screen)

    def tick(self):
        """Tick home screen"""
        # Render background
        self.screen.fill(self.header_text.dark_background)
        
        # Render title
        title_position = Pos(SCREEN_WIDTH / 2, round(SCREEN_HEIGHT * 0.2))
        self.header_text.render("Five Nights at Newcastle", self.header_text.primary, title_position, True)
        
        # Render buttons
        button_position = Pos(SCREEN_WIDTH / 2, round(SCREEN_HEIGHT * 0.4))
        self.button_text.render("Play", self.header_text.primary , button_position)

        # Reload screen
        pygame.display.flip()