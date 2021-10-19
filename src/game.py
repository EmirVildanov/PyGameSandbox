from math import sqrt, cos, sin, radians
from typing import Tuple, Union, Any

import pygame.mixer
from pygame.rect import RectType
from pygame.surface import SurfaceType

from src.constants.raytracing_constants import RAY_TRACING_CAMERA_WIDTH, RAY_TRACING_CAMERA_HEIGHT
from src.game_type import GameType
from src.mvc.controller import KeyboardController, MouseController, CPUSpinnerController
from src.mvc.event import EventManager
from src.mvc.view import PygameView
from src.objects.bullet import Bullet
from src.objects.camera import Camera
from src.constants.main_constants import *
from src.objects.player import Player
from src.constants.locations_constants import *
from src.utils.coordinates_helper import is_collide_rect_with_xy
from src.utils.yaml_worker import initialize_colliders


class Game:
    def __init__(self):
        self.game_type = GameType.RAY_CASTING
        camera = Camera()
        screen, background, background_box = self.initialize_screen()
        self.camera = camera
        self.bullet_list = pygame.sprite.Group()
        self.colliders_list = initialize_colliders()
        self.player = Player(self, camera)
        self.screen, self.background, self.background_box = screen, background, background_box
        self.first_person_mouse_angle = FIRST_LOCATION_MOUSE_START_ANGLE_POSITION
        self.first_person_mouse_previous_position = None
        self.clickable_objects = set()

    def initialize_screen(self) -> Tuple[Union[pygame.Surface, SurfaceType], Any, Union[Union[pygame.Rect, RectType], Any]]:
        if self.game_type is GameType.RAY_TRACING:
            screen = pygame.display.set_mode((RAY_TRACING_CAMERA_WIDTH, RAY_TRACING_CAMERA_HEIGHT))
        else:
            screen = pygame.display.set_mode((CAMERA_WIDTH, CAMERA_HEIGHT))
        background_box = screen.get_rect()
        pygame.display.set_icon(GAME_IMAGE)
        pygame.display.set_caption(APP_NAME)
        return screen, FIRST_LOCATION_BACKGROUND, background_box

    def start(self):
        if self.game_type == GameType.RAY_CASTING or self.game_type == GameType.RAY_TRACING:
            pygame.mouse.set_visible(False)
            pygame.event.set_grab(True)
        pygame_view = PygameView(self, self.screen)
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
        if self.game_type == GameType.RAY_CASTING or self.game_type == GameType.RAY_TRACING:
            x_motion, y_motion = self.calculate_motion_for_first_person_view()
        else:
            x_motion = player.move_x
            y_motion = player.move_y
        player_rect = player.rect
        for collider in self.colliders_list:
            allowed_movement_axis = self.check_collider_collision(allowed_movement_axis, collider, player_rect,
                                                                  x_motion, y_motion)
        allowed_movement_axis = self.check_location_wall_collision(allowed_movement_axis, player_rect, x_motion,
                                                                   y_motion)
        return allowed_movement_axis

    def calculate_motion_for_first_person_view(self):
        x_motion = self.player.move_x * cos(
            radians(180 - self.first_person_mouse_angle)) - self.player.move_y * sin(
            radians(180 - self.first_person_mouse_angle))
        y_motion = self.player.move_x * sin(
            radians(180 - self.first_person_mouse_angle)) - self.player.move_y * cos(
            radians(180 - self.first_person_mouse_angle))
        return x_motion, y_motion

    def check_collider_collision(self, allowed_movement_axis, collider, player_rect, x_motion, y_motion):
        if is_collide_rect_with_xy(player_rect, collider, x_motion, 0)\
                and not is_collide_rect_with_xy(player_rect, collider, 0, y_motion):
            allowed_movement_axis[0] = False
        elif is_collide_rect_with_xy(player_rect, collider, 0, y_motion)\
                and not is_collide_rect_with_xy(player_rect, collider, x_motion, 0):
            allowed_movement_axis[1] = False
        elif is_collide_rect_with_xy(player_rect, collider, x_motion, y_motion):
            allowed_movement_axis[0] = False
            allowed_movement_axis[1] = False
        return allowed_movement_axis

    def check_location_wall_collision(self, allowed_movement_axis, player_rect, x_motion, y_motion):
        if player_rect.x + x_motion <= 0 or player_rect.right + x_motion >= FIRST_LOCATION_WIDTH:
            allowed_movement_axis[0] = False
        if player_rect.y + y_motion <= 0 or player_rect.bottom + y_motion >= FIRST_LOCATION_HEIGHT:
            allowed_movement_axis[1] = False
        return allowed_movement_axis
