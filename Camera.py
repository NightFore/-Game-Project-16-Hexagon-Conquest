import pygame
from Settings import *
vec = pygame.math.Vector2

class Camera:
    def __init__(self, screen_size, player):
        self.screen_width, self.screen_height = screen_size
        self.set_player(player)
        self.method = self.follow
        self.offset = vec(0, 0)
        self.offset_float = vec(0, 0)

    def set_player(self, player):
        self.player = player
        self.offset_const = vec(-self.screen_width + player.rect.width, -self.screen_height + player.rect.height)/2
        self.offset = vec(0, 0)
        self.offset_float = vec(0, 0)

    def follow(self):
        self.offset_float.x += (self.player.rect.x - self.offset_float.x + self.offset_const.x)
        self.offset_float.y += (self.player.rect.y - self.offset_float.y + self.offset_const.y)
        self.offset.x, self.offset.y = int(self.offset_float.x), int(self.offset_float.y)

    def border(self):
        self.offset_float.x += (self.player.rect.x - self.offset_float.x + self.offset_const.x)
        self.offset_float.y += (self.player.rect.y - self.offset_float.y + self.offset_const.y)
        self.offset.x, self.offset.y = int(self.offset_float.x), int(self.offset_float.y)
        self.offset.x = max(self.player.camera_border_rect[0], self.offset.x)
        self.offset.y = max(self.player.camera_border_rect[2], self.offset.y)
        self.offset.x = min(self.offset.x, self.player.camera_border_rect[1])
        self.offset.y = min(self.offset.y, self.player.camera_border_rect[3])

    def auto(self):
        self.offset.x += 2

    def update(self):
        self.method()

class Player_camera(pygame.sprite.Sprite):
    def __init__(self, game, pos=(640, 360), camera_border_rect=(0, 0)):
        self.game = game
        self.pos, self.vel = vec(pos[0], pos[1]), vec(0, 0)
        self.size, self.size_border = [32, 32], [1, 1]
        self.color, self.color_border = BLUE, RED
        self.align = "center"
        self.rect = self.pos[0], self.pos[1], self.size[0], self.size[1]
        self.surface, self.rect = self.game.compute_surface(self.rect, self.color, self.size_border, self.color_border, self.align, True)

        # Debug
        self.camera_border_rect = camera_border_rect
        self.player_speed = 500
        print(self.camera_border_rect)

    def get_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel.x = -self.player_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel.x = +self.player_speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.vel.y = -self.player_speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.vel.y = +self.player_speed
        if self.vel.x != 0 and self.vel.y != 0:
            self.vel *= 0.7071

    def update_position(self):
        self.vel = vec(0, 0)
        self.get_keys()
        self.pos += self.vel * self.dt
        self.rect.center = self.pos

    def update(self):
        self.dt = self.game.dt
        self.update_position()

    def draw(self):
        self.game.gameDisplay.blit(self.surface, self.game.compute_camera_offset(self.rect))
