import pygame as pg
import colors

colors = colors.Colors()

class InputBox:
    def __init__(self, rect, font, color_inactive, color_active, text='', min_num=None, max_num=None, custom_validation=None):
        self.rect = rect
        self.color = color_inactive
        self.color_inactive = color_inactive
        self.color_active = color_active
        self.text = text
        self.font = font
        self.txt_surface = self.font.render(text, True, self.color)
        self.active = False
        self.max_num = max_num
        self.min_num = min_num
        self.custom_validation = custom_validation

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
                if self.active:
                    self.text = ""
                else:
                    self.color = self.color_inactive
            else:
                self.active = False
                self.color = self.color_inactive
                self.validate_numtext(self.max_num, ">")
                self.validate_numtext(self.min_num, "<")
            self.txt_surface = self.font.render(self.text, True, self.color)
            # Change the current color of the input box.
            self.color = self.color_active if self.active else self.color_inactive
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    self.active = False
                    self.color = self.color_inactive
                elif event.key == pg.K_v and event.mod & pg.KMOD_CTRL:
                    clipboard_text = pg.scrap.get(pg.SCRAP_TEXT)
                    try:
                        clipboard_text = str(clipboard_text)[2:str(clipboard_text).index("\\")]
                    except Exception as e:
                        clipboard_text = ""
                    if clipboard_text:
                        self.text += clipboard_text
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                if self.custom_validation:
                    self.validate_custom()
                self.txt_surface = self.font.render(self.text, True, self.color)

    def draw(self, screen, x=None, y=None):
        # Blit the text.
        if x and y:
            screen.blit(self.txt_surface, (x, y))
        else:
            screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+(self.rect.height//2-self.txt_surface.get_height()//2)))
        # Blit the rect.
        pg.draw.rect(screen, colors.purple if self.rect.collidepoint(pg.mouse.get_pos()) else self.color, self.rect, 2, 10)

    def validate_custom(self):
        for char in self.text:
            if char not in self.custom_validation:
                self.text = self.text.replace(char, "")

    def validate_numtext(self, num, op):
        if type(num) == int:
            if self.text:
                if op == "<":
                    if int(self.text) < num:
                        self.text = str(num)
                elif op == ">":
                    if int(self.text) > num:
                        self.text = str(num)
            else:
                self.text = str(num)

    def text_width(self):
        return self.txt_surface.get_width()

    def text_height(self):
        return self.txt_surface.get_height()
