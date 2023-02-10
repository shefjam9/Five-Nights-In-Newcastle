import pygame
from obstacle import Obstacle
from logger import log

class Glass(Obstacle):

    def __init__(self, time: float, x: int, y: int):
        super().__init__(time, x, y)
        

    def update(keys, time):
       # TODO
       # update animation sequence
       # determine if finished falling?
       pass
