import pygame
from text.text import HeaderText
from misc.logger import log
from objects.pos import Pos
from objects.button import Button
from misc.game_state import GameState
from misc.settings import *

class Win():
    """THe player won?!"""

    def __init__(self, screen, player, main_loop) -> None:
        self.screen = screen
        self.player = player
        self.main_loop = main_loop
        self.buttons = []
        self.header_text = HeaderText(self.screen)
        self.generate_buttons()

    def generate_buttons(self):
        self.generate_single_button(self.back_to_home_button_callback, 
                                    Pos(SCREEN_WIDTH / 2, round(SCREEN_HEIGHT * 0.45)), 
                                    "BACK")
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
        """Game update"""
        self.screen.fill(self.header_text.dark_background)

        title_position = Pos(SCREEN_WIDTH / 2, round(SCREEN_HEIGHT * 0.2))
        self.header_text.render("You survived...", self.header_text.primary, title_position, True)

        # Render buttons
        for button in self.buttons:
            button[1].render(*button[2])

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

    def back_to_home_button_callback(self):
        log("Play button pressed")
        self.main_loop.current_game_state = GameState.HOME
        try: self.game_loop.countdown_timer_thread.start()
        except Exception as _: pass

    def quit_button_callback(self):
        log("Quit button pressed")
        self.main_loop.current_game_state = GameState.QUIT