from enum import Enum


class GameState(Enum):
    MENU = 0
    IN_PROGRESS = 1
    PAUSED = 2
    FINISHED = 3
