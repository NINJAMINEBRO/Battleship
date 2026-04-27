import pygame as pg
import logger as log
import colors as color
import fonts as font
import entrybox
import button

class SettingsMenu:
    def __init__(self, fps, clock, screen, centre, settings):
        self.fps_cap = fps
        self.clock = clock
        self.screen = screen
        self.centre = centre
        self.color = color.Colors()
        self.font = font.Fonts()
        self.settings = settings

        fieldsize_box = entrybox.InputBox(pg.Rect(100, 100, 150, 50), self.font.normal_font, self.color.black,
                                          self.color.green, str(self.settings.fieldsize), 1, 24, "0123456789")
        layout_time_box = entrybox.InputBox(pg.Rect(100, 220, 150, 50), self.font.normal_font, self.color.black,
                                            self.color.green, str(self.settings.layout_time), 1, 300, "0123456789")
        turn_time_box = entrybox.InputBox(pg.Rect(100, 340, 150, 50), self.font.normal_font, self.color.black,
                                          self.color.green, str(self.settings.turn_time), 1, 60, "0123456789")
        strict_place_box = button.Button(pg.Rect(100, 460, 150, 50), self.font.normal_font, self.color.black,
                                         ['True', 'False'], 0 if settings.strict_placement else 1)

        self.boxes = [fieldsize_box, layout_time_box, turn_time_box, strict_place_box]

    def loop(self):
        mouse_pressed = False
        while True:
            mousepos = pg.mouse.get_pos()
            if not pg.mouse.get_pressed()[0]:
                mouse_pressed = False

            self.screen.fill("darkgray")

            text = self.font.symbol_font.render("←", True, self.color.black)
            rect = pg.Rect(10, 10, 50, 50)
            self.screen.blit(text, (rect.x + (rect.width // 2 - text.get_width() // 2),
                                    rect.y + (rect.height // 2 - text.get_height() // 2)))
            if rect.collidepoint(mousepos):
                pg.draw.rect(self.screen, self.color.purple, rect, 2, 10)
                if pg.mouse.get_pressed()[0] and not mouse_pressed:
                    mouse_pressed = True
                    return True, self.settings.fieldsize, self.settings.layout_time, self.settings.turn_time
            else:
                pg.draw.rect(self.screen, self.color.black, rect, 2, 10)

            origin_x = 150
            pad = 0
            width = 50
            origin_y = 100
            height = 50
            text = self.font.symbol_font.render(f"Field size:", True, self.color.black)
            rect = pg.Rect(origin_x-width-pad, origin_y-height, width*3+pad*3, height)
            self.screen.blit(text, (rect.x + (rect.width // 2 - text.get_width() // 2),
                                    rect.y + (rect.height // 2 - text.get_height() // 2)))

            origin_x = 150
            pad = 0
            width = 50
            origin_y = 220
            height = 50
            text = self.font.symbol_font.render(f"Layout time:", True, self.color.black)
            rect = pg.Rect(origin_x - width - pad, origin_y - height, width * 3 + pad * 3, height)
            self.screen.blit(text, (rect.x + (rect.width // 2 - text.get_width() // 2),
                                    rect.y + (rect.height // 2 - text.get_height() // 2)))

            origin_x = 150
            pad = 0
            width = 50
            origin_y = 340
            height = 50
            text = self.font.symbol_font.render(f"Turn time:", True, self.color.black)
            rect = pg.Rect(origin_x - width - pad, origin_y - height, width * 3 + pad * 3, height)
            self.screen.blit(text, (rect.x + (rect.width // 2 - text.get_width() // 2),
                                    rect.y + (rect.height // 2 - text.get_height() // 2)))

            origin_x = 150
            pad = 0
            width = 50
            origin_y = 460
            height = 50
            text = self.font.symbol_font.render(f"Strict placement:", True, self.color.black)
            rect = pg.Rect(origin_x - width - pad, origin_y - height, width * 3 + pad * 3, height)
            self.screen.blit(text, (rect.x + (rect.width // 2 - text.get_width() // 2),
                                    rect.y + (rect.height // 2 - text.get_height() // 2)))

            for box in self.boxes:
                box.draw(self.screen)

            try:
                self.settings.fieldsize = int(self.boxes[0].text)
                self.settings.layout_time = int(self.boxes[1].text)
                self.settings.turn_time = int(self.boxes[2].text)
                self.settings.strict_placement = True if self.boxes[3].element == "True" else False
            except ValueError:
                pass

            try:
                pg.display.flip()
                self.clock.tick(self.fps_cap)
            except pg.error:
                return False

            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        pg.quit()
                        return False

                if event.type == pg.QUIT:
                    pg.quit()
                    return False

                for box in self.boxes:
                    box.handle_event(event)
