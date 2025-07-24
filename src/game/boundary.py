import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.game.game import Game
from src.game.cards import Carte

SEPARATOR = 10

def clear_screen():
    print("\033c", end="")

def separator(sep):
    for _ in range(SEPARATOR):
        print(sep, end="")
    print()

def print_cartes(cartes: list[Carte]):
    for i, carte in enumerate(cartes):
        print(f"{i+1}. {carte.valeur} of {carte.couleur}")

def main():
    game = Game()
    running = True

    while running:

        current_player = game.current_player()
        clear_screen()
        separator("-")
        print(f"C'est au tour du joueur : {current_player.name}")
        print(f"Carte de la main du joueur : {current_player.name}")
        current_player.hand.hand.sort()
        print_cartes(current_player.hand.hand)
        separator("-")
        print("Carte de la zone de défausse (dernière main): ")
        print_cartes(game.bin[0])
        separator("-")

        if current_player.can_dumble():
            separator("-")
            print(f"Vous pouvez dire Dumble ! Votre score = {current_player.hand.sum_hand()}.")
            print("1. Dire Dumble.")
            print("2. Continuer le jeux.")
            res = int(input("Votre choix : "))
            if res == 1:
                running = False
                separator("-")
                print("Le jeu est terminé.")
                game.print_joueur_sum()
            else:
                print("La partie continue.")

        tf = True
        while tf and running:
            print("Qu'elles cartes voulez vous jouer ? (En séparant par un espace).")
            play = str(input("-> "))
            card_to_play = play.split(" ")
            cards = [current_player.hand.hand[int(i) - 1] for i in card_to_play]

            if game.can_play(cards):
                tf = False
                current_player.hand.delete(cards)
                print("Voulez vous : ")
                print("1. Piocher.")
                print("2. Choisir parmis la défausse.")
                res = int(input("Votre choix : "))
                if res == 1:
                    game.current_player_pioche()
                else:
                    separator("#")
                    print("Choissisez une carte de défausse :")
                    print_cartes(game.bin[0])
                    res = int(input("Votre choix : "))
                    select = game.bin[0][res - 1]
                    print(f"La carte selectionnée est : {select.valeur} of {select.couleur}")
                    game.current_player().add_card(select)
                    del game.bin[0][res - 1]
                game.bin.insert(0, cards)
                game.change_player()
                print("On change de joueur")
            else:
                print("Vous ne pouvez vous pas jouer ceci.")

main()