import pygame
import random
from os import path
from Dict import *
from Main import *
from ScaledGame import *

class Game:
    def __init__(self):
        self.game = self
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.mixer.init()
        pygame.init()
        random.seed()
        self.load()
        self.new()
        self.main = Main(self)
        self.update_menu()

    def load(self):
        """Initialization"""
        # Dictionaries
        self.game_dict = game_dict
        self.settings_dict = self.game_dict["settings"]
        self.menu_dict = self.game_dict["menu"]
        self.background_dict = self.game_dict["background"]
        self.font_dict = self.game_dict["font"]
        self.graphic_dict = self.game_dict["graphic"]
        self.music_dict = self.game_dict["music"]
        self.sound_dict = self.game_dict["sound"]

        # Folders
        self.game_folder = path.dirname(__file__)
        self.data_folder = path.join(self.game_folder, "data")
        self.font_folder = path.join(self.data_folder, "font")
        self.graphic_folder = path.join(self.data_folder, "graphic")
        self.music_folder = path.join(self.data_folder, "music")
        self.sound_folder = path.join(self.data_folder, "sound")

        """Settings"""
        # Game
        self.project_title = self.settings_dict["project_title"]
        self.screen_size = self.screen_width, self.screen_height = self.settings_dict["screen_size"]
        self.FPS = self.settings_dict["FPS"]
        self.gameDisplay = ScaledGame(self.project_title, self.screen_size, self.FPS)

        # Volume
        self.default_music_volume = self.music_volume = self.settings_dict["default_music_volume"]
        self.default_sound_volume = self.sound_volume = self.settings_dict["default_sound_volume"]
        pygame.mixer.music.set_volume(self.music_volume/100)

        # Key
        self.key_delay, self.key_interval = self.settings_dict["key_repeat"]
        pygame.key.set_repeat(self.key_delay, self.key_interval)

        """Font"""
        for font in self.font_dict:
            font_ttf, font_size = self.font_dict[font]["ttf"], self.font_dict[font]["size"]
            if font_ttf is not None:
                font_ttf = path.join(self.font_folder, font_ttf)
            self.font_dict[font] = pygame.font.Font(font_ttf, font_size)
        self.font = self.font_dict["default"]

        """Graphic"""
        for graphic in self.graphic_dict:
            graphic_path = path.join(self.graphic_folder, self.graphic_dict[graphic])
            graphic_image = pygame.image.load(graphic_path)
            graphic_surface = pygame.Surface.convert_alpha(graphic_image)
            self.graphic_dict[graphic] = graphic_surface

        """Music"""
        for music in self.music_dict:
            if self.music_dict[music] is not None:
                self.music_dict[music] = path.join(self.music_folder, self.music_dict[music])

        """Sound"""
        for sound in self.sound_dict:
            self.sound_dict[sound] = pygame.mixer.Sound(path.join(self.sound_folder, self.sound_dict[sound]))
            self.sound_dict[sound].set_volume(self.sound_volume / 100)

    def new(self):
        """Game"""
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.playing = True
        self.menu = "title"

        """Settings"""
        self.background_image = None
        self.background_color = None
        self.music = None

        """Pause"""
        self.paused = False
        self.paused_check = False
        self.pause_button_update = None
        self.pause_text_surface, self.pause_text_rect = self.compute_text("Game Paused", self.font, RED, (self.screen_width // 2, self.screen_height // 2), align="center")
        self.dim_screen = pygame.Surface(self.gameDisplay.get_size()).convert_alpha()
        self.dim_screen.fill((100, 100, 100, 120))

        """Debug"""
        self.debug_color = CYAN
        self.debug_mode = True

    # Game Loop ----------------------- #
    def run(self):
        while self.playing:
            self.dt = self.main.dt = self.gameDisplay.clock.tick(self.FPS) / 1000
            self.events()
            if not self.paused:
                self.update()
            elif self.pause_button_update is not None:
                # Continue to update pause button
                self.pause_button_update()
            self.draw()
        self.quit_game()

    def quit_game(self):
        pygame.quit()
        quit()

    def events(self):
        """Click: None, Left, Middle, Right, Scroll Up, Scroll Down"""
        self.click = self.main.click = [None, False, False, False, False, False]

        """Events"""
        self.event = self.main.event = pygame.event.get()
        for event in self.event:
            # Rescale mouse position to screen size
            self.mouse = self.main.mouse = pygame.mouse.get_pos()
            if self.gameDisplay.factor_w != 1 or self.gameDisplay.factor_h != 1:
                mouse_w = int((self.mouse[0] - self.gameDisplay.game_gap[0]) / self.gameDisplay.factor_w)
                mouse_h = int(self.mouse[1] / self.gameDisplay.factor_h)
                self.mouse = self.main.mouse = (mouse_w, mouse_h)

            # Mouse click
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.click[event.button] = True

            # Keyboard
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit_game()
                if event.key == pygame.K_p:
                    self.paused_check = self.pause_game(self.paused_check)
                if event.key == pygame.K_h:
                    self.debug_mode = not self.debug_mode
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_p:
                    self.paused_check = False

            # Quit Game (X Button)
            if event.type == pygame.QUIT:
                self.quit_game()

    def pause_game(self, paused_check=False):
        """Pause the game: self.paused_check = self.pause_game(self.paused_check) to avoid repetition when holding pause shortcut"""
        if not paused_check:
            self.paused = not self.paused
            if self.paused:
                pygame.mixer.music.pause()
            else:
                pygame.mixer.music.unpause()
        return True

    def update(self):
        self.main.update()
        self.all_sprites.update()

    def draw(self):
        # Background ------------------ #
        if self.background_color is not None:
            self.gameDisplay.fill(self.background_color)
        if self.background_image is not None:
            self.gameDisplay.blit(self.background_image, (0, 0))

        # Main ------------------------ #
        self.main.draw()

        # Sprite --------------------- #
        for sprite in self.all_sprites:
            sprite.draw()
            if self.debug_mode:
                pygame.draw.rect(self.gameDisplay, CYAN, sprite.rect, 1)

        # Pause ----------------------- #
        if self.paused:
            self.gameDisplay.blit(self.dim_screen, (0, 0))
            self.gameDisplay.blit(self.pause_text_surface, self.pause_text_rect)

        # Update ---------------------- #
        self.gameDisplay.update(self.event)

    def clear_sprites(self):
        """Remove all sprites"""
        for sprite in self.all_sprites:
            sprite.kill()

    def update_menu(self, menu=None):
        """Update the menu: Default menu is title"""
        self.menu = menu if menu is not None else self.menu
        self.clear_sprites()
        dict = self.menu_dict[self.menu]
        self.update_background(dict["background"])
        self.update_music(dict["music"])
        # self.main.buttons = Button(self.main, button_dict, self.menu)
        # self.main.interfaces = Interface(self.main, interface_dict, self.menu)

    def update_background(self, background):
        """Update the background"""
        if background in self.background_dict:
            background = self.background_dict[background]
        if background["color"] is not None:
            self.background_color = background["color"]
        if background["image"] is not None:
            self.background_image = load_image(self.graphics_folder, background["image"])

    def update_music(self, music):
        """Update the music"""
        if music in self.music_dict:
            music = self.music_dict[music]
        if self.music != music and music is not None:
            self.music = music
            pygame.mixer.music.load(self.music)
            pygame.mixer.music.play(-1)

    def update_music_volume(self, dv=0):
        """Update the music volume by dv (from 0 to 100)"""
        self.music_volume = min(max(0, self.music_volume + dv), 100)
        pygame.mixer.music.set_volume(self.music_volume/100)

    def play_sound(self, sound, check=False):
        """Play a sound and prevents repetition by returning True"""
        if sound is not None and not check:
            pygame.mixer.Sound.play(sound)
            return True

    def align_surface_rect(self, surface_rect, pos, align):
        """Return the surface_rect aligned to the position"""
        rect = surface_rect.get_rect()
        pos = (int(pos[0]), int(pos[1]))
        if align == "nw":
            rect.topleft = pos
        if align == "ne":
            rect.topright = pos
        if align == "sw":
            rect.bottomleft = pos
        if align == "se":
            rect.bottomright = pos
        if align == "n":
            rect.midtop = pos
        if align == "s":
            rect.midbottom = pos
        if align == "e":
            rect.midright = pos
        if align == "w":
            rect.midleft = pos
        if align == "center":
            rect.center = pos
        return rect

    def compute_surface(self, rect, color, border_size=[0, 0], border_color=None, align="center", return_rect=True):
        """Return a surface and its rectangle filled with color and border_color"""
        # Fill a surface with border_color
        surface = pygame.Surface((rect[2], rect[3]))
        if border_color is not None:
            surface.fill(border_color)

        # Fill the inside with color
        surface_in_rect = [border_size[0], border_size[1], rect[2] - 2*border_size[0], rect[3] - 2*border_size[1]]
        pygame.draw.rect(surface, color, surface_in_rect)

        if return_rect:
            surface_out_rect = self.align_surface_rect(surface, (rect[0], rect[1]), align)
            return surface, surface_out_rect
        return surface

    def compute_text(self, text, font, color, pos, align="nw"):
        """Return a surface and its rectangle with text drawn on it"""
        if text is not None and font is not None:
            text = str(text)
            text_surface = font.render(text, True, color)
            text_surface_rect = self.align_surface_rect(text_surface, pos, align)
            return text_surface, text_surface_rect
        return None, None

    def compute_text_pos(self, rect):
        """Return text position centered in the rectangle"""
        return [rect[0] + rect[2] // 2, rect[1] + rect[3] // 2]

m = Game()
while True:
    m.run()
