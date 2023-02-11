import pygame
from misc.settings import *
from misc.logger import log
from objects.pos import Pos
from text.text import ButtonText

class Button(ButtonText):
    """Button class"""
    def __init__(self, screen: pygame.Surface) -> None:
        super().__init__(screen)
        self.button: pygame.Surface

    def render(self, text: str, color, pos: Pos) -> pygame.Surface:
        """Render text"""
        try:
            text_img = self.font.render(text, False, color)
            text_rect = text_img.get_rect()
            background_img = pygame.draw.rect(self.screen, self.primary, (text_rect.left, text_rect.top, text_rect.width, text_rect.height))

            text_rect = text_img.get_rect(center=pos.to_tuple())
        except Exception as e:
            log("Error rendering text: " + str(e), "error")