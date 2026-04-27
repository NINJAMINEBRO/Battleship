import client
import copy
import random
from time import time


class Bot:
    def __init__(self, host, ip, difficulty):
        self.bot = client.Client(host, ip)
        self.bot_model = "random"
        self.current_events = []
        self.difficulty = difficulty

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
            not_shoot_coords = []
            for y in range(len(mypl.enemy_layout)):
                for x in range(len(mypl.enemy_layout[y])):
                    if mypl.enemy_layout[y][x] == "":
                        not_shoot_coords.append([x, y])

            if self.difficulty == 1:
                message = self.difficulty_1_play_logic(not_shoot_coords)
            elif self.difficulty == 2:
                message = self.difficulty_2_play_logic(not_shoot_coords, mypl.enemy_layout)

        return message

    def difficulty_1_play_logic(self, coords):
        if coords:
            coord = random.choice(coords)
            message = f"shoot:{coord[0]}:{coord[1]}"
        else:
            message = f"shoot:0:0"
        return message

    def difficulty_2_play_logic(self, coords, layout):
        message = None
        if coords:
            for coord in coords:
                pos = self.check_for_hit_around(coord, layout)
                if pos is not None:
                    message = f"shoot:{pos[0]}:{pos[1]}"
                    break
            if message is None:
                coords_left = len(coords)
                for i in range(coords_left):
                    coord = random.choice(coords)
                    coords.remove(coord)
                    if not self.check_for_diagonal(coord, layout):
                        message = f"shoot:{coord[0]}:{coord[1]}"
                        break
        if message is None:
            message = f"shoot:0:0"
        return message

    def check_for_hit_around(self, pos, layout):
        if self.check_for_diagonal(pos, layout):
            return None

        offsets = [[0, 1], [1, 0], [0, -1], [-1, 0]]

        for offset in offsets:
            pos_1 = pos[0] + offset[0]
            pos_2 = pos[1] + offset[1]
            if len(layout[0]) > pos_1 >= 0 and len(layout) > pos_2 >= 0 and "S" in layout[pos_2][pos_1]:
                return pos

        return None

    def check_for_diagonal(self, pos, layout):
        offsets = [[-1, -1], [1, -1], [-1, 1], [1, 1]]

        for offset in offsets:
            pos_1 = pos[0] + offset[0]
            pos_2 = pos[1] + offset[1]
            if len(layout[0]) > pos_1 >= 0 and len(layout) > pos_2 >= 0:
                print(layout[pos_2][pos_1])
            if len(layout[0]) > pos_1 >= 0 and len(layout) > pos_2 >= 0 and "S" in layout[pos_2][pos_1]:
                return True
        return False
