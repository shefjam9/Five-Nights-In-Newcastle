import pygame
from objects.player import Player
from pygame.locals import K_ESCAPE, KEYDOWN, QUIT
from settings import *
from logger import log
import time

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Five Nights at Newcastle")
bg_img = pygame.image.load("assets/bg.jpg")
bg_img = pygame.transform.scale(bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

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
        screen.fill((0, 0, 0))
        screen.blit(bg_img, (player.rect.x, 0))
        screen.blit(bg_img, (0, player.rect.y))

        # Render entities
        for ent in _entities:
            screen.blit(ent.surf, ent.rect)
        pygame.display.flip()


if __name__ == "__main__":
    log("Loading game...", type="info")
    log(f"Screen size: {SCREEN_WIDTH}x{SCREEN_HEIGHT}")
    run_game()