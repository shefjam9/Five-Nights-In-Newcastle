import pygame
from objects.pos import Pos
from misc.colours import Colours
from misc.logger import log

class Text:
    """Custom text font"""
    def __init__(self, screen: pygame.Surface) -> None:
        self.font = pygame.font.Font("assets/fonts/Minecraft.ttf", 10)
        self.screen = screen

        self.primary = Colours.PRIMARY.value
        self.secondary = Colours.SECONDARY.value
        self.shadow = Colours.SHADOW.value
        self.dark_background = Colours.DARK_BACKGROUND.value
        self.light_background = Colours.LIGHT_BACKGROUND.value

    def render(self, text: str, color, pos: Pos, shadow: bool = False) -> pygame.Surface:
        """Render text"""
        try:
            if shadow:
                shadow_img = self.font.render(text, False, self.shadow)
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
        self.angle = 15
        self.font_size = 80
        self.font = pygame.font.Font("assets/fonts/Minecraft.ttf", self.font_size)
        self.header_text_percentage = 1.0
        self.header_offset_amount = 0.005
        self.header_min_percentage = 0.9
        self.header_max_percentage = 1.1
        self.header_increasing = True
    
    def increment_header_font_size(self) -> None:
        """Set font size"""
        self.header_text_percentage += self.header_offset_amount if self.header_increasing else -self.header_offset_amount
        if self.header_text_percentage >= self.header_max_percentage: self.header_increasing = False
        elif self.header_text_percentage <= self.header_min_percentage: self.header_increasing = True

        self.font = pygame.font.Font("assets/fonts/Minecraft.ttf", round(self.header_text_percentage * self.font_size))

class HeadingText(Text):
    """Custom heading text"""
    def __init__(self, screen: pygame.Surface) -> None:
        super().__init__(screen)
        self.font = pygame.font.Font("assets/fonts/Minecraft.ttf", 70)

class ButtonText(Text):
    """Custom button text"""
    def __init__(self, screen: pygame.Surface) -> None:
        super().__init__(screen)
        self.font = pygame.font.Font("assets/fonts/Minecraft.ttf", 40)