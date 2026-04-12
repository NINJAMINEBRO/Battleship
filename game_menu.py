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
    pack_name = "premium"
    ship_1x1 = pg.transform.scale_by(pg.image.load(f"assets/{pack_name}/1x1.png"), scale_factor)
    ship_1x2 = pg.transform.scale_by(pg.image.load(f"assets/{pack_name}/1x2.png"), scale_factor)
    ship_1x3 = pg.transform.scale_by(pg.image.load(f"assets/{pack_name}/1x3.png"), scale_factor)
    ship_1x4 = pg.transform.scale_by(pg.image.load(f"assets/{pack_name}/1x4.png"), scale_factor)
    symbol_hit = pg.transform.scale_by(pg.image.load(f"assets/{pack_name}/symbols/hit.png"), scale_factor)
    symbol_water = pg.transform.scale_by(pg.image.load(f"assets/{pack_name}/symbols/water.png"), scale_factor)
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
        send_cooldown = 0.1
        last_send_time = time()
        selection = []
        myplayer = None
        enemy = None
        while True:
            message = "a"
            if not pg.mouse.get_pressed()[0] and not pg.mouse.get_pressed()[2]:
                mouse_pressed = False

            self.screen.fill("darkgray")
            data = self.client.receive_message(data)
            if data is not None:
                if data[0] == "Game Over":
                    if self.server is not None:
                        self.client.disconnect()
                        sleep(1)
                        self.server.terminate()
                    else:
                        self.client.disconnect()
                    return True, myplayer, data[1]

                myplayer = data[0]
                enemy = data[1]
                boardsize = data[2]

                """
                    Client site game logic starts here
                """

                mousepos = pg.mouse.get_pos()

                text = self.font.normal_font.render("GIVE UP", True, self.color.black)
                rect = pg.Rect(10, 10, 128, 32)
                self.screen.blit(text, (rect.x + (rect.width // 2 - text.get_width() // 2),
                                   rect.y + (rect.height // 2 - text.get_height() // 2)))
                if rect.collidepoint(mousepos):
                    pg.draw.rect(self.screen, self.color.purple, rect, 2, 10)
                    if pg.mouse.get_pressed()[0] and not mouse_pressed:
                        mouse_pressed = True
                        message = "surrender"
                else:
                    pg.draw.rect(self.screen, self.color.black, rect, 2, 10)

                if not enemy:
                    text = self.font.normal_font.render("Add Bot", True, self.color.black)
                    rect = pg.Rect(self.centre.x - 64, self.centre.y - 280, 128, 32)
                    self.screen.blit(text, (rect.x + (rect.width // 2 - text.get_width() // 2),
                                       rect.y + (rect.height // 2 - text.get_height() // 2)))
                    if rect.collidepoint(mousepos):
                        pg.draw.rect(self.screen, self.color.purple, rect, 2, 10)
                        if pg.mouse.get_pressed()[0] and not mouse_pressed:
                            mouse_pressed = True
                            t1 = Thread(target=bot.Bot, args=(self.client.host, self.client.port))
                            t1.start()
                    else:
                         pg.draw.rect(self.screen, self.color.black, rect, 2, 10)

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
                                if time() >= last_send_time + send_cooldown:
                                    message = f"place:{selection[1]}:{x}:{y}"
                                    last_send_time = time()
                                selection = []

                    self.draw_ships(boardsize, myplayer.layout, origin_x, origin_y, scale)

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
                                selection = [pg.transform.scale_by(self.ships[i].copy(), scale/100), f"{i+1}:{orientation}"]

                    pad = 3
                    text = self.font.normal_font.render(f"confirm", True, self.color.black)
                    rect = pg.Rect(self.centre.x-text.get_width()//2-pad, 1000-pad, text.get_width()+pad*2, text.get_height()+pad*2)
                    self.screen.blit(text, (rect.x+pad, rect.y+pad))
                    if rect.collidepoint(mousepos):
                        pg.draw.rect(self.screen, self.color.purple, rect, 2, 10)
                        if pg.mouse.get_pressed()[0] and not mouse_pressed:
                            mouse_pressed = True
                            if time() >= last_send_time + send_cooldown:
                                message = "confirm layout"
                                last_send_time = time()
                    else:
                        pg.draw.rect(self.screen, self.color.black, rect, 2, 10)

                    time_left = myplayer.turn_start + myplayer.time_for_layout - time()
                    if time_left > 0:
                        text = self.font.normal_font.render(f"Time Left: {int(round(time_left, 0))}", True,
                                                            self.color.black)
                        self.screen.blit(text, (self.centre.x - text.get_width() // 2, rect.y + text.get_height() + 10))

                    pad = 3
                    text = self.font.normal_font.render(f"random", True, self.color.black)
                    rect = pg.Rect((self.centre.x + base_scale // 2) - text.get_width() - (pad * 2),
                                   self.centre.y + base_scale // 2 + pad,
                                   text.get_width() + pad * 2,
                                   text.get_height() + pad * 2)
                    self.screen.blit(text, (rect.x + pad, rect.y + pad))
                    if rect.collidepoint(mousepos):
                        pg.draw.rect(self.screen, self.color.purple, rect, 2, 10)
                        if pg.mouse.get_pressed()[0] and not mouse_pressed:
                            mouse_pressed = True
                            if time() >= last_send_time + send_cooldown:
                                message = "random place"
                                last_send_time = time()
                    else:
                        pg.draw.rect(self.screen, self.color.black, rect, 2, 10)

                    if selection:
                        if selection[1].endswith("hor"):
                            self.screen.blit(selection[0], (mousepos[0]-(selection[0].get_height()//2),
                                                            mousepos[1]-(selection[0].get_height()//2)))
                        elif selection[1].endswith("ver"):
                            self.screen.blit(selection[0], (mousepos[0] - (selection[0].get_width() // 2),
                                                            mousepos[1] - (selection[0].get_width() // 2)))
                        if pg.mouse.get_pressed()[0] and not mouse_pressed:
                            mouse_pressed = True
                            selection = []
                        elif pg.mouse.get_pressed()[2] and not mouse_pressed:
                            mouse_pressed = True
                            if selection[1].endswith("hor"):
                                selection[1] = selection[1][:-3]+"ver"
                                selection[0] = pg.transform.rotate(selection[0], -90)
                            elif selection[1].endswith("ver"):
                                selection[1] = selection[1][:-3]+"hor"
                                selection[0] = pg.transform.rotate(selection[0], 90)

                elif not myplayer.setup and myplayer.turn_start > 0:
                    base_scale = 400
                    pad = 20
                    origin_x = self.screen.get_width() - base_scale - pad
                    origin_y = pad
                    self.draw_field(base_scale, boardsize, origin_x, origin_y, myplayer)
                    self.draw_ships(boardsize, enemy.enemy_layout, origin_x, origin_y, base_scale//boardsize)

                    base_scale = 800
                    scale = base_scale // boardsize
                    origin_x = self.centre.x - ((boardsize / 2) * scale)
                    origin_y = self.centre.y - (base_scale / 2)
                    rounding = scale // 8
                    for y in range(boardsize):
                        for x in range(boardsize):
                            rect = pg.Rect(origin_x + x * scale, origin_y + y * scale, scale, scale)
                            pg.draw.rect(self.screen,
                                         self.color.purple if rect.collidepoint(mousepos) else self.color.black, rect,
                                         2, -1,
                                         rounding if y == 0 and x == 0 else -1,
                                         rounding if y == 0 and x == boardsize - 1 else -1,
                                         rounding if y == boardsize - 1 and x == 0 else -1,
                                         rounding if y == boardsize - 1 and x == boardsize - 1 else -1)

                            if pg.mouse.get_pressed()[0] and not mouse_pressed and rect.collidepoint(mousepos):
                                mouse_pressed = True
                                if time() >= last_send_time + send_cooldown:
                                    message = f"shoot:{x}:{y}"
                                    last_send_time = time()

                    self.draw_ships(boardsize, myplayer.enemy_layout, origin_x, origin_y, scale)

                    time_left = myplayer.turn_start + myplayer.time_for_turn - time()
                    if enemy.setup:
                        text = self.font.normal_font.render(f"Waiting for enemy", True, self.color.black)
                        self.screen.blit(text, (self.centre.x-text.get_width()//2, 1000))
                    elif time_left > 0 and myplayer.is_my_turn:
                        text = self.font.normal_font.render(f"Time Left: {int(round(time_left, 0))}", True,
                                                            self.color.black if int(round(time_left, 0)) > 5 else self.color.red)
                        self.screen.blit(text, (self.centre.x - text.get_width() // 2, 1000))

            else:
                if self.server is not None:
                    self.server.terminate()
                log.error("aborted game")
                return True, None, None

            self.client.send_message(message)

            pg.display.flip()
            self.clock.tick(self.fps_cap)

            for event in pg.event.get():
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                    if self.server is not None:
                        self.server.terminate()
                    pg.quit()
                    return False, None, None

    def draw_ships(self, boardsize, layout, origin_x, origin_y, scale):
        for y in range(boardsize):
            for x in range(boardsize):
                rect = pg.Rect(origin_x + x * scale, origin_y + y * scale, scale, scale)
                if layout[y][x] == "OS1H":
                    self.screen.blit(pg.transform.scale_by(self.ship_1x1, scale / 100), (rect.x, rect.y))
                elif layout[y][x] == "OS2H":
                    self.screen.blit(pg.transform.scale_by(self.ship_1x2, scale / 100), (rect.x, rect.y))
                elif layout[y][x] == "OS3H":
                    self.screen.blit(pg.transform.scale_by(self.ship_1x3, scale / 100), (rect.x, rect.y))
                elif layout[y][x] == "OS4H":
                    self.screen.blit(pg.transform.scale_by(self.ship_1x4, scale / 100), (rect.x, rect.y))
                elif layout[y][x] == "OS1V":
                    self.screen.blit(
                        pg.transform.rotate(pg.transform.scale_by(self.ship_1x1, scale / 100), -90),
                        (rect.x, rect.y))
                elif layout[y][x] == "OS2V":
                    self.screen.blit(
                        pg.transform.rotate(pg.transform.scale_by(self.ship_1x2, scale / 100), -90),
                        (rect.x, rect.y))
                elif layout[y][x] == "OS3V":
                    self.screen.blit(
                        pg.transform.rotate(pg.transform.scale_by(self.ship_1x3, scale / 100), -90),
                        (rect.x, rect.y))
                elif layout[y][x] == "OS4V":
                    self.screen.blit(
                        pg.transform.rotate(pg.transform.scale_by(self.ship_1x4, scale / 100), -90),
                        (rect.x, rect.y))
                elif layout[y][x] == "S":
                    self.screen.blit(pg.transform.scale_by(self.symbol_hit, scale / 100), (rect.x, rect.y))
                elif layout[y][x] == "W":
                    self.screen.blit(pg.transform.scale_by(self.symbol_water, scale / 100), (rect.x, rect.y))

    def draw_field(self, base_scale, boardsize, x, y, player):
        scale = base_scale // boardsize
        origin_x = x
        origin_y = y
        rounding = scale // 8
        for y in range(boardsize):
            for x in range(boardsize):
                rect = pg.Rect(origin_x + x * scale, origin_y + y * scale, scale, scale)
                pg.draw.rect(self.screen, self.color.black, rect, 2, -1,
                             rounding if y == 0 and x == 0 else -1,
                             rounding if y == 0 and x == boardsize - 1 else -1,
                             rounding if y == boardsize - 1 and x == 0 else -1,
                             rounding if y == boardsize - 1 and x == boardsize - 1 else -1)

        self.draw_ships(boardsize, player.layout, origin_x, origin_y, scale)
