import pygame
from pygame import Rect


class Collider:
    def __init__(self, x, y, width, height):
        self.rect = Rect((x, y, width, height))

    @classmethod
    def from_rect(cls, rect: pygame.Rect):
        return cls(rect.x, rect.y, rect.width, rect.height)
