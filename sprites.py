import pygame as pg
from pygame.sprite import Sprite

from settings import *


vec = pg.math.Vector2


# Parent sprite class shared by both test rectangles so movement code only lives once.
class Mover(Sprite):
    def __init__(self, game, x, y, color, controls, group, hit_rect_template):
        self.groups = game.all_sprites, group  # group
        Sprite.__init__(self, self.groups)
        self.game = game
        self.controls = controls
        self.image = pg.Surface((RECT_WIDTH, RECT_HEIGHT))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))  # creating rect for vector math
        self.pos = vec(x, y)  # position
        self.vel = vec(0, 0)  # velocity
        self.hit_rect = hit_rect_template.copy()
        self.hit_rect.topleft = self.rect.topleft

    def get_input(self):  # reads the control scheme assigned to this rectangle
        keys = pg.key.get_pressed()
        self.vel.x = 0
        self.vel.y = 0

        if keys[self.controls["left"]]:
            self.vel.x -= RECT_SPEED
        if keys[self.controls["right"]]:
            self.vel.x += RECT_SPEED
        if keys[self.controls["up"]]:
            self.vel.y -= RECT_SPEED
        if keys[self.controls["down"]]:
            self.vel.y += RECT_SPEED

    def clamp_to_screen(self):
        # keeps the rectangle inside the window so collision tests stay visible
        self.pos.x = max(SCREEN_PADDING, min(self.pos.x, WIDTH - RECT_WIDTH - SCREEN_PADDING))
        self.pos.y = max(SCREEN_PADDING, min(self.pos.y, HEIGHT - RECT_HEIGHT - SCREEN_PADDING))

    def reset_position(self, x, y):
        # hard-resets both the visual rect and hitbox to the requested coordinates
        self.pos.update(x, y)
        self.rect.topleft = (round(self.pos.x), round(self.pos.y))
        self.hit_rect.topleft = self.rect.topleft

    def update(self):  # frame-by-frame movement update for each rectangle
        self.get_input()
        self.pos += self.vel * self.game.dt
        self.clamp_to_screen()
        self.rect.topleft = (round(self.pos.x), round(self.pos.y))  # updates visual position
        self.hit_rect.topleft = self.rect.topleft


# First player-controlled test rectangle using WASD.
class RectOne(Mover):
    def __init__(self, game, x, y):
        controls = {
            "left": pg.K_a,
            "right": pg.K_d,
            "up": pg.K_w,
            "down": pg.K_s,
        }
        super().__init__(
            game,
            x,
            y,
            RECT_ONE_COLOR,
            controls,
            game.rect_one_group,
            RECT_ONE_HIT_RECT,
        )


# Second player-controlled test rectangle using arrow keys.
class RectTwo(Mover):
    def __init__(self, game, x, y):
        controls = {
            "left": pg.K_LEFT,
            "right": pg.K_RIGHT,
            "up": pg.K_UP,
            "down": pg.K_DOWN,
        }
        super().__init__(
            game,
            x,
            y,
            RECT_TWO_COLOR,
            controls,
            game.rect_two_group,
            RECT_TWO_HIT_RECT,
        )
