import pygame
import random
from os import path
from Main import *
from ScaledGame import *

class Main:
    def __init__(self):
        self.main = self
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.mixer.init()
        pygame.init()
        random.seed()
        self.load()
        self.new()
        self.game = Game(self)
        self.init_game()
        self.update_menu()

    def load(self):
        # Dictionaries
        self.main_dict = MAIN_DICT
        self.init_dict = self.main_dict["game"]
        self.settings_dict = self.main_dict["settings"]
        self.background_dict = self.main_dict["background"]
        self.music_dict = self.main_dict["music"]
        self.sound_dict = self.main_dict["sound"]
        self.font_dict = self.main_dict["font"]
        self.menu_dict = self.main_dict["menu"]

        # Directories
        self.game_folder = path.dirname(__file__)
        self.data_folder = path.join(self.game_folder, "data")
        self.font_folder = path.join(self.data_folder, "font")
        self.graphic_folder = path.join(self.data_folder, "graphic")
        self.item_folder = path.join(self.data_folder, "item")
        self.music_folder = path.join(self.data_folder, "music")
        self.se_folder = path.join(self.data_folder, "sound")

        # Sound Effects
        self.sound_effects = {}
        for sound in self.sound_dict:
            self.sound_effects[sound] = pygame.mixer.Sound(path.join(self.se_folder, self.sound_dict[sound]))
            self.sound_effects[sound].set_volume(self.sound_volume / 100)

        # Fonts
        for font in self.font_dict:
            font_ttf = self.font_dict[font]["ttf"]
            font_size = self.font_dict[font]["size"]
            if font_ttf is not None:
                self.font_dict[font] = pygame.font.Font(path.join(self.font_folder, font_ttf), font_size)
            else:
                self.font_dict[font] = pygame.font.Font(font_ttf, font_size)
        self.font = self.font_dict["default"]

        # Game Settings
        self.project_title = self.init_dict["project_title"]
        self.screen_size = self.screen_width, self.screen_height = self.init_dict["screen_size"]
        self.FPS = self.init_dict["FPS"]
        self.gameDisplay = ScaledGame(self.project_title, self.screen_size, self.FPS)

        # Volume Settings
        self.default_music_volume = self.init_dict["default_music_volume"]
        self.music_volume = self.default_music_volume
        self.default_sound_volume = self.init_dict["default_sound_volume"]
        self.sound_volume = self.default_sound_volume
        pygame.mixer.music.set_volume(self.music_volume/100)

        # Key Settings
        self.key_delay, self.key_interval = self.init_dict["key_repeat"]
        pygame.key.set_repeat(self.key_delay, self.key_interval)

    def new(self):
        # Game Initialization
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.playing = True
        self.menu = "main_menu"

        # Settings
        self.background_image = None
        self.background_color = None
        self.music = None

        # Pause
        self.paused = False
        self.pause_check = False
        self.dim_screen = pygame.Surface(self.gameDisplay.get_size()).convert_alpha()
        self.dim_screen.fill((100, 100, 100, 120))

        # Debug
        self.debug_color = CYAN
        self.debug_mode = True

    def init_game(self):
        # Surface
        self.game.gameDisplay = self.gameDisplay

        # Dictionaries
        self.game.main_dict = self.main_dict
        self.game.settings_dict = self.main_dict["settings"]

        # Sprites
        self.game.players = pygame.sprite.Group()

    # Game Loop ----------------------- #
    def run(self):
        while self.playing:
            self.dt = self.gameDisplay.clock.tick(self.FPS) / 1000
            self.game.dt = self.dt
            self.events()
            if not self.paused:
                self.update()
            self.draw()
        self.quit_game()

    def quit_game(self):
        pygame.quit()
        quit()

    def pause_game(self, pause=None, pause_check=False):
        # Keyboard Pause
        if pause_check:
            # Pause
            if pause:
                self.paused = True
                pygame.mixer.music.pause()

            # Unpause
            elif self.pause_check:
                self.pause_check = False
                self.paused = False
                pygame.mixer.music.unpause()
            else:
                self.pause_check = True

        # Click Pause
        elif not pause_check:
            # Pause
            pause = not self.paused if pause is None else pause
            if pause:
                self.pause_check = True
                self.paused = True
                pygame.mixer.music.pause()

            # Unpause
            else:
                self.pause_check = False
                self.paused = False
                pygame.mixer.music.unpause()


    def events(self):
        # Click: None, Left, Middle, Right, Scroll Up, Scroll Down
        self.click = [None, False, False, False, False, False]
        self.mouse = pygame.mouse.get_pos()
        self.event = pygame.event.get()

        for event in self.event:
            # Rescales mouse position to screen size
            if self.gameDisplay.factor_w != 1 or self.gameDisplay.factor_h != 1:
                mouse_w = int((self.mouse[0] - self.gameDisplay.game_gap[0]) / self.gameDisplay.factor_w)
                mouse_h = int(self.mouse[1] / self.gameDisplay.factor_h)
                self.mouse = (mouse_w, mouse_h)

            # Mouse Click
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.click[event.button] = True

            # Keyboard
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Quit Game (Escape)
                    self.quit_game()
                if event.key == pygame.K_p:
                    # Pause Game
                    self.pause_game(True, pause_check=True)
                if event.key == pygame.K_h:
                    # Debug Mode
                    self.debug_mode = not self.debug_mode
            if event.type == pygame.KEYUP:
                    # Unpause Game
                if event.key == pygame.K_p:
                    self.pause_game(False, pause_check=True)

            # Quit Game (Close Button)
            if event.type == pygame.QUIT:
                self.quit_game()

    def update(self):
        self.game.update()
        self.all_sprites.update()

    def draw(self):
        # Background ------------------ #
        if self.background_image is not None:
            self.gameDisplay.blit(self.background_image, (0, 0))
        if self.background_color is not None:
            self.gameDisplay.fill(self.background_color)

        # Game ------------------------ #
        self.game.draw()

        # Sprite --------------------- #
        for sprite in self.all_sprites:
            sprite.draw()
            if self.debug_mode:
                pygame.draw.rect(self.gameDisplay, CYAN, sprite.rect, 1)

        # Pause ----------------------- #
        if self.paused:
            self.gameDisplay.blit(self.dim_screen, (0, 0))
            self.draw_text("Game Paused", self.font, RED, (self.screen_width // 2, self.screen_height // 2), align="center")

        # Update ---------------------- #
        self.gameDisplay.update(self.event)

    def update_menu(self, menu=None):
        # Default menu is main_menu
        if menu is None:
            self.update_menu(self.menu)
        else:
            self.menu = menu
            self.clear_sprites()
            self.update_background(self.menu_dict[self.menu]["background"])
            self.update_music(self.menu_dict[self.menu]["music"])

    def update_background(self, background):
        if isinstance(background, str):
            background = self.background_dict[background]
        if background is not None:
            if background["color"] is not None:
                self.background_color = background["color"]
            if background["image"] is not None:
                self.background_image = load_image(self.graphics_folder, background["image"])

    def update_music(self, music):
        if isinstance(music, str):
            music = self.music_dict[music]
        if music is not None:
            music = path.join(self.music_folder, music)
            if self.music != music:
                self.music = music
                pygame.mixer.music.load(self.music)
                pygame.mixer.music.play(-1)

    def update_volume(self, dv=0):
        self.music_volume = min(max(0, self.music_volume + dv), 100)
        pygame.mixer.music.set_volume(self.music_volume/100)

    def clear_sprites(self):
        for sprite in self.all_sprites:
            sprite.kill()

    def align_rect(self, surface_rect, pos, align):
        """Returns the rect aligned to the position"""
        if isinstance(surface_rect, pygame.Surface):
            rect = surface_rect.get_rect()
        else:
            rect = pygame.Rect(surface_rect)
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

    def update_sprite_rect(self, sprite, x=None, y=None):
        """Update sprite's rect position"""
        if x is None:
            x = sprite.pos[0]
        if y is None:
            y = sprite.pos[1]
        sprite.pos = [x, y]
        sprite.rect = self.align_rect(sprite.surface, (int(sprite.pos[0]), int(sprite.pos[1])), sprite.align)

    def compute_text(self, text, font, color, pos, align="nw"):
        """Returns a surface and its rectangle with text drawn on it"""
        if text is not None and font is not None:
            text = str(text)
            text_surface = font.render(text, True, color)
            text_surface_rect = self.align_rect(text_surface, pos, align)
            return text_surface, text_surface_rect
        else:
            return None, None

    def compute_text_pos(self, rect):
        """Returns text position centered in the rectangle"""
        return [rect[0] + rect[2] // 2, rect[1] + rect[3] // 2]

    def compute_surface(self, rect, color, border_size=[0, 0], border_color=None, align="center", return_rect=True):
        """Returns a surface and its rectangle filled with color and border_color"""
        # Fills a surface with border_color
        surface = pygame.Surface((rect[2], rect[3]))
        if border_color is not None:
            surface.fill(border_color)

        # Fills the inside with color
        surface_in_rect = [border_size[0], border_size[1], rect[2] - 2*border_size[0], rect[3] - 2*border_size[1]]
        pygame.draw.rect(surface, color, surface_in_rect)

        if return_rect:
            surface_out_rect = self.align_rect(surface, (rect[0], rect[1]), align)
            return surface, surface_out_rect
        else:
            return surface

    def play_sound(self, sound, check=False):
        """Plays a sound and prevents repetition by returning True"""
        if sound is not None and not check:
            pygame.mixer.Sound.play(sound)
            return True

m = Main()
while True:
    m.run()
