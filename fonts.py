import pygame as pg

class Fonts:
    def __init__(self):
        self.normal_font = pg.font.SysFont(None, 32)
        self.symbol_font = pg.font.SysFont("Segoe UI Emoji", 32)
        self.medium_font = pg.font.SysFont(None, 26)
        self.small_font = pg.font.SysFont(None, 22)
