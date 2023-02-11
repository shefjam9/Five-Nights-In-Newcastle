import pygame
import globals

_background_img: pygame.Surface = None


def init_map():
    """ Loads background image + other initialisation stuff """
    global _background_img
    _background_img = pygame.transform.scale(pygame.image.load("res\\Background.png").convert(), globals.SCREEN_DIMENSIONS)


def _render_background_map(surface: pygame.Surface):
    """ Draws background map """
    surface.blit(_background_img, (0, 0))

def render(surface: pygame.Surface):
    """ Render :) """
    _render_background_map(surface)

def update(time: float):
    pass
