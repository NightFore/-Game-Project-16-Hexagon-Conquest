import pygame
from Settings import *

button_dict_template = {
    "settings": {
        "default": {
            "box_size": [280, 50], "box_active_color": DARK_SKY_BLUE, "box_inactive_color": LIGHT_SKY_BLUE, "box_align": "nw",
            "box_border_size": [5, 5], "box_border_color": BLACK,
            "text_font": "LiberationSerif", "text_color": WHITE, "text_align": "center",
            "sound_action": None, "sound_active": None, "sound_inactive": None},
    },

    "title": {
        "new_game": {"settings": "default", "position": [10, 50], "text": "New Game", "image": None, "action": "self.game.new_game"}},
}

class Button:
    def __init__(self, game, dict, data, item=None):
        """Initialization: main, dict, data, items"""
        self.game = game
        self.main = game.main
        self.dict = dict
        self.data = self.dict[data]
        self.items = [self.data[item]] if item is not None else [item for item in self.data]

        """Item dict:
        box_rect, box_active_color, box_inactive_color, box_align, box_border_size, box_border_color
        text, text_pos, text_font, text_color, text_align, text_check
        box_surface, box_surface_rect, text_surface, text_surface_rect, box_surface_active, box_surface_inactive
        sound_action, sound_active, sound_inactive, sound_check
        action
        """
        self.item_dict = {}
        for item in self.items:
            # Initialization
            dict = {}
            data = self.data[item]
            settings = self.dict["settings"][data["settings"]]

            # Box
            box_pos, box_size = data["position"], settings["box_size"]
            dict["box_rect"] = [box_pos[0], box_pos[1], box_size[0], box_size[1]]
            dict["box_active_color"] = settings["box_active_color"]
            dict["box_inactive_color"] = settings["box_inactive_color"]
            dict["box_align"] = settings["box_align"]
            dict["box_border_size"] = settings["box_border_size"]
            dict["box_border_color"] = settings["box_border_color"]

            # Text
            dict["text"] = data["text"]
            dict["text_pos"] = self.main.compute_text_pos(dict["box_rect"])
            dict["text_font"] = self.main.font_dict[settings["text_font"]]
            dict["text_color"] = settings["text_color"]
            dict["text_align"] = settings["text_align"]
            dict["text_check"] = dict["text"]

            # Surface
            dict["box_surface_active"], dict["box_surface_rect"] = self.main.compute_surface(dict["box_rect"], dict["box_active_color"], dict["box_border_size"], dict["box_border_color"], dict["box_align"])
            dict["box_surface_inactive"] = self.main.compute_surface(dict["box_rect"], dict["box_inactive_color"], dict["box_border_size"], dict["box_border_color"], dict["box_align"], False)
            dict["box_surface"] = dict["box_surface_inactive"]
            dict["text_surface"], dict["text_surface_rect"] = self.main.compute_text(dict["text"], dict["text_font"], dict["text_color"], dict["text_pos"], dict["text_align"])

            # Sound
            dict["sound_action"] = settings["sound_action"]
            dict["sound_active"] = settings["sound_active"]
            dict["sound_inactive"] = settings["sound_inactive"]
            dict["sound_check"] = False

            # Action
            dict["action"] = eval(data["action"])

            # Output
            self.item_dict[item] = dict

    def draw(self):
        for item in self.item_dict:
            dict = self.item_dict[item]

            # Box
            self.main.gameDisplay.blit(dict["box_surface"], dict["box_surface_rect"])

            # Text Check
            if dict["text"] != dict["text_check"]:
                dict["text_surface"], dict["text_surface_rect"] = self.main.compute_text(dict["text"], dict["text_font"], dict["text_color"], dict["text_pos"], dict["text_align"])
                dict["text_check"] = dict["text"]

            # Text
            if dict["text_surface"] is not None and dict["text_surface_rect"] is not None:
                self.main.gameDisplay.blit(dict["text_surface"], dict["text_surface_rect"])

    def update(self):
        for item in self.item_dict:
            dict = self.item_dict[item]
            if dict["box_surface_rect"].collidepoint(self.main.mouse):
                # Active
                dict["box_surface"] = dict["box_surface_active"]
                dict["sound_check"] = self.main.play_sound(dict["sound_active"], dict["sound_check"])

                # Action
                if self.main.click[1]:
                    self.main.play_sound(dict["sound_action"])
                    if dict["action"] is not None:
                        dict["action"]()
            else:
                # Inactive
                dict["box_surface"] = dict["box_surface_inactive"]
                dict["sound_check"] = self.main.play_sound(dict["sound_inactive"], dict["sound_check"])
