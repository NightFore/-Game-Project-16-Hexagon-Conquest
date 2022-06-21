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
        self.colliding_hexagons = []
        self.hexagon_map = [
            [0, 1, 1, 1, 0],
            [1, 1, 1, 1, 1],
            [0, 0, 0, 0, 1],
            [1, 1, 0, 1, 0]
        ]
        self.map_size = len(self.hexagon_map[0]), len(self.hexagon_map)
        self.hexagons = init_hexagons(flat_top=False)

    def update(self):
        self.click = self.main.click
        self.mouse = self.main.mouse
        self.event = self.main.event

        for hexagon in self.hexagons:
            hexagon.update()

        if self.click[1]:
            for hexagon in self.colliding_hexagons:
                hexagon.color = (125, 125, 125)

    def draw(self):
        for hexagon in self.hexagons:
            hexagon.render(self.gameDisplay)

        self.colliding_hexagons = [hexagon for hexagon in self.hexagons if hexagon.collide_with_point(self.mouse)]
        for hexagon in self.colliding_hexagons:
            for neighbour in hexagon.compute_neighbours(self.hexagons):
                # neighbour.render_highlight(self.gameDisplay, border_color=(100, 100, 100))
                pass
            hexagon.render_highlight(self.gameDisplay, border_color=(0, 0, 0))


    def ui_new_game(self):
        # Initialization
        self.main.update_menu()
        self.load_map()

    def load_map(self, map=None):
        self.hexagon_map = self.hexagon_map if map is None else map
        self.map_size = len(self.hexagon_map[0]), len(self.hexagon_map)
        self.hexagons = init_hexagons(position=(300, 200), num_x=self.map_size[0], num_y=self.map_size[1], flat_top=False)

        for count in range(len(self.hexagons)):
            line = count // self.map_size[0]
            column = count % self.map_size[0]
            if self.hexagon_map[line][column] == 1:
                self.hexagons[count].color = (0, 0, 0)
            else:
                self.hexagons[count].color = (255, 255, 255)


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
