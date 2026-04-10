import random

class Player:
    def __init__(self, name, player_id):
        self.name = name
        self.player_id = player_id
        self.is_my_turn = False
        self.turn_start = 0
        self.time_for_turn = 15
        self.time_for_layout = 60
        self.layout = []
        self.setup = False
        self.inventory = []
