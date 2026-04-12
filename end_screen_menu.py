import pygame as pg
import fonts as font
import colors as color

class EndScreenMenu:
    def __init__(self, fps, clock, screen, centre):
        self.fps_cap = fps
        self.clock = clock
        self.screen = screen
        self.centre = centre
        self.color = color.Colors()
        self.font = font.Fonts()

    def loop(self, player, data):
        mouse_pressed = True
        while True:

            self.screen.fill("darkgray")

            if not pg.mouse.get_pressed()[0] and not pg.mouse.get_pressed()[2]:
                mouse_pressed = False

            mousepos = pg.mouse.get_pos()

            if data[2] == player.player_id:
                text = self.font.normal_font.render(f"YOU WON!", True, self.color.green)
            else:
                text = self.font.normal_font.render(f"YOU LOST!", True, self.color.red)
            self.screen.blit(text, (self.centre.x - text.get_width() // 2, self.centre.y - text.get_height() // 2))

            pad = 3
            text = self.font.normal_font.render(f"confirm", True, self.color.black)
            rect = pg.Rect(self.centre.x - pad - text.get_width() // 2, 1000,
                           text.get_width() + pad * 2, text.get_height() + pad * 2)
            self.screen.blit(text, (rect.x + pad, rect.y + pad))

            if rect.collidepoint(mousepos):
                pg.draw.rect(self.screen, self.color.purple, rect, 2, 10)
                if pg.mouse.get_pressed()[0]:
                    mouse_pressed = True
                    return True
            else:
                pg.draw.rect(self.screen, self.color.black, rect, 2, 10)

            origin_x = 400
            origin_y = 400
            pad = 5
            text = self.font.normal_font.render(f"Time played: {round(data[1], 2)}", True, self.color.black)
            self.screen.blit(text, (origin_x, origin_y))
            origin_y += text.get_height() + pad

            text = self.font.normal_font.render(f"Overall turns: {data[0]}", True, self.color.black)
            self.screen.blit(text, (origin_x, origin_y))
            origin_y += text.get_height() + pad

            pg.display.flip()
            self.clock.tick(self.fps_cap)

            for event in pg.event.get():
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                    pg.quit()
                    return False
