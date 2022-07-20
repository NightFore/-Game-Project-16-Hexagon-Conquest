import pygame
from Function import *
from Settings import *

class Button:
    def __init__(self, game, dict, data, item=None):
        init_class(self, game, dict, data, item)

        """Pause Button"""
        for item in self.items:
            if item == "pause":
                self.game.pause_button_update = self.pause_button_update

    def pause_button_update(self):
        self.update_button(self.item_dict["pause"])

    def update_button(self, dict):
        # Collision
        if dict["surface_rect"].collidepoint(self.game.mouse):
            # Action
            if self.game.click[1]:
                self.game.play_sound(dict["sound_action"])
                if dict["action"] is not None:
                    if dict["argument"] is not None:
                        dict["action"](dict["argument"])
                    else:
                        dict["action"]()
            # Active
            dict["surface"] = dict["surface_active"]
            dict["sound_check"] = self.game.play_sound(dict["sound_active"], dict["sound_check"])
        else:
            # Inactive
            dict["surface"] = dict["surface_inactive"]
            dict["sound_check"] = self.game.play_sound(dict["sound_inactive"], dict["sound_check"])

    def update(self):
        for item in self.item_dict:
            dict = self.item_dict[item]
            self.update_button(dict)

    def draw(self):
        for item in self.item_dict:
            dict = self.item_dict[item]
            draw_surface(self, dict)
            draw_text(self, dict)
