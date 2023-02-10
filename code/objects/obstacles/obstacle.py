import pygame

class Obstacle:

    def __init__(self, time):
        self.placementTime = time
        
    def place():
        raise NotImplementedError("Implement place method nerd🤓")

    def update(keys_pressed, time):
        raise NotImplementedError("Obstacle needs update method")
