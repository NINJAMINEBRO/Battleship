from pygame import Vector2
import client
import copy
import random
from time import time


class Bot:
    def __init__(self, host, ip, settings):
        self.bot = client.Client(host, ip)
        self.bot_model = "random"
        self.current_events = []
        self.difficulty = settings.bot_difficulty
        self.myplayer = None
        self.settings = settings

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

                self.myplayer = data[0]
                enemyplayer = data[1]

                if last_send_time + send_cooldown < time():
                    message = self.play_logic(self.myplayer, message)

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
            elif not self.settings.strict_placement:
                message = self.difficulty_without_strict_placement(not_shoot_coords, mypl.enemy_layout)
            elif self.difficulty == 2:
                message = self.difficulty_2_play_logic(not_shoot_coords, mypl.enemy_layout)
            elif self.difficulty == 3:
                message = self.difficulty_3_play_logic(not_shoot_coords, mypl.enemy_layout)

        return message

    def difficulty_without_strict_placement(self, coords, layout):
        message = None
        if coords:
            random.shuffle(coords)
            for coord in coords:
                pos = self.check_for_hit_around(coord, layout)
                if pos is not None:
                    message = f"shoot:{pos[0]}:{pos[1]}"
                    break

            num = random.randint(1, 2)
            if message is None and num == 1:
                for coord in coords:
                    if not self.check_for_hit_around(coord, layout, False, True):
                        message = f"shoot:{coord[0]}:{coord[1]}"
                        break

        if message is None:
            message = self.difficulty_1_play_logic(coords)
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
            random.shuffle(coords)
            for coord in coords:
                pos = self.check_for_hit_around(coord, layout)
                if pos is not None:
                    message = f"shoot:{pos[0]}:{pos[1]}"
                    break
            if message is None:
                for coord in coords:
                    if not self.check_for_diagonal(coord, layout):
                        message = f"shoot:{coord[0]}:{coord[1]}"
                        break

        if message is None:
            message = self.difficulty_1_play_logic(coords)
        return message
    
    def difficulty_3_play_logic(self, coords, layout):
        message = None
        enemy_ship_counts = copy.deepcopy(self.myplayer.enemy_ships_left)
        longest_ship = self.get_longest_ship(enemy_ship_counts.copy())

        if coords:
            random.shuffle(coords)
            for coord in coords:
                pos = self.check_for_hit_around(coord, layout)
                if pos is not None:
                    hit_pos = self.check_for_hit_around(coord, layout, True)
                    ship_size = self.get_shipsize_on_coord(hit_pos, self.myplayer.enemy_layout, pos)
                    if ship_size < longest_ship:
                        message = f"shoot:{pos[0]}:{pos[1]}"
                        break

            if message is None:
                for coord in coords:
                    if self.check_for_hit_around(coord, layout, return_1_on_diagonal=True) is None:
                        message = f"shoot:{coord[0]}:{coord[1]}"
                        break

        if message is None:
            message = self.difficulty_1_play_logic(coords)
        return message

    def get_shipsize_on_coord(self, coord, layout, from_coord):
        if coord[1] >= 0 and coord[0] >= 0 and coord[1] < len(layout) and coord[0] < len(layout[0]) and layout[coord[1]][coord[0]].startswith("S"):
            dir_vector = self.get_vector(coord, from_coord)
            new_coord = [coord[0]+dir_vector[0], coord[1]+dir_vector[1]]
            return 1 + self.get_shipsize_on_coord(new_coord, layout, coord)
        else:
            return 0

    def get_vector(self, to_coord, from_coord):
        x = 0
        y = 0
        if to_coord[0] < from_coord[0]:
            x = -1
        elif to_coord[0] > from_coord[0]:
            x = 1

        if to_coord[1] < from_coord[1]:
            y = -1
        elif to_coord[1] > from_coord[1]:
            y = 1

        return [x, y]
    
    def get_longest_ship(self, ship_counts):
        longest_ship_size = -1
        for size in range(len(ship_counts)):
            if ship_counts[size] > 0:
                longest_ship_size = size+1

        return longest_ship_size

    def check_for_hit_around(self, pos, layout, get_hit_around=False, ignore_diagonal=False, return_1_on_diagonal=False):
        if not ignore_diagonal and self.check_for_diagonal(pos, layout):
            if return_1_on_diagonal:
                return 1
            return None

        offsets = [[0, 1], [1, 0], [0, -1], [-1, 0]]

        for offset in offsets:
            pos_1 = pos[0] + offset[0]
            pos_2 = pos[1] + offset[1]
            if len(layout[0]) > pos_1 >= 0 and len(layout) > pos_2 >= 0 and "S" in layout[pos_2][pos_1]:
                if get_hit_around:
                    return [pos_1, pos_2]
                return pos

        return None

    def check_for_diagonal(self, pos, layout):
        offsets = [[-1, -1], [1, -1], [-1, 1], [1, 1]]

        for offset in offsets:
            pos_1 = pos[0] + offset[0]
            pos_2 = pos[1] + offset[1]
            if len(layout[0]) > pos_1 >= 0 and len(layout) > pos_2 >= 0 and "S" in layout[pos_2][pos_1]:
                return True
        return False
