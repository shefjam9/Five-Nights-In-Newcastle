import pygame
import globals


class Animation:
    

    def __init__(self, path: str, num_frames, FPS: int):
        self._image = pygame.image.load(path).convert_alpha()
        self._currentframe = 0
        self._frame_time = 1e3/FPS
        self._last_time = -1
        self._acc_time = 0
        self._num_frames = num_frames
    
    def update(self, time):
        if self._last_time < 0:
            self._last_time = time
            return
        self._acc_time += (time - self._last_time)
        if self._acc_time >= self._frame_time:
            self._currentframe = (self._currentframe + 1) % self._num_frames
            self._acc_time -= self._frame_time
        self._last_time = time

    def render(self, surface, x, y):
        surface.blit(self._image, (x, y), pygame.Rect(globals.TILE_SIZE*self._currentframe, 0, 
                                                      globals.TILE_SIZE, globals.TILE_SIZE))
        