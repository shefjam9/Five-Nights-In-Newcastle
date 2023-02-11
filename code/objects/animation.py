import pygame
import random


class Animation:
    

    def __init__(self, path: str, w: int, h: int, num_frames: int, upf: int, upper_bound: int = 0):
        """
        path: path to sprite sheet
        w: width of one frame
        h: height of one frame
        num_frames: number of frames in the animation
        upf: updates per frame
        """
        self.tex = pygame.image.load(path).convert_alpha()
        self.current_frame = 0
        self.current_updates = 0
        self.num_frames = num_frames
        # scaling animation
        if h != self.tex.get_height():
            self.tex = pygame.transform.scale(self.tex, (w*num_frames, h))
        self.width, self.height = w, h
        if not upper_bound:
          self.updates_per_frame = upf
        else:
            self.updates_per_frame = random.randint(upf, upper_bound)
    
    def update(self, time):
        """ Update animation so frames change """
        if self.current_updates >= self.updates_per_frame:
            self.current_frame = (self.current_frame+1)%self.num_frames
            self.current_updates -= self.updates_per_frame
        self.current_updates+=1
    
    def render_frame(self, surface: pygame.Surface, x: int, y: int) -> None:
        """ render the current animation """
        surface.blit(self.tex, (x, y), (self.current_frame*self.width, 0, self.width, self.height))