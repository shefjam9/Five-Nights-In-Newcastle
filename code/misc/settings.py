import pygame

SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720

def check_full_screen():
    """Check if the game should be full screen"""
    global SCREEN_WIDTH, SCREEN_HEIGHT
    # Make it full screen
    screen = pygame.display.set_mode()
    x, y = screen.get_size()
    if not(x == 0 or y == 0):
        SCREEN_WIDTH = x
        SCREEN_HEIGHT = y

# Check full screen
check_full_screen()