import pygame
from misc.settings import *
from misc.logger import log
from objects.pos import Pos
from text.text import ButtonText

class Button(ButtonText):
    """Button class"""
    def __init__(self, screen: pygame.Surface, callback, callback_args=None) -> None:
        super().__init__(screen)
        self.button: pygame.Surface
        self.padding_x = 40
        self.padding_y = 5
        self.highlighted = False
        self.callback = callback
        self.callback_args = callback_args

    def render(self, text: str, color, pos: Pos) -> pygame.Surface:
        """Render text"""
        try:
            text_img = self.font.render(text, False, color)
            text_rect = text_img.get_rect()
            background_rect = pygame.Rect((pos.x - round(text_rect.width/2) - self.padding_x, 
                                           pos.y - round(text_rect.height/2) - (self.padding_y * 2), 
                                           text_rect.width + self.padding_x * 2, 
                                           text_rect.height + self.padding_y * 2))
            text_rect = text_img.get_rect(center=pos.to_tuple())
            pygame.draw.rect(self.screen, self.light_background, background_rect, 0, 10)
            pygame.draw.rect(self.screen, self.secondary if self.highlighted else self.primary, background_rect, 4, 10)
            self.screen.blit(text_img, text_rect)
            self.button = background_rect

            return self
        except Exception as e:
            log("Error rendering text: " + str(e), "error")

    def check_pressed(self, event):
        """Check if button is pressed"""
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.button.collidepoint(x, y):
                if self.callback_args is not None:
                    self.callback(self.callback_args)
                else:
                    self.callback()
    
    def check_hover(self) -> bool:
        """Check if button is hovered"""
        x, y = pygame.mouse.get_pos()
        if self.button.collidepoint(x, y):
            return True
        return False

