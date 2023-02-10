import sys
import pygame

# Keyboard inputs
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
# Initialize pygame
pygame.init()

# Create a screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

def run_game():
    # Game loop
    running = True

    # Main loop
    while running:
    # Look at every event in the queue
        for event in pygame.event.get():
            # Did the user hit a key?
            if event.type == KEYDOWN:
                # Was it the Escape key? If so, stop the loop.
                if event.key == K_ESCAPE:
                    running = False

            # Did the user click the window close button? If so, stop the loop.
            elif event.type == QUIT:
                running = False

        # Fill the screen with white
        screen.fill((255, 255, 255))

            # Update


if __name__ == "__main__":
    run_game()