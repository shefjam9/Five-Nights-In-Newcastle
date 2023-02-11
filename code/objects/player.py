import pygame
from misc.settings import *
from pygame.locals import K_w, K_s, K_a, K_d
from objects.pos import Pos

class Player(pygame.sprite.Sprite):
    def __init__(self, bg_img: pygame.Surface):
        """Initialize the player"""
        super(Player, self).__init__()

        # Initialize the player surface
        self.surf = pygame.Surface((75, 25))
        self.surf.fill((0, 0, 0))
        self.rect = self.surf.get_rect()

        # Speeds and health
        self.health = 100
        self.default_speed = 1
        self.sprint_speed = 2
        self.speed = self.default_speed

        # Collisions
        self.bg_img = bg_img
        self.wall = (75, 221, 161, 255)
        self.collision = False
        self.entities = []
        self.ignore_entity_collision = []

        # Move player
        self.start_pos = Pos(SCREEN_CENTER[0], SCREEN_CENTER[1])
        self.rect.move_ip(self.start_pos.to_tuple())
        self.bg_tile = []

        # Relative positions
        self.rel = self.start_pos
        self.obj_offset = Pos(0, 0)

    def boundary_check(self):
        """Check if player is within screen bounds"""
        return (self.rect.left > 300 and self.rect.right < SCREEN_WIDTH  - 300
                and self.rect.top > 150 and self.rect.bottom < SCREEN_HEIGHT - 150)

    def set_bg_tile(self, bg_tile):
        """Set bg tile position"""
        self.bg_tile = bg_tile

    def set_entities(self, entities):
        """Set entities for collision"""
        self.entities = entities

    def set_sprint(self, is_sprinting):
        """Set sprint speed"""
        if is_sprinting:
            self.speed = self.sprint_speed
        else:
            self.speed = self.default_speed

    def damage(self, ent):
        """Damage player"""
        if not ent.has_damaged:
            self.health -= ent.damage_amount
            ent.has_damaged = True
            print(self.health)

    def add_ignore_entity_collision(self, entity):
        """Add entity to ignore collision"""
        self.ignore_entity_collision.append(entity)

    def update(self, key_pressed):
        """Update the player position based on key presses"""
        has_moved = False
        if self.boundary_check():
            self.collision = False

        key_results = {K_w: (0, -self.speed), K_s: (0, self.speed), 
                       K_a: (-self.speed, 0), K_d: (self.speed, 0)}
        for key in key_results:
            hit_boundary = self.increment_boundary(key_pressed, key, key_results)
            if hit_boundary:
                self.bg_tile[0] -= key_results[key][0]
                self.bg_tile[1] -= key_results[key][1]
                self.obj_offset.x -= key_results[key][0]
                self.obj_offset.y -= key_results[key][1]
                self.rect.move_ip(-key_results[key][0], -key_results[key][1])
            if self.check_collision(self.wall):
                self.rel.x -= key_results[key][0]
                self.rel.y -= key_results[key][1]
                self.rect.move_ip(-key_results[key][0], -key_results[key][1])
                has_moved = False
            for ent in self.entities:
                if ent != self:
                    if self.check_entity_collision(ent):
                        if ent not in self.ignore_entity_collision:
                            self.rel.x -= key_results[key][0]
                            self.rel.y -= key_results[key][1]
                            self.rect.move_ip(-key_results[key][0], -key_results[key][1])
                            has_moved = False
                        self.damage(ent)
        return has_moved
    
    def increment_boundary(self, key_pressed, key, key_results):
        """Move the player and check to see if they hit a wall, if they
        did the move back and return True, else return False"""
        hit_boundary = False
        if key_pressed[key] and self.boundary_check():
            self.rect.move_ip(key_results[key])
            self.rel.x += key_results[key][0]
            self.rel.y += key_results[key][1]

            # Make sure the player doesn't get stuck in the wall by moving
            # them back if they are
            if not self.boundary_check():
                self.rel.x -= key_results[key][0]
                self.rel.y -= key_results[key][1]
                self.rect.move_ip(-key_results[key][0], -key_results[key][1])
                hit_boundary = True
        return hit_boundary


    def check_collision(self, color):
        """Check if entity collides with any other entity"""
        try:
            if self.bg_img.get_at((round(self.rect.left - self.bg_tile[0]), round(self.rect.top - self.bg_tile[1]))) == color:
                return True
            elif self.bg_img.get_at((round(self.rect.left - self.bg_tile[0]), round(self.rect.bottom - self.bg_tile[1]))) == color:
                return True
            elif self.bg_img.get_at((round(self.rect.right - self.bg_tile[0]), round(self.rect.top - self.bg_tile[1]))) == color:
                return True
            elif self.bg_img.get_at((round(self.rect.right - self.bg_tile[0]), round(self.rect.bottom - self.bg_tile[1]))) == color:
                return True
        except Exception as e:
            print(e)
        return False
    
    def check_entity_collision(self, ent):
        """Check if player collides with any other entity"""
        return pygame.Rect.colliderect(self.rect, ent)
