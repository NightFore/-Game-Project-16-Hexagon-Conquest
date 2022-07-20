import pygame

"""
    Class Initialization
"""
def init_class(self, game, dict, data, item):
    """Initialization: game, main, dict, data"""
    self.game = game
    self.main = self.game.main
    self.dict = dict
    self.data = self.dict[data]
    self.settings = self.dict["settings"]

    """Loading: item_dict
    Call each function in init_functions to load the dict for each item
    """
    self.item_dict = {}
    self.items = [self.data[item]] if item is not None else [item for item in self.data]
    for item in self.items:
        dict = {}
        data = self.data[item]
        settings = self.settings[data["settings"]]
        for function in self.settings["init_functions"]:
            dict = function(self, dict, data, settings)
        self.item_dict[item] = dict


def load_interface(self, dict, data, settings):
    """Load the surface and surface_rect"""
    if "image" in data and data["image"] is not None:
        # Image
        dict["surface"] = self.game.graphic_dict[data["image"]]
    else:
        # Box
        rect = [data["position"][0], data["position"][1], settings["size"][0], settings["size"][1]]
        dict["surface"] = self.game.compute_surface(rect, settings["color"], settings["border_size"], settings["border_color"], settings["align"])
    dict["surface_rect"] = self.game.align_surface_rect(dict["surface"], (data["position"][0], data["position"][1]), settings["align"])
    return dict


def load_button(self, dict, data, settings):
    """Load the surface for each state and surface_rect"""
    if "image" in data and data["image"] is not None:
        # Image
        image_active, image_inactive = data["image"]
        dict["surface_active"] = self.game.graphic_dict[image_active]
        dict["surface_inactive"] = self.game.graphic_dict[image_inactive]
    else:
        # Box
        rect = [data["position"][0], data["position"][1], settings["size"][0], settings["size"][1]]
        dict["surface_active"] = self.game.compute_surface(rect, settings["color"][0], settings["border_size"], settings["border_color"], settings["align"])
        dict["surface_inactive"] = self.game.compute_surface(rect, settings["color"][1], settings["border_size"], settings["border_color"], settings["align"])
    dict["surface"] = dict["surface_inactive"]
    dict["surface_rect"] = self.game.align_surface_rect(dict["surface"], (data["position"][0], data["position"][1]), settings["align"])
    return dict


def load_text(self, dict, data, settings):
    """Load all text parameters"""
    if "text" in data:
        dict["text"] = dict["text_check"] = data["text"]
        dict["text_pos"] = self.game.compute_text_pos(dict["surface_rect"])
        dict["text_font"] = self.game.font_dict[settings["text_font"]]
        dict["text_color"] = settings["text_color"]
        dict["text_align"] = settings["text_align"]
        dict["text_surface"], dict["text_surface_rect"] = self.game.compute_text(dict["text"], dict["text_font"], dict["text_color"], dict["text_pos"], dict["text_align"])
    return dict

def load_sound(self, dict, data, settings):
    """Load all sound parameters"""
    dict["sound_action"] = settings["sound_action"]
    dict["sound_active"] = settings["sound_active"]
    dict["sound_inactive"] = settings["sound_inactive"]
    dict["sound_check"] = False
    return dict

def load_action(self, dict, data, settings):
    """Load all action parameters"""
    dict["argument"] = data["argument"] if "argument" in data else None
    dict["action"] = eval(data["action"]) if "action" in data and data["action"] is not None else None
    return dict



"""
    Class Draw
"""
def draw_surface(self, dict):
    self.game.gameDisplay.blit(dict["surface"], dict["surface_rect"])

def draw_text(self, dict):
    if "text" in dict:
        if dict["text"] != dict["text_check"]:
            dict["text_check"] = dict["text"]
            dict["text_surface"], dict["text_surface_rect"] = self.game.compute_text(dict["text"], dict["text_font"], dict["text_color"], dict["text_pos"], dict["text_align"])

        if dict["text"] is not None:
            self.game.gameDisplay.blit(dict["text_surface"], dict["text_surface_rect"])















