import pygame
import time

from objects.player import Player
from pygame.locals import K_ESCAPE, KEYDOWN, QUIT, K_p, K_o
from settings import *
from logger import log
from game_state import GameState

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Five Nights at Newcastle")
current_game_state = GameState.GAME
is_player_loaded = False

# Creating background image and tiles
bg_img = pygame.image.load("assets/newcastle.png").convert()
tile = [0, 0]
player: Player

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

def main_loop():
    """Main game loop that switches between game states"""
    global current_game_state
    running = True
    while running:
        # Event loop
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                elif event.key == K_p:
                    current_game_state = GameState.HOME
                elif event.key == K_o:
                    current_game_state = GameState.GAME
            elif event.type == QUIT:
                running = False

        # Check game status
        if current_game_state == GameState.HOME:
            pass
        elif current_game_state == GameState.GAME:
            run_game()

def run_game():
    """Main game loop"""
    global is_player_loaded, tile, player
    # Generate background tiles and player
    if not is_player_loaded:
        player = Player()
        add_entity(player)
        is_player_loaded = True

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
    main_loop()