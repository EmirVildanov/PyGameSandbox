from math import sqrt

import pygame, pygame.mixer

from objects.bullet import Bullet
from objects.camera import Camera
from attributes.constants import *
from src.game_state import GameState
from objects.player import Player, FIRST_LOCATION_BACKGROUND
from utils.coordinates_helper import is_outside_screen, is_collide_collider, \
    is_bullet_collide_collider
from utils.event_handling import is_movement_event_key
from utils.yaml_worker import initialize_colliders


def initialize_screen():
    screen = pygame.display.set_mode((CAMERA_WIDTH, CAMERA_HEIGHT))
    background_box = screen.get_rect()
    pygame.display.set_icon(GAME_IMAGE)
    pygame.display.set_caption(APP_NAME)
    return screen, FIRST_LOCATION_BACKGROUND, background_box


class Game:
    def __init__(self):
        clock = pygame.time.Clock()
        camera = Camera()
        screen, background, background_box = initialize_screen()
        colliders_list = initialize_colliders()
        self.camera = camera
        self.bullet_list = pygame.sprite.Group()
        self.colliders_list = colliders_list
        self.pressed_movement_buttons_list = []
        self.player = Player(colliders_list, camera)
        self.clock = clock
        self.screen, self.background, self.background_box = screen, background, background_box
        self.state = GameState.MENU
        self.clickable_objects = set()
        self.hoverable_objects = set()
        self.bullets = pygame.sprite.Group()

    def start(self):
        while self.state == GameState.MENU:
            for event in pygame.event.get():
                self.handle_event(event)
            self.player.update()
            self.camera.update(self.player)
            self.screen.blit(self.background, (-self.camera.rect.x, -self.camera.rect.y))
            for bullet in self.bullet_list:
                bullet.update()
                if is_bullet_collide_collider(bullet):
                    BULLET_METAL_HIT_SOUND.play()
                    self.bullet_list.remove(bullet)
                if is_outside_screen(bullet):
                    self.bullet_list.remove(bullet)
            self.screen.blit(self.player.image, self.camera.apply(self.player))

            self.bullet_list.draw(self.screen)

            pygame.draw.line(self.screen, BLACK, self.camera.apply(self.player).center, pygame.mouse.get_pos())
            pygame.display.update()
            self.clock.tick(FPS)
        while self.state != GameState.FINISHED:
            while self.state == GameState.PAUSED:
                for event in pygame.event.get():
                    self.handle_event(event)
                pygame.display.update()
                self.clock.tick(FPS)
            for event in pygame.event.get():
                self.handle_event(event)
            pygame.display.update()

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.QUIT:
            self.state = GameState.FINISHED
        elif event.type == pygame.KEYDOWN:
            self.handle_key_down_event(event)
        elif event.type == pygame.KEYUP:
            self.handle_key_up_event(event)
        elif event.type == pygame.MOUSEMOTION:
            self.handle_mouse_motion_event()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_mouse_down_event()

    def handle_key_down_event(self, event: pygame.event.Event):
        if event.key == pygame.K_ESCAPE:
            self.state = GameState.FINISHED
        elif is_movement_event_key(event.key):
            self.handle_movement_key_down(event.key)

    def handle_movement_key_down(self, key):
        if len(self.pressed_movement_buttons_list) == 0:
            SNOW_WALK_SOUND.play()
        wanted_movement = ()
        if key == pygame.K_LEFT or key == ord('a'):
            wanted_movement = (-ONE_STEP_IN_PX, 0)
        elif key == pygame.K_RIGHT or key == ord('d'):
            wanted_movement = (ONE_STEP_IN_PX, 0)
        elif key == pygame.K_UP or key == ord('w'):
            wanted_movement = (0, -ONE_STEP_IN_PX)
        elif key == pygame.K_DOWN or key == ord('s'):
            wanted_movement = (0, ONE_STEP_IN_PX)
        self.pressed_movement_buttons_list.append(key)
        self.player.control(wanted_movement[0],
                            wanted_movement[1])

    def handle_movement_key_up(self, key):
        if key in self.pressed_movement_buttons_list:
            if key == pygame.K_LEFT or key == ord('a'):
                self.player.control(ONE_STEP_IN_PX, 0)
            elif key == pygame.K_RIGHT or key == ord('d'):
                self.player.control(-ONE_STEP_IN_PX, 0)
            elif key == pygame.K_UP or key == ord('w'):
                self.player.control(0, ONE_STEP_IN_PX)
            elif key == pygame.K_DOWN or key == ord('s'):
                self.player.control(0, -ONE_STEP_IN_PX)
            self.pressed_movement_buttons_list.remove(key)
            if len(self.pressed_movement_buttons_list) == 0:
                SNOW_WALK_SOUND.stop()

    def handle_key_up_event(self, event: pygame.event.Event):
        if is_movement_event_key(event.key):
            self.handle_movement_key_up(event.key)

    def handle_mouse_motion_event(self):
        for element in self.hoverable_objects:
            if element.rect.collidepoint(pygame.mouse.get_pos()):
                element.fill(RED)

    def handle_mouse_down_event(self):
        self.shot_bullet()

    def shot_bullet(self):
        PISTOL_SHOT_SOUND.play()
        BULLET_SHELL_SOUND.play()
        bullet = Bullet(self.colliders_list)
        bullet.rect.x = self.camera.apply(self.player).center[0]
        bullet.rect.y = self.camera.apply(self.player).center[1]
        vector_x = pygame.mouse.get_pos()[0] - bullet.rect.x
        vector_y = pygame.mouse.get_pos()[1] - bullet.rect.y
        vector_length = sqrt(vector_x ** 2 + vector_y ** 2)
        vector_x = vector_x / vector_length * BULLET_SPEED
        vector_y = vector_y / vector_length * BULLET_SPEED
        bullet.control(vector_x, vector_y)
        self.bullet_list.add(bullet)
