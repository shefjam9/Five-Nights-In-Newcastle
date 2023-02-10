import sys
import pygame

# Initialize pygame
pygame.init()

# Create a screen
screen = pygame.display.set_mode((800, 600))

def run_game():
    # Game loop
    running = True
    while running:
        try:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Draw background
            screen.fill((255, 255, 255))

            # Update
            pygame.display.update()
        except KeyboardInterrupt:
            running = False
            
    # End game
    pygame.quit()
    sys.exit(0)

if __name__ == "__main__":
    run_game()