import logger as log
import time
import copy
import random

class Game:
    def __init__(self):
        self.players = []
        self.starttime = 0
        self.phase = -1
        self.game_over = False
        self.turn_count = 0
        self.duration = 0
        self.has_started = False
        self.set_boardsize(12)
        self.layout_time = 60

    def add_player(self, player):
        if player not in self.players:
            self.players.append(player)
            log.success(f"Player {player.name} added to game.")
        else:
            log.info(f"Player {player.name} is already in the game.")

    def remove_player(self, player):
        if player in self.players:
            self.players.remove(player)
            log.success(f"Player {player.name} removed from game.")
        else:
            log.info(f"Player {player.name} is not in the game.")

    def start_game(self):
        if len(self.players) < 2:
            log.info("Not enough players to start the game.")

        for i in range(len(self.players)):
            self.players[i].setup = True
            self.players[i].turn_start = time.time()
            self.players[i].time_for_layout = self.layout_time
            for j in range(self.boardsize):
                row = ["W" for _ in range(self.boardsize)]
                self.players[i].layout.append(row)
                row = ["" for _ in range(self.boardsize)]
                self.players[i].enemy_layout.append(row)

            self.players[i].inventory.append(self.boardsize*self.boardsize//36)
            self.players[i].inventory.append(self.boardsize*self.boardsize//48)
            self.players[i].inventory.append(self.boardsize*self.boardsize//72)
            self.players[i].inventory.append(self.boardsize*self.boardsize//144)

            if self.players[i].inventory[0] <= 0:
                self.players[i].inventory[0] = 1

        self.players[0].is_my_turn = True
        log.success(f"Game started with players: {', '.join([player.name for player in self.players])}")
        self.players[0].turn_start = time.time()
        self.starttime = time.time()
        self.has_started = True
        self.phase = 0

    def next_player(self):
        self.turn_count += 1

        self.players[0].is_my_turn = not self.players[0].is_my_turn
        self.players[1].is_my_turn = not self.players[1].is_my_turn

        for player in self.players:
            if player.is_my_turn:
                player.turn_start = time.time()

    def shoot_field(self, player, command):
        values = command.split(":")

    def time_over(self, player):
        if self.phase == 0 and player.turn_start + self.layout_time <= time.time() and player.setup:
            log.info(f"{player.name} has run out of time")
            player.setup = False
            self.rand_place(player)
        elif self.phase == 1 and player.is_my_turn and player.turn_start + player.time_for_turn <= time.time():
            log.info(f"{player.name} has run out of time.")
            self.next_player()

    def is_game_over(self):
        if self.game_over:
            self.duration = time.time() - self.starttime
            return True
        return False

    def place_ship(self, player, command):
        values = command.split(":")

        new_layout = copy.deepcopy(player.layout)

        if player.inventory[int(values[1])-1] > 0:
            try:
                for i in range(int(values[1])):
                    if values[2] == "hor":
                        if new_layout[int(values[4])][int(values[3])+i] != "W":
                            raise Exception("ships crashing")
                        new_layout[int(values[4])][int(values[3])+i] = f"OS{values[1]}H" if i == 0 else f"S{values[1]}"
                    elif values[2] == "ver":
                        if new_layout[int(values[4])+i][int(values[3])] != "W":
                            raise Exception("ships crashing")
                        new_layout[int(values[4])+i][int(values[3])] = f"OS{values[1]}V" if i == 0 else f"S{values[1]}"

                player.inventory[int(values[1])-1] -= 1
                player.layout = copy.deepcopy(new_layout)
                log.info(f"{player.name} placed a ship")
            except IndexError:
                log.warning(f"{player.name} tried to place a ship out of bounce")
            except Exception as e:
                if str(e) == "ships crashing":
                    log.warning(f"{player.name} tried to place a ship on top of another ship")
                else:
                    log.error(str(e))

    def rand_place(self, player):
        while player.inventory.count(0) < len(player.inventory):
            command = (f"place:"
                       f"{random.randint(1, len(player.inventory))}:"
                       f"{random.choice(["hor", "ver"])}:"
                       f"{random.randint(0, len(player.layout))}:"
                       f"{random.randint(0, len(player.layout[0]))}")
            self.place_ship(player, command)

    def set_boardsize(self, boardsize):
        if boardsize > 24:
            log.warning(f"You can not set the board size above 24")
            boardsize = 24
        self.boardsize = boardsize
