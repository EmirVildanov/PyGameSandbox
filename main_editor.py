import pygame.freetype
from level_editor.editor import Editor

if __name__ == '__main__':
    pygame.init()
    editor = Editor(1)
    editor.start()
