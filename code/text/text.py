import pygame
from objects.pos import Pos
from misc.logger import log

class Text:
    """Custom text font"""
    white = (255, 255, 255)
    red = (255, 0, 0)

    def __init__(self, screen: pygame.Surface) -> None:
        self.font = pygame.font.Font("assets/fonts/JetBrainsMono.ttf", 10)
        self.screen = screen

    def render(self, text: str, color, pos: Pos) -> pygame.Surface:
        """Render text"""
        try:
            text_img = self.font.render(text, True, color)
            text_rect = text_img.get_rect(center=pos.to_tuple())
            self.screen.blit(text_img, text_rect)
        except Exception as e:
            log("Error rendering text: " + str(e), "error")

class HeaderText(Text):
    """Custom header text"""
    def __init__(self, screen: pygame.Surface) -> None:
        super().__init__(screen)
        self.font = pygame.font.Font("assets/fonts/JetBrainsMono.ttf", 50)

class ButtonText(Text):
    """Custom button text"""
    def __init__(self, screen: pygame.Surface) -> None:
        super().__init__(screen)
        self.font = pygame.font.Font("assets/fonts/JetBrainsMono.ttf", 25)