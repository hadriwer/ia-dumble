from src.game.hand import *

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = Hand()

    def add_card(self, card):
        self.hand.add_card(card)

    def get_sum(self):
        """Return hand sum of the player."""
        return self.hand.sum_hand()

    def can_dumble(self):
        return self.hand.sum_hand() <= 10