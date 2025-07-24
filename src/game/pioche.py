from src.game.cards import *
import random

class Pioche:
    def __init__(self):
        self.pioche = [
            Carte(valeur, couleur)
            for valeur in ["Joker", "Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]
            for couleur in ["Spades", "Hearts", "Diamonds", "Clubs"]
        ]
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.pioche)
    
    def draw_card(self):
        return self.pioche.pop(0)