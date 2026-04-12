import random

class Player:
    def __init__(self, name, player_id):
        self.name = name
        self.player_id = player_id
        self.is_my_turn = False
        self.turn_start = 0
        self.time_for_turn = 15
        self.setup = False
        self.shoots_fired = 0

        # Set on Server in Game logic
        self.time_for_layout = 0
        self.layout = []
        self.enemy_layout = []
        self.inventory = []
