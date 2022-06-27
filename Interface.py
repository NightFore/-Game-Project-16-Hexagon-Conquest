import pygame
from Settings import *

class Interface:
    def __init__(self, main, dict, data, item=None):
        """Initialization: game, main, dict, data, items"""
        self.main = main
        self.game = main.game
        self.dict = dict
        self.data = self.dict[data]
        self.items = [self.data[item]] if item is not None else [item for item in self.data]

        """item_dict:
        rect, size_border, color, color_border, align
        text, text_check, text_pos, text_font, text_color, text_align
        surface, surface_rect, text_surface, text_surface_rect
        """
        self.item_dict = {}
        for item in self.items:
            # Initialization
            dict = {}
            data = self.data[item]
            settings = self.dict["settings"][data["settings"]]

            # Surface
            if "image" in data:
                dict = self.load_image(dict, data, settings)
            else:
                dict = self.load_box(dict, data, settings)
            dict["surface_rect"] = self.game.align_surface_rect(dict["surface"], (data["position"][0], data["position"][1]), dict["align"])

            # Text
            if "text" in data:
                dict = self.load_text(dict, data, settings)

            # Output
            self.item_dict[item] = dict

    def load_box(self, dict, data, settings):
        dict["rect"] = [data["position"][0], data["position"][1], settings["size"][0], settings["size"][1]]
        dict["size_border"] = settings["size_border"]
        dict["color"] = settings["color"]
        dict["color_border"] = settings["color_border"]
        dict["align"] = settings["align"]
        dict["surface"] = self.game.compute_surface(dict["rect"], dict["color"], dict["size_border"], dict["color_border"], dict["align"])
        return dict

    def load_image(self, dict, data, settings):
        dict["align"] = settings["align"]
        dict["surface"] = self.game.graphic_dict[data["image"]]
        return dict

    def load_text(self, dict, data, settings):
        dict["text"] = data["text"]
        dict["text_check"] = dict["text"]
        dict["text_pos"] = self.game.compute_text_pos(dict["rect"])
        dict["text_font"] = self.game.font_dict[settings["text_font"]]
        dict["text_color"] = settings["text_color"]
        dict["text_align"] = settings["text_align"]
        dict["text_surface"], dict["text_surface_rect"] = self.game.compute_text(dict["text"], dict["text_font"], dict["text_color"], dict["text_pos"], dict["text_align"])
        return dict

    def update(self):
        pass

    def draw(self):
        for item in self.item_dict:
            dict = self.item_dict[item]

            # Surface
            self.game.gameDisplay.blit(dict["surface"], dict["surface_rect"])

            # Text
            if "text" in dict:
                if dict["text"] != dict["text_check"]:
                    dict["text_check"] = dict["text"]
                    dict["text_surface"], dict["text_surface_rect"] = self.game.compute_text(dict["text"], dict["text_font"], dict["text_color"], dict["text_pos"], dict["text_align"])

                if dict["text"] is not None:
                    self.game.gameDisplay.blit(dict["text_surface"], dict["text_surface_rect"])
