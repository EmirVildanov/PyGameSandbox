import os

import pygame

from src.constants.main_constants import BACKGROUND_SPRITES_FOLDER

FIRST_LOCATION_WIDTH = 1600
FIRST_LOCATION_HEIGHT = 1200
FIRST_LOCATION_MOUSE_START_ANGLE_POSITION = 0
PLAYER_FIRST_LOCATION_START_COORDINATES = (FIRST_LOCATION_WIDTH / 2, FIRST_LOCATION_HEIGHT / 2)
FIRST_LOCATION_NAME = "Room"
FIRST_LOCATION_BACKGROUND = pygame.image.load(os.path.join(BACKGROUND_SPRITES_FOLDER, "Room.jpg"))
