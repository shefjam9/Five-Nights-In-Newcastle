import pygame

class Obstacle:

    def __init__(self, time, x, y):
        self.placementTime = time
        self.startX, self.startY = x, y

    def update(keys_pressed, time):
        raise NotImplementedError("Obstacle needs update method")
