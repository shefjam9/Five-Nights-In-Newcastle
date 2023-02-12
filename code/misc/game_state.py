from enum import Enum
from misc.settings import *

class GameState(Enum):
    """Enum for game states"""
    HOME = 1
    GAME = 2
    QUIT = 3
    WIN = 4
    DEAD = 5