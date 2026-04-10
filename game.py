import logger as log
import time
import copy

class Game:
    def __init__(self):
        self.players = []
        self.starttime = 0
        self.current_phase = 0
        self.game_over = False
        self.turn_count = 0
        self.duration = 0
        self.has_started = False
        self.boardsize = 8

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
            return False

        for i in range(len(self.players)):
            self.players[i].setup = True
            for j in range(self.boardsize):
                row = ["W" for _ in range(self.boardsize)]
                self.players[i].layout.append(row)

        self.players[0].is_my_turn = True
        log.success(f"Game started with players: {', '.join([player.name for player in self.players])}")
        self.players[0].turn_start = time.time()
        self.starttime = time.time()
        self.has_started = True

    def next_player(self):
        self.turn_count += 1

        self.players[0].is_my_turn = not self.players[0].is_my_turn
        self.players[1].is_my_turn = not self.players[1].is_my_turn

        for player in self.players:
            if player.is_my_turn:
                player.turn_start = time.time()

    def shoot_field(self, player):
        pass

    def time_over(self, player):
        if player.is_my_turn and player.turn_start + player.time_for_turn <= time.time():
            log.info(f"{player.name} has run out of time.")
            self.next_player()

    def is_game_over(self):
        if len(self.players) >= 2:
            pass
        if self.game_over:
            self.duration = time.time() - self.starttime
            return True
        return False

    def place_ship(self, player, command):
        values = command.split(":")

        new_layout = copy.deepcopy(player.layout)

        try:
            for i in range(int(values[1])):
                if values[2] == "hor":
                    if new_layout[int(values[4])][int(values[3])+i] != "W":
                        raise Exception("ships crashing")
                    new_layout[int(values[4])][int(values[3])+i] = f"S{values[1]}"
                elif values[2] == "ver":
                    if new_layout[int(values[4])+i][int(values[3])] != "W":
                        raise Exception("ships crashing")
                    new_layout[int(values[4])+i][int(values[3])] = f"S{values[1]}"
            player.layout = copy.deepcopy(new_layout)
        except IndexError:
            log.warning(f"{player.name} tried to place a ship out of bounce")
        except Exception as e:
            if str(e) == "ships crashing":
                log.warning(f"{player.name} tried to place a ship on top of another ship")

        log.info(f"{player.name} placed a ship")
