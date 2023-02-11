import pygame
import time
import math

from objects.player import Player
from pygame.locals import K_ESCAPE, KEYDOWN, QUIT
from settings import *
from logger import log

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Five Nights at Newcastle")

# Creating background image
bg_img = pygame.image.load("assets/newcastle.png").convert()

"""
CHeck if a tile is visible on the screen, if it is not delete it
If it's not visible on the screen, then that means that a new tile needs to be made in the opposite direction to which it's not visible on the screen
If a tile is not fully visible on the screen (all 4 points), then check which points are off the screen, then create a tile in the opposite direction

E.g. if there are 3x3 tiles on the screen:
______
|x x x|
|x . x|
|x x x|
______

Then if the player moves left a bit, the screen would look like this:
  ______
x|x x x|
x|. x x|
x|x x x|
  ______

So the left tiles which were made are only half visible, as are the right tiles, but the other half compared to the left.
"""

_entities = []

def add_entity(entity: pygame.sprite.Sprite):
    """
    Add an entity to the game (needs update method)
    """
    _entities.append(entity)

def remove_entity(entity: pygame.sprite.Sprite):
    """
    Removes entity
    """
    _entities.remove(entity)

def get_current_time() -> float:
    """
    Return current time in ms
    """
    return time.perf_counter() * 1e3

def run_game():
    """Main game loop"""
    running = True
    player = Player()
    add_entity(player)

    # Generate background tiles
    tile = [0, 0]

    # Main loop
    while running:
        # Event loop
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            elif event.type == QUIT:
                running = False

        # Update pressed keys
        pressed_keys = pygame.key.get_pressed()
        # update entities
        for ent in _entities:
          ent.update(pressed_keys, get_current_time())

        # Render background
        screen.fill((255, 0, 0))
        tile_x = tile[0]
        tile_y = tile[1]

        if tile_x > -bg_img.get_width() - player.rel.x:
            screen.blit(bg_img, (tile_x, tile_y))
        elif tile_x > SCREEN_WIDTH + bg_img.get_width():
            continue

        tile_x = -player.rel.x
        tile_y = -player.rel.y
        tile = [tile_x, tile_y]
        

        # Render entities
        for ent in _entities:
            screen.blit(ent.surf, ent.rect)
        pygame.display.flip()


if __name__ == "__main__":
    log("Loading game...", type="info")
    log(f"Screen size: {SCREEN_WIDTH}x{SCREEN_HEIGHT}")
    run_game()