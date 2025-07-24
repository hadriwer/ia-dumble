from src.game.pioche import Pioche
from src.game.player import *
from src.game.cards import *
from collections import Counter

NOMBRE_JOUEUR = 2
CARTES_DISTRIBUER = 7

class Game:
    def __init__(self):
        self.pioche = Pioche()
        self.init_player()
        self.distribute(CARTES_DISTRIBUER)
        self.bin = [[self.draw_card()]]

    def init_player(self):
        nb_player = NOMBRE_JOUEUR
        self.players = [Player(f"Joueur{num+1}") for num in range(nb_player)]

    def draw_card(self) -> Carte:
        """Draw card on the 'PIOCHE'. Return the card from it. Delete from it."""
        if not self.pioche.pioche:
            for i in range(1,len(self.bin)):
                for j in range(0, len(self.bin[i])):
                    self.pioche.pioche.append(self.bin[i][j])
            self.pioche.shuffle()
        return self.pioche.draw_card()

    def distribute(self, number: int):
        for player in self.players:
            for _ in range(number):
                card = self.draw_card()
                player.add_card(card)

    def current_player(self):
        return self.players[0]
    
    def current_player_pioche(self):
        return self.current_player().hand.add_card(self.draw_card())
    
    def change_player(self):
        curr = self.players.pop(0)
        self.players.append(curr)
    
    def is_same_kind(self, cartes):
        if len(cartes) == 1:
            return True

        tf = True
        pred = cartes[0]
        for carte in cartes:
            tf = (tf and (carte.valeur == pred.valeur or pred.valeur == "Joker" or carte.valeur == "Joker"))
            if carte.valeur != "Joker":
                pred = carte

        return tf

    # Fonction vérif suite même couleur (tierce)
    def is_straight(self, cards):
        if len(cards) != 3:
            return False
        sorted_cards = sorted(cards, key=lambda c: self.valeur_to_int(c.valeur))
        vals = [self.valeur_to_int(c.valeur) for c in sorted_cards]
        cols = [c.couleur for c in sorted_cards]
        if len(set(cols)) != 1:
            return False
        return vals[1] == vals[0] + 1 and vals[2] == vals[1] + 1

    
    def can_play(self, cartes: list[Carte]):
        return self.is_same_kind(cartes) or self.is_straight(cartes)
    
    def is_finished(self):
        return self.current_player().can_dumble()
    
    def print_joueur_sum(self):
        for player in self.players:
            print(f"{player.name} a obtenu {player.get_sum()}.")

    def get_sum_card_select(self, card_selected : list[Carte]) -> int:
        return sum(carte.get_value() for carte in card_selected)
    
    def get_ranks(self, hand):
        """Extrait les valeurs des cartes ("As", "Joker" ...)."""
        return [self.valeur_to_int(card.valeur) for card in hand]
    
    def has_pair(self, hand):
        """Renvoie True si une paire est présente (au moins deux cartes de même rang)."""
        ranks = self.get_ranks(hand)
        counts = Counter(ranks)
        return any(count == 2 for count in counts.values())

    def has_brelan(self, hand):
        """Renvoie True si un brelan est présent (trois cartes du même rang)."""
        ranks = self.get_ranks(hand)
        counts = Counter(ranks)
        return any(count == 3 for count in counts.values())

    def has_carre(self, hand):
        """Renvoie True si un carré est présent (quatre cartes du même rang)."""
        ranks = self.get_ranks(hand)
        counts = Counter(ranks)
        return any(count == 4 for count in counts.values())

    def has_straight(self, hand):
        """Renvoie True si une suite d'au moins 3 cartes consécutives de même couleur est présente."""
        # Regrouper les cartes par couleur
        suit_groups = {}
        for card in hand:
            suit = card.couleur
            if suit not in suit_groups:
                suit_groups[suit] = []
            suit_groups[suit].append(self.valeur_to_int(card.valeur))  # convertit les valeurs en int

        # Vérifie les suites dans chaque groupe de couleur
        for ranks in suit_groups.values():
            if len(ranks) < 3:
                continue
            sorted_ranks = sorted(set(ranks))
            for i in range(len(sorted_ranks) - 2):
                if sorted_ranks[i+1] == sorted_ranks[i] + 1 and \
                sorted_ranks[i+2] == sorted_ranks[i] + 2:
                    return True

        return False
    
    def valeur_to_int(self, v):
        return {
            "Joker" : 0,
            "Ace" : 1,
            "2": 2, "3": 3, "4": 4, "5": 5,
            "6": 6, "7": 7, "8": 8, "9": 9,
            "10": 10, "Jack": 11, "Queen": 12, "King": 13
        }.get(v, 0)

    def couleur_to_int(self, c):
        return {"Hearts": 0, "Diamonds": 1, "Clubs": 2, "Spades": 3}.get(c, 0)
