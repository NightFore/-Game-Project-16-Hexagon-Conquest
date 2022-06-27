import pygame
from Button import *
from Dict import *
from Interface import *
from Hexagon import *

class Main:
    def __init__(self, game):
        # Game Initialization
        self.game = game
        self.main = self
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
        self.interfaces = Interface(self, interface_dict, "main")
        self.buttons = Button(self, button_dict, "main")
        self.main_dict = main_dict

        self.colliding_hexagons = []


        # WIP
        self.player_worker = 5
        self.player_color = (125, 125, 125)
        self.player = Player(0, self.main_dict)

        self.buttons_test = Button(self, button_dict, "test")
        self.interface_test = Interface(self, interface_dict, "test")
        self.test_active = False

    def new_game(self):
        # Initialization
        self.game.update_menu()
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

    def test(self):
        self.test_active = not self.test_active

    def update(self):
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

        self.interfaces.update()
        self.buttons.update()

        if self.test_active:
            self.interface_test.update()
            self.buttons_test.update()

    def draw(self):
        for hexagon in self.hexagons:
            hexagon.render(self.game.gameDisplay)

        self.colliding_hexagons = [hexagon for hexagon in self.hexagons if hexagon.collide_with_point(self.mouse)]
        for hexagon in self.colliding_hexagons:
            for neighbour in hexagon.compute_neighbours(self.hexagons):
                # neighbour.render_highlight(self.game.gameDisplay, border_color=(100, 100, 100))
                pass
            hexagon.render_highlight(self.game.gameDisplay, border_color=(0, 0, 0))

        self.interfaces.draw()
        self.buttons.draw()

        if self.test_active:
            self.interface_test.draw()
            self.buttons_test.draw()

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

main_dict = {
    "crystals": 500, "gas": 0, "supply": 0,
    "citizen": 5, "miner": 2, "harvester": 0, "builder": 1, "soldier": 1
}
