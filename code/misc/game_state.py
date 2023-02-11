from enum import Enum
from misc.settings import *

class GameState(Enum):
    """Enum for game stat"""
    HOME = 1
    GAME = 2
GameState = Enum("GameState", ["HOME", "GAME"])