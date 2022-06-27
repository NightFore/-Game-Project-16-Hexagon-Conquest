import pygame
from Settings import *


game_dict = {
    # Settings (Game / Volume / Sound) ----------------- #
    "settings": {
        "project_title": "Hexagon Conquest", "screen_size": (1280, 720), "FPS": 60,
        "default_music_volume": 5, "default_sound_volume": 75,
        "key_repeat": (100, 30)
    },

    # Menu Dict ----------------------- #
    "menu": {
        "title": {
            "background": "default",
            "music": "default"
        }
    },

    # Background Dict ----------------------- #
    "background": {
        "default": {
            "color": DARK_SKY_BLUE,
            "image": None,
        },
    },

    # Font Dict ----------------------- #
    "font": {
        "default": {"ttf": None, "size": 100},
        "LiberationSerif": {"ttf": "LiberationSerif-Regular.ttf", "size": 40},
        "LiberationSerif_30": {"ttf": "LiberationSerif-Regular.ttf", "size": 30}
    },

    # Graphic Dict ----------------------- #
    "graphic": {
        "button_exit_active": "button_exit_active.png", "button_exit_inactive": "button_exit_inactive.png"
    },

    # Music Dict ---------------------- #
    "music": {
        "default": None,
    },

    # Sound Dict ---------------------- #
    "sound": {
    },
}

button_dict = {
    "settings": {
        "default": {
            "size": [280, 50], "size_border": [5, 5], "align": "nw",
            "color_active": DARK_SKY_BLUE, "color_inactive": LIGHT_SKY_BLUE, "color_border": BLACK,
            "text_font": "LiberationSerif", "text_color": WHITE, "text_align": "center",
            "sound_action": None, "sound_active": None, "sound_inactive": None},
        "image": {
            "align": "center",
            "sound_action": None, "sound_active": None, "sound_inactive": None,
        }
    },

    "title": {},
    "main": {
        "new_game": {"settings": "default", "position": [10, 50], "text": "New Game", "argument": None, "action": "self.main.new_game"},
        "end_turn": {"settings": "default", "position": [10, 120], "text": "End Turn", "argument": None, "action": "self.main.end_turn"},
        "pause": {"settings": "default", "position": [10, 190], "text": "Pause", "argument": None, "action": "self.game.pause_game"},
        "volume_up": {"settings": "default", "position": [10, 260], "text": "Volume +", "argument": +5, "action": "self.game.update_music_volume"},
        "volume_down": {"settings": "default", "position": [10, 330], "text": "Volume -", "argument": -5, "action": "self.game.update_music_volume"},
        "fullscreen": {"settings": "default", "position": [10, 400], "text": "Fullscreen", "argument": None, "action": "self.game.gameDisplay.fullscreen"},
        "test": {"settings": "default", "position": [10, 470], "text": "Test", "argument": None, "action": "self.main.test"},
    },
    "test": {
        "test_1": {"settings": "default", "position": [500, 615], "text": "Test", "argument": None, "action": "self.main.test"},
        "test_2": {"settings": "image", "position": [400, 640], "image": ["button_exit_active", "button_exit_inactive"], "argument": None, "action": "self.game.quit_game"},
    },
}

interface_dict = {
    "settings": {
        "default": {
            "size": [180, 50], "color": DARKGREY, "align": "center",
            "size_border": [6, 6], "color_border": LIGHTSKYGREY,
            "text_font": "LiberationSerif_30", "text_color": WHITE, "text_align": "center"},
        "main": {
            "size": [180, 50], "color": DARKGREY, "align": "nw",
            "size_border": [6, 6], "color_border": LIGHTSKYGREY,
            "text_font": "LiberationSerif_30", "text_color": WHITE, "text_align": "center"},
        "big_test": {
            "size": [590, 80], "color": DARKGREY, "align": "center",
            "size_border": [6, 6], "color_border": LIGHTSKYGREY,
            "text_font": "LiberationSerif_30", "text_color": WHITE, "text_align": "center"},
    },

    "title": {},
    "main": {
        "test": {"settings": "big_test", "position": [975, 50], "text": None},
        "crystals": {"settings": "main", "position": [695, 25], "text": None},
        "gas": {"settings": "main", "position": [885, 25], "text": None},
        "supply": {"settings": "main", "position": [1075, 25], "text": None},
    },
    "test": {
        "test_box": {"settings": "big_test", "position": [640, 640], "text": None}
    },
}
