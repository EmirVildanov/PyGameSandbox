import pygame
from pygame import Rect

from attributes.locations import FIRST_LOCATION_WIDTH, FIRST_LOCATION_HEIGHT
from attributes.constants import *


def camera_configure(target_rect: pygame.Rect):
    camera_x = target_rect.x - CAMERA_WIDTH / 2  # coordinates relative to the level (0,0) coordinate
    camera_y = target_rect.y - CAMERA_HEIGHT / 2
    if camera_x < 0:
        camera_x = 0
    elif camera_x + CAMERA_WIDTH > FIRST_LOCATION_WIDTH:
        camera_x = FIRST_LOCATION_WIDTH - CAMERA_WIDTH
    if camera_y < 0:
        camera_y = 0
    elif camera_y + CAMERA_HEIGHT > FIRST_LOCATION_HEIGHT:
        camera_y = FIRST_LOCATION_HEIGHT - CAMERA_HEIGHT
    # camera_x = min(0, camera_x)  # Не движемся дальше левой границы
    # print(f"2: x: {camera_x}, y: {camera_y}")
    # camera_x = max(-(FIRST_LOCATION_WIDTH - CAMERA_WIDTH),
    #                camera_x)  # Не движемся дальше правой границы
    # print(f"3: x: {camera_x}, y: {camera_y}")
    # camera_y = max(-(FIRST_LOCATION_HEIGHT - CAMERA_HEIGHT),
    #                camera_y)  # Не движемся дальше нижней границы
    # print(f"4: x: {camera_x}, y: {camera_y}")
    # camera_y = min(0, camera_y)  # Не движемся дальше верхней границы

    return pygame.Rect(camera_x, camera_y, CAMERA_WIDTH, CAMERA_HEIGHT)


class Camera(object):
    def __init__(self):
        self.rect = Rect(0, 0, CAMERA_WIDTH, CAMERA_HEIGHT)

    def apply(self, target) -> pygame.Rect:
        return target.rect.move(-self.rect.x, -self.rect.y)

    def update(self, target):
        self.rect = camera_configure(target.rect)
