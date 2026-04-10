import logger as log
import time

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
        print(values)
        print(player.layout)
        player.layout[int(values[3])][int(values[2])] = values[1]
        log.info(f"{player.name} placed a ship")
