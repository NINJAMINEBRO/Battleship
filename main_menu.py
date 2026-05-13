import pygame as pg
import entrybox as eb
import colors as color
import fonts as font
from multiprocessing import Process
import logger as log
import server
import client
import settings_menu

class MainMenu:
    def __init__(self, fps, clock, screen, centre, settings):
        self.fps_cap = fps
        self.clock = clock
        self.screen = screen
        self.centre = centre
        self.color = color.Colors()
        self.font = font.Fonts()
        self.client = None
        self.server = None
        self.settings = settings
        self.settingsMenu = settings_menu.SettingsMenu(self.fps_cap, self.clock, self.screen, self.centre, self.settings)

    def loop(self, local_ip, port):
        host_ip_box = eb.InputBox(pg.Rect(self.centre.x+15, self.centre.y-37, 180, 32), self.font.normal_font,
                                  self.color.black, self.color.green, local_ip, custom_validation="0123456789.")
        host_port_box = eb.InputBox(pg.Rect(self.centre.x+15, self.centre.y+5, 180, 32), self.font.normal_font,
                                    self.color.black, self.color.green, port, 1024, 65535, "0123456789")

        boxes = [host_ip_box, host_port_box]

        mouse_pressed = False
        while True:
            mousepos = pg.mouse.get_pos()
            if not pg.mouse.get_pressed()[0]:
                mouse_pressed = False

            self.screen.fill("darkgray")

            text = self.font.normal_font.render('Host', True, self.color.black)
            rect = pg.Rect(self.centre.x - 125, self.centre.y - 37, 100, 32)
            self.screen.blit(text, (rect.x + (rect.width // 2 - text.get_width() // 2),
                               rect.y + (rect.height // 2 - text.get_height() // 2)))
            if rect.collidepoint(mousepos):
                pg.draw.rect(self.screen, self.color.purple, rect, 2, 10)
                if pg.mouse.get_pressed()[0] and not mouse_pressed:
                    mouse_pressed = True
                    try:
                        self.server = Process(target=server.start_server,
                                    args=(host_ip_box.text, int(host_port_box.text), self.settings))
                        self.server.start()
                        self.client = client.Client(host_ip_box.text, int(host_port_box.text))
                        return True
                    except Exception as e:
                        log.warning(f"Coudn't start server: {e}")
            else:
                pg.draw.rect(self.screen, self.color.black, rect, 2, 10)

            text = self.font.normal_font.render('Join', True, self.color.black)
            rect = pg.Rect(self.centre.x - 125, self.centre.y + 5, 100, 32)
            self.screen.blit(text, (rect.x + (rect.width // 2 - text.get_width() // 2),
                               rect.y + (rect.height // 2 - text.get_height() // 2)))
            if rect.collidepoint(mousepos):
                pg.draw.rect(self.screen, self.color.purple, rect, 2, 10)
                if pg.mouse.get_pressed()[0] and not mouse_pressed:
                    mouse_pressed = True
                    try:
                        self.client = client.Client(host_ip_box.text, int(host_port_box.text))
                        return True
                    except ConnectionRefusedError:
                        log.error("Connection refused. Make sure the server is running.")
                        continue
                    except Exception as e:
                        log.error(f"coudn't connect to server: {e}")
                        continue
            else:
                pg.draw.rect(self.screen, self.color.black, rect, 2, 10)

            text = self.font.normal_font.render('Quit', True, self.color.black)
            rect = pg.Rect(10, self.screen.get_height()-42, 100, 32)
            self.screen.blit(text, (rect.x + (rect.width // 2 - text.get_width() // 2),
                               rect.y + (rect.height // 2 - text.get_height() // 2)))
            if rect.collidepoint(mousepos):
                pg.draw.rect(self.screen, self.color.purple, rect, 2, 10)
                if pg.mouse.get_pressed()[0] and not mouse_pressed:
                    mouse_pressed = True
                    pg.quit()
                    return False
            else:
                pg.draw.rect(self.screen, self.color.black, rect, 2, 10)

            text = self.font.symbol_font.render('⚙', True, self.color.black)
            rect = pg.Rect(self.screen.get_width()-60, 10, 50, 50)
            self.screen.blit(text, (rect.x + (rect.width // 2 - text.get_width() // 2),
                                    rect.y + (rect.height // 2 - text.get_height() // 2)))
            if rect.collidepoint(mousepos):
                pg.draw.rect(self.screen, self.color.purple, rect, 2, 10)
                if pg.mouse.get_pressed()[0] and not mouse_pressed:
                    mouse_pressed = True
                    if not self.settingsMenu.loop():
                        return False

            else:
                pg.draw.rect(self.screen, self.color.black, rect, 2, 10)

            for box in boxes:
                box.draw(self.screen)

            if not host_ip_box.active:
                self.settings.last_used_ip = host_ip_box.text
            if not host_port_box.active:
                self.settings.last_used_port = host_port_box.text

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

                for box in boxes:
                    box.handle_event(event)
