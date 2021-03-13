from math import cos, radians, sin

from attributes.constants import *
from attributes.locations import *


class Player(pygame.sprite.Sprite):
    def __init__(self, game, camera):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.camera = camera
        self.move_x = 0
        self.move_y = 0
        player_image = PLAYER_IMAGE.convert()
        player_image.convert_alpha()
        player_image.set_colorkey(ALPHA_WHITE)
        self.image = player_image
        knife_image = PLAYER_KNIFE_IMAGE
        # knife_image.convert_alpha()
        # knife_image.set_colorkey(ALPHA_STRANGE_WHITE)
        self.knife_image = knife_image
        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.x = PLAYER_FIRST_LOCATION_START_COORDINATES[0]
        self.rect.y = PLAYER_FIRST_LOCATION_START_COORDINATES[1]
        self.cadr = 0

    def control(self, x: float, y: float):
        self.move_x += x
        self.move_y += y

    def stop_axis(self, x: bool = False, y: bool = False):
        if x:
            self.move_x = 0
        if y:
            self.move_y = 0

    def update(self):
        allowed_axis = self.game.check_collisions()
        if self.game.level_index == 3:
            if allowed_axis[0]:
                self.rect.x = self.rect.x + self.move_x * cos(radians(180 - self.game.first_person_mouse_angle))
                self.rect.x = self.rect.x - self.move_y * sin(radians(180 - self.game.first_person_mouse_angle))
            if allowed_axis[1]:
                self.rect.y = self.rect.y + self.move_x * sin(radians(180 - self.game.first_person_mouse_angle))
                self.rect.y = self.rect.y - self.move_y * cos(radians(180 - self.game.first_person_mouse_angle))
        else:
            if allowed_axis[0]:
                self.rect.x = self.rect.x + self.move_x
            if allowed_axis[1]:
                self.rect.y = self.rect.y + self.move_y
        self.cadr = (self.cadr + 1) % 1000