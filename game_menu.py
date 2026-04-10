import colors as color
import fonts as font
import pygame as pg
from time import sleep, time
import logger as log

class GameMenu:
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
        while True:
            message = "a"
            if not pg.mouse.get_pressed()[0]:
                mouse_pressed = False

            self.screen.fill("gray")  # fill the screen with a color to wipe away anything from last frame
            data = self.client.receive_message(data)
            if data is not None:
                if data[0] == "Game Over":
                    if self.server is not None:
                        self.client.disconnect()
                        sleep(1)
                        self.client.terminate()
                    else:
                        self.client.disconnect()
                    return False

                myplayer = data[0]
                enemy = data[1]
                if enemy:
                    enemy = enemy[0]

                mousepos = pg.mouse.get_pos()
                surrender_button = pg.draw.rect(self.screen, self.color.black, (10, 10, 128, 32), 2, 10)
                text = font.render("GIVE UP", True, self.color.black)
                self.screen.blit(text, (surrender_button.x + (surrender_button.width // 2 - text.get_width() // 2),
                                   surrender_button.y + (surrender_button.height // 2 - text.get_height() // 2)))
                if surrender_button.collidepoint(mousepos) and pg.mouse.get_pressed()[0] and not mouse_pressed:
                    mouse_pressed = True
                    message = "surrender"

                if enemy:
                    pass
                else:
                    add_bot_button = pg.draw.rect(self.screen, self.color.black, (self.centre.x - 64, self.centre.y - 280, 128, 32), 2, 10)
                    text = font.render("Add Bot", True, self.color.black)
                    self.screen.blit(text, (add_bot_button.x + (add_bot_button.width // 2 - text.get_width() // 2),
                                       add_bot_button.y + (add_bot_button.height // 2 - text.get_height() // 2)))
                    if add_bot_button.collidepoint(mousepos) and pg.mouse.get_pressed()[0] and not mouse_pressed:
                        mouse_pressed = True
                        #t1 = Thread(target=Bot.Bot, args=("Bot", RandomDeck.random_deck(cards), host, port, cards))
                        #t1.start()

            else:
                if self.server is not None:
                    self.server.terminate()
                log.error("aborted game")
                return True

            self.client.send_message(message)

            pg.display.flip()
            self.clock.tick(self.fps_cap)

            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        pg.quit()
                        return False

                if event.type == pg.QUIT:
                    if self.server is not None:
                        self.server.terminate()
                    pg.quit()
                    return False
