from src.game.cards import Carte

class Hand:
    def __init__(self):
        self.hand = []
    
    def add_card(self, carte):
        self.hand.append(carte)

    def sum_hand(self):
        return sum(carte.get_value() for carte in self.hand)
    
    def delete(self, cartes_select: list[Carte]):
        self.hand = [carte for carte in self.hand if carte not in cartes_select]