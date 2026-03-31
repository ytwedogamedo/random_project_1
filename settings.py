import pygame as pg

# regular game settings
WIDTH = 960
HEIGHT = 736
TITLE = "Collision Tester"
FPS = 60

# tuple storing RGB color values
BACKGROUND_COLOR = (18, 24, 38)
HUD_TEXT_COLOR = (240, 244, 248)
RECT_ONE_COLOR = (66, 135, 245)
RECT_TWO_COLOR = (245, 166, 35)
SAFE_COLOR = (86, 204, 157)
COLLISION_COLOR = (235, 87, 87)

# rectangle values
RECT_WIDTH = 120
RECT_HEIGHT = 120
RECT_SPEED = 320
SCREEN_PADDING = 12

# start points for each rectangle so they begin separated
RECT_ONE_START = (160, HEIGHT // 2 - RECT_HEIGHT // 2)
RECT_TWO_START = (WIDTH - 280, HEIGHT // 2 - RECT_HEIGHT // 2)

# template hitboxes copied into each sprite on creation
RECT_ONE_HIT_RECT = pg.Rect(0, 0, RECT_WIDTH, RECT_HEIGHT)
RECT_TWO_HIT_RECT = pg.Rect(0, 0, RECT_WIDTH, RECT_HEIGHT)
