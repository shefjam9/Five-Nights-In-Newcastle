import pygame
from objects.pos import Pos
from misc.colours import Colours
from misc.logger import log

class Text:
    """Custom text font"""
    def __init__(self, screen: pygame.Surface) -> None:
        self.font = pygame.font.Font("assets/fonts/RobotoCondensed-Regular.ttf", 10)
        self.screen = screen

        self.primary = Colours.PRIMARY.value
        self.secondary = Colours.SECONDARY.value
        self.dark_background = Colours.DARK_BACKGROUND.value
        self.light_background = Colours.LIGHT_BACKGROUND.value

    def render(self, text: str, color, pos: Pos, shadow: bool = False) -> pygame.Surface:
        """Render text"""
        try:
            if shadow:
                shadow_img = self.font.render(text, False, self.light_background)
                shadow_pos = Pos(pos.x + 10, pos.y + 10)
                shadow_rect = shadow_img.get_rect(center=shadow_pos.to_tuple())
                self.screen.blit(shadow_img, shadow_rect
                                 )
            text_img = self.font.render(text, False, color)
            text_rect = text_img.get_rect(center=pos.to_tuple())
            self.screen.blit(text_img, text_rect)
        except Exception as e:
            log("Error rendering text: " + str(e), "error")

class HeaderText(Text):
    """Custom header text"""
    def __init__(self, screen: pygame.Surface) -> None:
        super().__init__(screen)
        self.font = pygame.font.Font("assets/fonts/RobotoCondensed-Bold.ttf", 80)

class ButtonText(Text):
    """Custom button text"""
    def __init__(self, screen: pygame.Surface) -> None:
        super().__init__(screen)
        self.font = pygame.font.Font("assets/fonts/RobotoCondensed-Regular.ttf", 40)