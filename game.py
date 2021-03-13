from math import sqrt, cos, sin, radians
from typing import Tuple, Union, Any

import pygame, pygame.mixer
from pygame.rect import RectType
from pygame.surface import SurfaceType

from mvc.controller import KeyboardController, MouseController, CPUSpinnerController
from mvc.event import EventManager
from mvc.view import PygameView
from objects.bullet import Bullet
from objects.camera import Camera
from attributes.constants import *
from objects.player import Player
from attributes.locations import *
from utils.coordinates_helper import is_collide_rect_with_xy
from utils.yaml_worker import initialize_colliders


class Game:
    @staticmethod
    def initialize_screen() -> Tuple[Union[pygame.Surface, SurfaceType], Any, Union[Union[pygame.Rect, RectType], Any]]:
        screen = pygame.display.set_mode((CAMERA_WIDTH, CAMERA_HEIGHT))
        background_box = screen.get_rect()
        pygame.display.set_icon(GAME_IMAGE)
        pygame.display.set_caption(APP_NAME)
        return screen, FIRST_LOCATION_BACKGROUND, background_box

    def __init__(self):
        camera = Camera()
        screen, background, background_box = self.initialize_screen()
        self.camera = camera
        self.bullet_list = pygame.sprite.Group()
        self.colliders_list = initialize_colliders()
        self.player = Player(self, camera)
        self.screen, self.background, self.background_box = screen, background, background_box
        self.level_index = 3
        self.first_person_mouse_angle = FIRST_LOCATION_MOUSE_START_ANGLE_POSITION
        self.first_person_mouse_previous_position = None
        self.clickable_objects = set()
        self.hoverable_objects = set()

    def start(self):
        if self.level_index == 3:
            pygame.mouse.set_visible(False)
            pygame.event.set_grab(True)
        pygame_view = PygameView(self)
        event_manager = EventManager()

        keyboard = KeyboardController(self, event_manager)
        mouse = MouseController(self, event_manager)
        spinner = CPUSpinnerController(self, pygame_view, event_manager)

        event_manager.register_listener(keyboard)
        event_manager.register_listener(mouse)
        event_manager.register_listener(spinner)
        spinner.run()

    def shot_bullet(self):
        PISTOL_SHOT_SOUND.play()
        BULLET_SHELL_SOUND.play()
        bullet = Bullet()
        bullet.rect.x = self.camera.apply(self.player).center[0]
        bullet.rect.y = self.camera.apply(self.player).center[1]
        vector_x = pygame.mouse.get_pos()[0] - bullet.rect.x
        vector_y = pygame.mouse.get_pos()[1] - bullet.rect.y
        vector_length = sqrt(vector_x ** 2 + vector_y ** 2)
        vector_x = vector_x / vector_length * BULLET_SPEED
        vector_y = vector_y / vector_length * BULLET_SPEED
        bullet.control(vector_x, vector_y)
        self.bullet_list.add(bullet)

    def control_player(self, wanted_movement: Tuple[float, float] = None):
        self.player.control(wanted_movement[0], wanted_movement[1])

    def check_collisions(self):
        player = self.player
        allowed_movement_axis = [True, True]
        if self.level_index == 3:
            x_motion = self.player.move_x * cos(
                radians(180 - self.first_person_mouse_angle)) - self.player.move_y * sin(
                radians(180 - self.first_person_mouse_angle))
            y_motion = self.player.move_x * sin(
                radians(180 - self.first_person_mouse_angle)) - self.player.move_y * cos(
                radians(180 - self.first_person_mouse_angle))
        else:
            x_motion = player.move_x
            y_motion = player.move_y
        player_rect = player.rect
        for collider in self.colliders_list:
            if is_collide_rect_with_xy(player_rect, collider, x_motion,
                                       0) and not is_collide_rect_with_xy(
                player_rect, collider, 0, y_motion):
                allowed_movement_axis[0] = False
            elif is_collide_rect_with_xy(player_rect, collider, 0,
                                         y_motion) and not is_collide_rect_with_xy(
                player_rect, collider, x_motion, 0):
                allowed_movement_axis[1] = False
            elif is_collide_rect_with_xy(player_rect, collider, x_motion, y_motion):
                allowed_movement_axis[0] = False
                allowed_movement_axis[1] = False
        if player_rect.x + x_motion <= 0 or player_rect.right + x_motion >= FIRST_LOCATION_WIDTH:
            allowed_movement_axis[0] = False
        if player_rect.y + y_motion <= 0 or player_rect.bottom + y_motion >= FIRST_LOCATION_HEIGHT:
            allowed_movement_axis[1] = False
        return allowed_movement_axis
