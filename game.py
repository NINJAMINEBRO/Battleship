import logger as log
import time

class Game:
    def __init__(self, players):
        self.players = players
        self.starttime = 0
        self.current_phase = 0
        self.game_over = False
        self.turn_count = 0
        self.duration = 0
        self.time_for_turn = 10

    def add_player(self, player):
        """
        Adds a player to the game.
        :param player: The player to add (string).
        """
        if player not in self.players:
            self.players.append(player)
            log.success(f"Player {player.name} added to game.")
        else:
            log.info(f"Player {player.name} is already in the game.")

    def remove_player(self, player):
        """
        Removes a player from the game.
        :param player: The player to remove (string).
        """
        if player in self.players:
            self.players.remove(player)
            log.success(f"Player {player.name} removed from game.")
        else:
            log.info(f"Player {player.name} is not in the game.")

    def start_game(self):
        if len(self.players) < 2:
            log.info("Not enough players to start the game.")
            return False

        self.players[0].is_my_turn = True
        log.success(f"Game started with players: {', '.join([player.name for player in self.players])}")
        self.players[0].turn_start = time.time()
        self.starttime = time.time()

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
        if player.is_my_turn and player.turn_start + self.time_for_turn <= time.time():
            log.info(f"{player.name} has run out of time.")
            self.next_player()

    def is_game_over(self):
        if len(self.players) >= 2:
            pass
        if self.game_over:
            self.duration = time.time() - self.starttime
            return True
        return False
