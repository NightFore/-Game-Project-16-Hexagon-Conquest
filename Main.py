import pygame
import random
from math import *
from pygame.locals import *
from os import path
from Class import *
from Function import *
from Hexagon import *
from Settings import *
from ScaledGame import *


class Game:
    def __init__(self, main):
        # Game Initialization
        self.main = main
        self.game = self
        self.load()
        self.new()

    def load(self):
        pass

    def new(self):
        self.hexagons = init_hexagons(flat_top=False)

    def draw(self):
        draw_hexagon(self.gameDisplay, self.hexagons)

    def update(self):
        for hexagon in self.hexagons:
            hexagon.update()

    def ui_new_game(self):
        # Initialization
        self.main.update_menu()

MAIN_DICT = {
    # Init (Settings) ----------------- #
    "game": {
        "project_title": "Hexagon", "screen_size": (1280, 720), "FPS": 60,
        "default_music_volume": 5, "default_sound_volume": 75,
        "key_repeat": (100, 30)},


    # Game (Settings) ----------------- #
    "settings": {
    },


    # Game (Interface) ---------------- #
    "interface_box": {
        1: {"pos": [390, 10]},
        2: {"pos": [710, 10]},
        3: {"pos": [900, 10]},
        4: {"pos": [1090, 10]},
    },

    "interface_castle": {
        1: {"pos": [20, 520]},
        2: {"pos": [980, 520]}

    },



    # Background Dict ----------------- #
    "background": {
        None: None,
        "default": {
            "color": DARK_SKY_BLUE,
            "image": None,
        },
    },


    # Music Dict ---------------------- #
    "music": {
        "default": None,
    },


    # Sound Dict ---------------------- #
    "sound": {
    },


    # Font Dict ----------------------- #
    "font": {
        "default": {"ttf": None, "size": 100},
        "LiberationSerif": {"ttf": "LiberationSerif-Regular.ttf", "size": 40},
        "LiberationSerif_30": {"ttf": "LiberationSerif-Regular.ttf", "size": 30}
    },


    # Menu Dict ----------------------- #
    "menu": {
        "main_menu": {
            "background": "default",
            "music": "default",
        },
    },


    # Button Dict --------------------- #
    "button": {
        "settings": {
            "default": {
                "size": (280, 50), "border_size": (5, 5), "align": "nw",
                "font": "LiberationSerif", "font_color": WHITE, "text_align": "center",
                "inactive_color": LIGHT_SKY_BLUE, "active_color": DARK_SKY_BLUE, "border_color": BLACK,
                "sound_action": None, "sound_active": None, "sound_inactive": None},
        },
        "main_menu": {
            "new_game": {"settings": "default", "pos": [10, 70], "text": "New Game", "action": "self.game.ui_new_game"},
        },
    },
}
