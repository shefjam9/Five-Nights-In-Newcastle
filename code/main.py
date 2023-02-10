import pygame
from objects.player import Player

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

# Create a screen and player
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
player = Player()

def run_game():
    # Game loop
    running = True

    # Main loop
    while running:
        # for loop through the event queue
        for event in pygame.event.get():
            # Check for KEYDOWN event
            if event.type == KEYDOWN:
                # If the Esc key is pressed, then exit the main loop
                if event.key == K_ESCAPE:
                    running = False
            # Check for QUIT event. If QUIT, then set running to false.
            elif event.type == QUIT:
                running = False

        # Fill the screen with black
        screen.fill((0, 0, 0))

        # Draw the player on the screen
        screen.blit(player.surf, (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))

        # Update the display
        pygame.display.flip()


if __name__ == "__main__":
    run_game()