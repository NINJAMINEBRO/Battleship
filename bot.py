import client
import copy
import random
from time import time


class Bot:
    def __init__(self, host, ip):
        self.bot = client.Client(host, ip)
        self.bot_model = "random"
        self.current_events = []
        self.loop()

    def loop(self):
        data = None
        send_cooldown = 0.15
        last_send_time = time()
        while True:
            message = "a"
            data = self.bot.receive_message(data)
            if data is not None:
                if data[0] == "Game Over":
                    self.bot.disconnect()
                    return

                myplayer = data[0]
                enemyplayer = data[1]

                if last_send_time + send_cooldown < time():
                    message = self.play_logic(myplayer, message)

            else:
                self.bot.disconnect()
                return

            self.bot.send_message(message)

    def play_logic(self, mypl, message):
        if mypl.setup:
            if mypl.inventory.count(0) < len(mypl.inventory):
                message = f"random place"
            else:
                message = f"confirm layout"

        elif mypl.is_my_turn:
            not_shoot_coors = []
            for x in range(len(mypl.enemy_layout)):
                for y in range(len(mypl.enemy_layout[x])):
                    if mypl.enemy_layout[y][x] == "":
                        not_shoot_coors.append([x, y])

            if not_shoot_coors:
                coord = random.choice(not_shoot_coors)
                message = f"shoot:{coord[0]}:{coord[1]}"
            else:
                message = f"shoot:0:0"

        return message
