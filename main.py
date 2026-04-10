import logger as log
import colors as color
import socket
import main_menu as MenuMain
import pygame as pg
from multiprocessing import freeze_support
import centre
import game_menu as MenuGame

def get_lan_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = str(s.getsockname()[0])
        s.close()
        return ip
    except Exception as e:
        log.warning(f"could not grab local ip: {str(e)}")
        return "127.0.0.1"

def initialize_pygame():
    pg.init()
    freeze_support()
    pg.init()

def initialize_extras():
    pg.scrap.init()
    pg.scrap.set_mode(pg.SCRAP_CLIPBOARD)
    pg.display.set_caption("Schiffe versenken")

if __name__ == '__main__':
    log.success("Client started")

    initialize_pygame()

    # Set global variables
    width, height = 1920, 1080
    screen = pg.display.set_mode((width, height))
    centre = centre.Centre(width, height)
    clock = pg.time.Clock()
    fps = 60
    running = True

    initialize_extras()

    while running:
        main_menu = MenuMain.MainMenu(fps, clock, screen, centre)
        running = main_menu.loop(get_lan_ip(), "56565")

        if running:
            game_menu = MenuGame.GameMenu(fps, clock, screen, centre, main_menu.server, main_menu.client)
            running = game_menu.loop()
