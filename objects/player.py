import pygame

from attributes.constants import *
from attributes.locations import *
from utils.coordinates_helper import is_collide_collider


class Player(pygame.sprite.Sprite):
    def __init__(self, blocks, camera):
        pygame.sprite.Sprite.__init__(self)
        self.camera = camera
        self.move_x = 0
        self.move_y = 0
        player_image = PLAYER_IMAGE.convert()
        player_image.convert_alpha()
        player_image.set_colorkey(ALPHA)
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.x = PLAYER_FIRST_LOCATION_START_COORDINATES[0]
        self.rect.y = PLAYER_FIRST_LOCATION_START_COORDINATES[1]
        self.blocks = blocks

    def control(self, x, y):
        self.move_x += x
        self.move_y += y

    def update(self):
        x_motion = self.move_x
        y_motion = self.move_y
        for block in self.blocks:
            if is_collide_collider(self.rect, block, self.move_x, 0) and not is_collide_collider(self.rect, block, 0, self.move_y):
                y_motion = self.move_y
                x_motion = 0
            elif is_collide_collider(self.rect, block, 0, self.move_y) and not is_collide_collider(self.rect, block, self.move_x, 0):
                x_motion = self.move_x
                y_motion = 0
            elif is_collide_collider(self.rect, block, self.move_x, self.move_y):
                x_motion = 0
                y_motion = 0
            if self.rect.x + self.move_x <= 0 or self.rect.right + self.move_x >= FIRST_LOCATION_WIDTH:
                x_motion = 0
            if self.rect.y + self.move_y <= 0 or self.rect.bottom + self.move_y >= FIRST_LOCATION_HEIGHT:
                y_motion = 0
        self.rect.x = self.rect.x + x_motion
        self.rect.y = self.rect.y + y_motion
