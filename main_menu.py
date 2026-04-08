import pygame as pg
import entrybox as eb
import colors as color
import fonts as font
from multiprocessing import Process
import logger as log

class MainMenu:
    def __init__(self, fps, clock, screen, centre):
        self.fps_cap = fps
        self.clock = clock
        self.screen = screen
        self.centre = centre
        self.color = color.Colors()
        self.font = font.Fonts()

    def loop(self, local_ip, port):
        host_ip_box = eb.InputBox(pg.Rect(self.centre.x+35, self.centre.y-37, 180, 32), self.font.normal_font,
                                  self.color.orange, self.color.green, local_ip, custom_validation="0123456789.")
        host_port_box = eb.InputBox(pg.Rect(self.centre.x+35, self.centre.y+5, 180, 32), self.font.normal_font,
                                    self.color.orange, self.color.green, port, 1024, 65535, "0123456789")

        boxes = [host_ip_box, host_port_box]

        mouse_pressed = False
        while True:
            mouse_x, mouse_y = pg.mouse.get_pos()
            if not pg.mouse.get_pressed()[0]:
                mouse_pressed = False

            self.screen.fill("gray")

            host_rect = pg.draw.rect(self.screen, self.color.orange, (self.centre.x-145, self.centre.y-37, 100, 32), 2, 10)
            text = self.font.normal_font.render('Host', True, self.color.red)
            self.screen.blit(text, (host_rect.x + (host_rect.width // 2 - text.get_width() // 2),
                               host_rect.y + (host_rect.height // 2 - text.get_height() // 2)))
            if host_rect.collidepoint(mouse_x, mouse_y):
                if pg.mouse.get_pressed()[0] and not mouse_pressed:
                    mouse_pressed = True
                    try:
                        pass
                    except Exception as e:
                        log.warning("Coudn't start server: ", e)

            join_rect = pg.draw.rect(self.screen, self.color.orange, (self.centre.x-145, self.centre.y+5, 100, 32), 2, 10)
            text = self.font.normal_font.render('Join', True, self.color.red)
            self.screen.blit(text, (join_rect.x + (join_rect.width // 2 - text.get_width() // 2),
                               join_rect.y + (join_rect.height // 2 - text.get_height() // 2)))
            if join_rect.collidepoint(mouse_x, mouse_y):
                if pg.mouse.get_pressed()[0] and not mouse_pressed:
                    mouse_pressed = True
                    try:
                        pass
                    except ConnectionRefusedError:
                        log.error("Connection refused. Make sure the server is running.")
                        continue
                    except Exception as e:
                        log.error("coudn't connect to server:")
                        continue

            for box in boxes:
                box.draw(self.screen)

            try:
                pg.display.flip()
                self.clock.tick(self.fps_cap)
            except pg.error:
                return

            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        pg.quit()
                        return

                for box in boxes:
                    box.handle_event(event)

                if event.type == pg.QUIT:
                    pg.quit()
                    return
