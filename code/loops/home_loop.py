import pygame
from misc.settings import *
from misc.logger import log
from misc.game_state import GameState
from objects.pos import Pos
from objects.button import Button
from text.text import HeaderText
from loops.game_loop import GameLoop, EndReason
from pygame import mixer

class HomeLoop:
    """Home loop class"""

    def __init__(self, screen: pygame.Surface, main_loop, game_loop) -> None:
        self.screen = screen
        self.header_text = HeaderText(self.screen)
        self.buttons = []
        self.main_loop = main_loop
        self.game_loop = game_loop
        self.generate_buttons()
        self.is_init = False

    def generate_buttons(self):
        self.generate_single_button(self.play_button_callback, 
                                    Pos(SCREEN_WIDTH / 2, round(SCREEN_HEIGHT * 0.45)), 
                                    "PLAY")
        self.generate_single_button(self.quit_button_callback,
                                    Pos(SCREEN_WIDTH / 2, round(SCREEN_HEIGHT * 0.55)), 
                                    "QUIT")

    def generate_single_button(self, callback, pos: Pos, text: str):
        """Generate single button"""
        button = Button(self.screen, callback)
        button_position = pos
        button_args = (text, self.header_text.primary, button_position)
        button_rect = button.render(*button_args)
        self.buttons.append([button_rect, button, button_args])

    def tick(self):
        if not self.is_init:
            pygame.mixer.music.load("assets/home.wav")
            pygame.mixer.music.play(-1)
            self.is_init = True
            
        """Tick home screen"""
        # Render background
        self.screen.fill(self.header_text.dark_background)
        
        # Render title
        title_position = Pos(SCREEN_WIDTH / 2, round(SCREEN_HEIGHT * 0.2))
        self.header_text.render("FIVE NIGHTS IN NEWCASTLE", self.header_text.primary, title_position, True)
        self.header_text.increment_header_font_size()

        # Render buttons
        for button in self.buttons:
            button[1].render(*button[2])

        # Reload screen
        pygame.display.flip()

    def check_pressed(self, event):
        """Check if button is pressed"""
        for button in self.buttons:
            button[0].check_pressed(event)

    def check_hover(self):
        """Check if button is hovered"""
        for button in self.buttons:
            if button[0].check_hover():
                button[1].highlighted = True
            else:
                button[1].highlighted = False

    #############
    # Callbacks #
    #############

    def play_button_callback(self):
        log("Play button pressed")
        self.main_loop.current_game_state = GameState.GAME
        self.game_loop.start_time = GameLoop.get_current_time()
        self.game_loop.game_ended = EndReason.END_NONE
        try: self.game_loop.countdown_timer_thread.start()
        except Exception as _: pass

    def quit_button_callback(self):
        log("Quit button pressed")
        self.main_loop.current_game_state = GameState.QUIT