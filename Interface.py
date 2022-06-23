import pygame
from Settings import *

interface_dict_template = {
    "settings": {
        "default": {
            "box_size": [180, 50], "box_color": DARKGREY, "box_align": "center",
            "box_border_size": [6, 6], "box_border_color": LIGHTSKYGREY,
            "text_font": "LiberationSerif_30", "text_color": WHITE, "text_align": "center"},
    },

    "title": {
        "title_screen": {"settings": "default", "position": [640, 10], "text": "Title Screen"}},
}

class Interface:
    def __init__(self, main, dict, data, item=None):
        """Initialization: main, dict, data, items"""
        self.main = main
        self.dict = dict
        self.data = self.dict[data]
        self.items = [self.data[item]] if item is not None else [item for item in self.data]

        """Item dict:
        box_rect, box_color, box_align, box_border_size, box_border_color
        text, text_pos, text_font, text_color, text_align, text_check
        box_surface, box_surface_rect, text_surface, text_surface_rect
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
            dict["box_color"] = settings["box_color"]
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
            dict["box_surface"], dict["box_surface_rect"] = self.main.compute_surface(dict["box_rect"], dict["box_color"], dict["box_border_size"], dict["box_border_color"], dict["box_align"])
            dict["text_surface"], dict["text_surface_rect"] = self.main.compute_text(dict["text"], dict["text_font"], dict["text_color"], dict["text_pos"], dict["text_align"])

            # Output
            self.item_dict[item] = dict

    def update(self):
        pass

    def draw(self):
        for item in self.item_dict:
            dict = self.item_dict[item]

            # Box
            self.main.gameDisplay.blit(dict["box_surface"], dict["box_surface_rect"])

            # Text
            if dict["text"] != dict["text_check"]:
                dict["text_surface"], dict["text_surface_rect"] = self.main.compute_text(dict["text"], dict["text_font"], dict["text_color"], dict["text_pos"], dict["text_align"])
                dict["text_check"] = dict["text"]

            if dict["text_surface"] is not None and dict["text_surface_rect"] is not None:
                self.main.gameDisplay.blit(dict["text_surface"], dict["text_surface_rect"])



