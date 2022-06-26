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
            "box_size": [280, 50], "box_active_color": DARK_SKY_BLUE, "box_inactive_color": LIGHT_SKY_BLUE, "box_align": "nw",
            "box_border_size": [5, 5], "box_border_color": BLACK,
            "text_font": "LiberationSerif", "text_color": WHITE, "text_align": "center",
            "sound_action": None, "sound_active": None, "sound_inactive": None},
    },

    "title": {},
    "main": {
        "new_game": {"settings": "default", "position": [10, 50], "text": "New Game", "argument": None, "action": "self.main.new_game"},
        "end_turn": {"settings": "default", "position": [10, 120], "text": "End Turn", "argument": None, "action": "self.main.end_turn"},
        "pause": {"settings": "default", "position": [10, 190], "text": "Pause", "argument": None, "action": "self.game.pause_game"},
        "volume_up": {"settings": "default", "position": [10, 260], "text": "Volume +", "argument": +5, "action": "self.game.update_music_volume"},
        "volume_down": {"settings": "default", "position": [10, 330], "text": "Volume -", "argument": -5, "action": "self.game.update_music_volume"},
        "fullscreen": {"settings": "default", "position": [10, 400], "text": "Fullscreen", "argument": None, "action": "self.game.gameDisplay.fullscreen"},
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
