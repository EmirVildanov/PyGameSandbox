import pygame.freetype

from attributes.locations import FIRST_LOCATION_WIDTH
from level_editor.editor import Editor
from src.game import Game


if __name__ == '__main__':
    pygame.init()
    value = True
    if value:
        game = Game()
        game.start()
    else:
        screen = pygame.display.set_mode(
            (FIRST_LOCATION_WIDTH, FIRST_LOCATION_WIDTH))
        clock = pygame.time.Clock()
        editor = Editor(screen, 1)
        editor.start()
