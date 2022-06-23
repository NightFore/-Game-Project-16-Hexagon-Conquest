import pygame
from Button import *
from Interface import *
from Hexagon import *

class Game:
    def __init__(self, main):
        # Game Initialization
        self.main = main
        self.game = self
        self.load()
        self.new()

    def load(self):
        self.hexagon_map = [
            [0, 1, 1, 1, 0],
            [1, 1, 1, 1, 1],
            [0, 0, 0, 0, 1],
            [1, 1, 0, 1, 0]
        ]
        self.load_map()

    def new(self):
        self.colliding_hexagons = []
        self.player_worker = 5
        self.player_color = (125, 125, 125)

        self.buttons = Button(self, button_dict, "main")
        self.interfaces = Interface(self.main, interface_dict, "main")


        # WIP
        wip_dict = {
            "crystals": 500, "gas": 0, "supply": 0,
            "citizen": 5, "miner": 2, "harvester": 0, "builder": 1, "soldier": 1
        }
        self.player = Player(0, wip_dict)

    def new_game(self):
        # Initialization
        self.main.update_menu()
        self.load_map()

    def end_turn(self):
        self.player.end_turn()

    def load_map(self, map=None):
        self.hexagon_map = self.hexagon_map if map is None else map
        self.map_size = len(self.hexagon_map[0]), len(self.hexagon_map)
        self.hexagons = init_hexagons(position=(300, 200), num_x=self.map_size[0], num_y=self.map_size[1], flat_top=False)

        for index in range(len(self.hexagons)):
            line, column = self.convert_index(index)
            if self.hexagon_map[line][column] == 1:
                self.hexagons[index].color = (0, 0, 0)
            else:
                self.hexagons[index].color = (255, 255, 255)

    def convert_index(self, index):
        line = index // self.map_size[0]
        column = index % self.map_size[0]
        return line, column

    def hexagon_update(self, hexagon, line, column, player, type):
        if self.player_worker > 0 and hexagon.color != self.player_color:
            self.player_worker -= 1
            hexagon.color = (125, 125, 125)
            self.hexagon_map[line][column] = type

    def update(self):
        # Main
        self.click = self.main.click
        self.mouse = self.main.mouse
        self.event = self.main.event

        # Interface
        self.interfaces.item_dict["crystals"]["text"] = "%i Crystals" % self.player.crystals
        self.interfaces.item_dict["gas"]["text"] = "%i Gas" % self.player.gas
        self.interfaces.item_dict["supply"]["text"] = "%i/%i Supply" % (self.player.supply, self.player.max_supply)


        # Hexagons
        for hexagon in self.hexagons:
            hexagon.update()

        if self.click[1]:
            if len(self.colliding_hexagons) == 1:
                hexagon = self.colliding_hexagons[0]
                line, column = self.convert_index(self.hexagons.index(hexagon))
                self.hexagon_update(hexagon, line, column, 0, 0)

        self.buttons.update()
        self.interfaces.update()

    def draw(self):
        for hexagon in self.hexagons:
            hexagon.render(self.gameDisplay)

        self.colliding_hexagons = [hexagon for hexagon in self.hexagons if hexagon.collide_with_point(self.mouse)]
        for hexagon in self.colliding_hexagons:
            for neighbour in hexagon.compute_neighbours(self.hexagons):
                # neighbour.render_highlight(self.gameDisplay, border_color=(100, 100, 100))
                pass
            hexagon.render_highlight(self.gameDisplay, border_color=(0, 0, 0))

        self.buttons.draw()
        self.interfaces.draw()

class Player:
    def __init__(self, team, player_dict):
        """Team"""
        self.team = team

        """Resources"""
        self.crystals = player_dict["crystals"]
        self.gas = player_dict["gas"]
        self.supply = 0
        self.max_supply = 0

        """Units"""
        self.units = []
        self.citizen = player_dict["citizen"]
        self.miner = player_dict["miner"]
        self.harvester = player_dict["harvester"]
        self.builder = player_dict["builder"]
        self.soldier = player_dict["soldier"]

        """Buildings"""
        self.buildings = []

    def new_building(self, item):
        pass

    def end_turn(self):
        self.crystals += 25*self.miner
        self.gas += 10*self.harvester

        for unit in self.units:
            unit.update()

        for building in self.buildings:
            building.update()

    def production(self, item):
        pass

MAIN_DICT = {
    # Init (Settings) ----------------- #
    "game": {
        "project_title": "Hexagon", "screen_size": (1280, 720), "FPS": 60,
        "default_music_volume": 5, "default_sound_volume": 75,
        "key_repeat": (100, 30)},


    # Game (Settings) ----------------- #
    "settings": {
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
}











button_dict = {
    "settings": {
        "default": {
            "box_size": [280, 50], "box_active_color": DARK_SKY_BLUE, "box_inactive_color": LIGHT_SKY_BLUE, "box_align": "nw",
            "box_border_size": [5, 5], "box_border_color": BLACK,
            "text_font": "LiberationSerif", "text_color": WHITE, "text_align": "center",
            "sound_action": None, "sound_active": None, "sound_inactive": None},
    },

    "title": {},
    "main": {
        "new_game": {"settings": "default", "position": [10, 50], "text": "New Game", "action": "self.game.new_game"},
        "end_turn": {"settings": "default", "position": [10, 120], "text": "End Turn", "action": "self.game.end_turn"},
    }
}

interface_dict = {
    "settings": {
        "default": {
            "box_size": [180, 50], "box_color": DARKGREY, "box_align": "center",
            "box_border_size": [6, 6], "box_border_color": LIGHTSKYGREY,
            "text_font": "LiberationSerif_30", "text_color": WHITE, "text_align": "center"},
        "main": {
            "box_size": [180, 50], "box_color": DARKGREY, "box_align": "nw",
            "box_border_size": [6, 6], "box_border_color": LIGHTSKYGREY,
            "text_font": "LiberationSerif_30", "text_color": WHITE, "text_align": "center"},
    },

    "title": {},
    "main": {
        "crystals": {"settings": "main", "position": [710, 10], "text": None},
        "gas": {"settings": "main", "position": [900, 10], "text": None},
        "supply": {"settings": "main", "position": [1090, 10], "text": None}},
}
