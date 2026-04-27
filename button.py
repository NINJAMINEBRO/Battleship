import pygame as pg
import colors

colors = colors.Colors()

class Button:
    def __init__(self, rect, font, color, elements, index=0):
        self.rect = rect
        self.font = font
        self.color = color
        self.elements = elements
        self.element = elements[index]
        self.index = index
        self.text_surface = self.font.render(self.element, True, self.color)

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.rotate()

    def rotate(self):
        self.index += 1
        if self.index >= len(self.elements):
            self.index = 0
        self.element = self.elements[self.index]
        self.text_surface = self.font.render(self.element, True, self.color)

    def draw(self, screen):
        screen.blit(self.text_surface, (self.rect.x+(self.rect.width//2)-(self.text_surface.get_width()//2),
                                self.rect.y+(self.rect.height//2)-(self.text_surface.get_height()//2)))
        pg.draw.rect(screen, colors.purple if self.rect.collidepoint(pg.mouse.get_pos()) else self.color, self.rect, 2, 10)
