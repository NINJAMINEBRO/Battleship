import colors as color
import fonts as font
import pygame as pg
from time import sleep, time
import logger as log
from threading import Thread
import bot
import copy


class GameMenu:
    scale_factor = 2
    ship_1x1 = pg.transform.scale_by(pg.image.load("assets/1x1.png"), scale_factor)
    ship_1x2 = pg.transform.scale_by(pg.image.load("assets/1x2.png"), scale_factor)
    ship_1x3 = pg.transform.scale_by(pg.image.load("assets/1x3.png"), scale_factor)
    ship_1x4 = pg.transform.scale_by(pg.image.load("assets/1x4.png"), scale_factor)
    ships = [ship_1x1, ship_1x2, ship_1x3, ship_1x4]

    def __init__(self, fps, clock, screen, centre, server, client):
        self.fps_cap = fps
        self.clock = clock
        self.screen = screen
        self.centre = centre
        self.color = color.Colors()
        self.font = font.Fonts()
        self.server = server
        self.client = client

    def loop(self):
        mouse_pressed = True
        data = None
        send_cooldown = 0.2
        last_send_time = time()
        selection = None
        orientation = "hor"
        while True:
            message = "a"
            if not pg.mouse.get_pressed()[0] and not pg.mouse.get_pressed()[2]:
                mouse_pressed = False

            self.screen.fill("darkgray")  # fill the screen with a color to wipe away anything from last frame
            data = self.client.receive_message(data)
            if data is not None:
                if data[0] == "Game Over":
                    if self.server is not None:
                        self.client.disconnect()
                        sleep(1)
                        self.server.terminate()
                    else:
                        self.client.disconnect()
                    return True

                myplayer = data[0]
                enemy = data[1]
                boardsize = data[2]

                """
                    Client site game logic starts here
                """

                mousepos = pg.mouse.get_pos()
                surrender_button = pg.draw.rect(self.screen, self.color.black, (10, 10, 128, 32), 2, 10)
                text = self.font.normal_font.render("GIVE UP", True, self.color.black)
                self.screen.blit(text, (surrender_button.x + (surrender_button.width // 2 - text.get_width() // 2),
                                   surrender_button.y + (surrender_button.height // 2 - text.get_height() // 2)))
                if surrender_button.collidepoint(mousepos) and pg.mouse.get_pressed()[0] and not mouse_pressed:
                    mouse_pressed = True
                    message = "surrender"

                if not enemy:
                    add_bot_button = pg.draw.rect(self.screen, self.color.black, (self.centre.x - 64, self.centre.y - 280, 128, 32), 2, 10)
                    text = self.font.normal_font.render("Add Bot", True, self.color.black)
                    self.screen.blit(text, (add_bot_button.x + (add_bot_button.width // 2 - text.get_width() // 2),
                                       add_bot_button.y + (add_bot_button.height // 2 - text.get_height() // 2)))
                    if add_bot_button.collidepoint(mousepos) and pg.mouse.get_pressed()[0] and not mouse_pressed:
                        mouse_pressed = True
                        t1 = Thread(target=bot.Bot, args=(self.client.host, self.client.port))
                        t1.start()

                if myplayer.setup:
                    base_scale = 800
                    scale = base_scale//boardsize
                    origin_x = self.centre.x-((boardsize/2)*scale)
                    origin_y = self.centre.y-(base_scale/2)
                    rounding = scale//8
                    for y in range(boardsize):
                        for x in range(boardsize):
                            rect = pg.Rect(origin_x+x*scale, origin_y+y*scale, scale, scale)
                            pg.draw.rect(self.screen, self.color.purple if rect.collidepoint(mousepos) else self.color.black, rect, 2, -1,
                                         rounding if y == 0 and x == 0 else -1,
                                         rounding if y == 0 and x == boardsize-1 else -1,
                                         rounding if y == boardsize-1 and x == 0 else -1,
                                         rounding if y == boardsize-1 and x == boardsize-1 else -1)

                            if selection and pg.mouse.get_pressed()[0] and not mouse_pressed and rect.collidepoint(mousepos):
                                mouse_pressed = True
                                message = f"place:{selection[1]}:{x}:{y}"
                                selection = None

                    for y in range(boardsize):
                        for x in range(boardsize):
                            rect = pg.Rect(origin_x+x*scale, origin_y+y*scale, scale, scale)
                            if myplayer.layout[y][x] == "OS1H":
                                self.screen.blit(pg.transform.scale_by(self.ship_1x1, scale/100), (rect.x, rect.y))
                            elif myplayer.layout[y][x] == "OS2H":
                                self.screen.blit(pg.transform.scale_by(self.ship_1x2, scale/100), (rect.x, rect.y))
                            elif myplayer.layout[y][x] == "OS3H":
                                self.screen.blit(pg.transform.scale_by(self.ship_1x3, scale/100), (rect.x, rect.y))
                            elif myplayer.layout[y][x] == "OS4H":
                                self.screen.blit(pg.transform.scale_by(self.ship_1x4, scale/100), (rect.x, rect.y))
                            elif myplayer.layout[y][x] == "OS1V":
                                self.screen.blit(pg.transform.rotate(pg.transform.scale_by(self.ship_1x1, scale/100), -90), (rect.x, rect.y))
                            elif myplayer.layout[y][x] == "OS2V":
                                self.screen.blit(pg.transform.rotate(pg.transform.scale_by(self.ship_1x2, scale/100), -90), (rect.x, rect.y))
                            elif myplayer.layout[y][x] == "OS3V":
                                self.screen.blit(pg.transform.rotate(pg.transform.scale_by(self.ship_1x3, scale/100), -90), (rect.x, rect.y))
                            elif myplayer.layout[y][x] == "OS4V":
                                self.screen.blit(pg.transform.rotate(pg.transform.scale_by(self.ship_1x4, scale/100), -90), (rect.x, rect.y))

                    origin_x = 100
                    origin_y = 140
                    spacing = self.ships[0].get_height()
                    for i in range(len(self.ships)):
                        rect = pg.Rect(origin_x, origin_y+spacing*i, self.ships[i].get_width(), self.ships[i].get_height())
                        self.screen.blit(self.ships[i], (origin_x, origin_y+spacing*i))
                        text = self.font.normal_font.render(f"{myplayer.inventory[i]}x{i+1}", True, self.color.black)
                        self.screen.blit(text, (rect.x-text.get_width()-10, rect.y+self.ships[i].get_height()//2-text.get_height()//2))
                        if rect.collidepoint(mousepos):
                            pg.draw.rect(self.screen, self.color.purple, rect, 2, 10)
                            if pg.mouse.get_pressed()[0] and not mouse_pressed:
                                mouse_pressed = True
                                orientation = "hor"
                                selection = [self.ships[i].copy(), f"{i+1}:{orientation}"]

                    if selection:
                        self.screen.blit(selection[0], (mousepos[0]-50, mousepos[1]-50))
                        if pg.mouse.get_pressed()[0] and not mouse_pressed:
                            mouse_pressed = True
                            selection = None
                        elif pg.mouse.get_pressed()[2] and not mouse_pressed:
                            mouse_pressed = True
                            if selection[1].endswith("hor"):
                                selection[1] = selection[1][:-3]+"ver"
                                selection[0] = pg.transform.rotate(selection[0], -90)
                            elif selection[1].endswith("ver"):
                                selection[1] = selection[1][:-3]+"hor"
                                selection[0] = pg.transform.rotate(selection[0], 90)

            else:
                if self.server is not None:
                    self.server.terminate()
                log.error("aborted game")
                return True

            self.client.send_message(message)

            pg.display.flip()
            self.clock.tick(self.fps_cap)

            for event in pg.event.get():
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                    if self.server is not None:
                        self.server.terminate()
                    pg.quit()
                    return False
