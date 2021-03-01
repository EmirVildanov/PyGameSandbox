import sys
import os

import pygame

pygame.init()

APP_NAME = 'Shooter'
APP_FONT = 'Comic Sans MS'
CAMERA_WIDTH = 1000
CAMERA_HEIGHT = 800
FPS = 60
ONE_STEP_IN_PX = 10
BULLET_STEP_IN_PX = 1
BULLET_SPEED = 100

ALPHA = (255, 255, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
HOVERED_COLOR = (97, 103, 165)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

APP_FOLDER = os.path.dirname(os.path.realpath(sys.argv[0]))
SPRITES_FOLDER = "sprites"
SOUND_FOLDER = "sound"
PLAYER_SPRITES_FOLDER = os.path.join(SPRITES_FOLDER, "Player")
BACKGROUND_SPRITES_FOLDER = os.path.join(SPRITES_FOLDER, "Background")


SNOW_WALK_SOUND = pygame.mixer.Sound(os.path.join(APP_FOLDER, SOUND_FOLDER, "walk_snow.wav"))
PISTOL_SHOT_SOUND = pygame.mixer.Sound(os.path.join(APP_FOLDER, SOUND_FOLDER, "gun_shot.wav"))
BULLET_SHELL_SOUND = pygame.mixer.Sound(os.path.join(APP_FOLDER, SOUND_FOLDER, "gun_shot_ground_fall.wav"))
BULLET_METAL_HIT_SOUND = pygame.mixer.Sound(os.path.join(APP_FOLDER, SOUND_FOLDER, "hit_wall.wav"))

GAME_IMAGE = pygame.image.load(os.path.join(APP_FOLDER, SPRITES_FOLDER, "shooter.png"))
PLAYER_IMAGE = pygame.image.load(os.path.join(APP_FOLDER, PLAYER_SPRITES_FOLDER, "circle.png"))
