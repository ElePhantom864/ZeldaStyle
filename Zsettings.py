import pygame as pg
from enum import Enum


class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# game settings
WIDTH = 15 * 32   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 15 * 32  # 16 * 48 or 32 * 24 or 64 * 12
FPS = 60
TITLE = "Tilemap Demo"
BGCOLOR = DARKGREY

TILESIZE = 32

# player settings
PLAYER_SPEED = 150
PLAYER_HIT_RECT = pg.Rect(0, 0, 21, 23)
PLAYER_IMAGES = {
    Direction.UP: [
        'LinkUp1.png',
        'LinkUp2.png',
        'LinkUp3.png'
    ],
    Direction.DOWN: [
        'LinkDown1.png',
        'LinkDown2.png',
        'LinkDown3.png'
    ],
    Direction.LEFT: [
        'LinkLeft1.png',
        'LinkLeft2.png',
        'LinkLeft3.png'
    ],
    Direction.RIGHT: [
        'LinkRight1.png',
        'LinkRight2.png',
        'LinkRight3.png'
    ],
}

# mob settings
COBRA_IMAGES = {
    Direction.UP: [
        'CobraUp1.png',
        'CobraUp2.png'
    ],
    Direction.DOWN: [
        'CobraDown1.png',
        'CobraDown2.png'
    ],
    Direction.LEFT: [
        'CobraLeft1.png',
        'CobraLeft2.png'
    ],
    Direction.RIGHT: [
        'CobraRight1.png',
        'CobraRight2.png'
    ],
}