import pygame

from misc.settings import *
from misc.logger import log
from loops.main_loop import MainLoop

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Five Nights at Newcastle")

# Creating background image and tiles
bg_img = pygame.image.load("assets/newcastle.png").convert()       


if __name__ == "__main__":
    log("Loading game...", type="info")
    log(f"Screen size: {SCREEN_WIDTH}x{SCREEN_HEIGHT}")

    # Start main loop
    main_loop = MainLoop(screen, bg_img)
    main_loop.start()