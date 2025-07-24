import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pygame
import sys
from game.game import Game
from game.cards import Carte
from cardSprite import CardSprite

# Initialisation de Pygame
pygame.init()
font = pygame.font.Font(None, 36)

# Configuration de la fenêtre
WIDTH, HEIGHT = 1000, 600
CARD_WIDTH, CARD_HEIGHT = 100, 150
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Boucle de jeu Dumble")

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Horloge pour contrôler le framerate
clock = pygame.time.Clock()
game = Game()

def draw_button(screen, text, x, y, width, height, font, color, text_color):
    """Dessine un bouton avec du texte."""
    pygame.draw.rect(screen, color, (x, y, width, height))
    label = font.render(text, True, text_color)
    text_rect = label.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(label, text_rect)

def is_button_clicked(pos, x, y, width, height):
    """Vérifie si un clic est sur le bouton."""
    return x <= pos[0] <= x + width and y <= pos[1] <= y + height

card_sprites = []
card_selected = []

def update_card_sprites():
    """Met à jour les sprites des cartes en fonction du joueur actuel."""
    global card_sprites
    card_sprites = []  # Réinitialise la liste des sprites
    curr_player = game.current_player()  # Récupère le joueur actuel
    for i, card in enumerate(curr_player.hand.hand):
        sprite = CardSprite(card, 50 + i * (CARD_WIDTH + 20), 400, font)
        card_sprites.append(sprite)

    for i, card in enumerate(game.bin[0]):
        sprite = CardSprite(card, 50 + i * (CARD_WIDTH + 20), 200, font)
        card_sprites.append(sprite)

    pioche_sprite = CardSprite(Carte("Pioche", None), WIDTH - CARD_WIDTH - 50, 200, font)
    card_sprites.append(pioche_sprite)
        

def change_color_selected_card_sprites(pos):
    for sprite in card_sprites:
        if sprite.rect.collidepoint(pos):
            color = (200,200,255) if sprite.color == (0,0,255) else (0,0,255)
            sprite.color = color
            if sprite in card_selected:
                card_selected.remove(sprite)
            else:
                card_selected.append(sprite)
    print(f"Card select = {card_selected}")


red_timer = 0
# Boucle principale du jeu
def main_game_loop():
    running = True
    button_width, button_height = 200, 50
    update_card_sprites()
    global red_timer
    while running:
        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if is_button_clicked(pos, 250, 10, button_width, button_height):
                    card_selected_not_sprite = [sprite.card for sprite in card_selected]
                    if card_selected != [] and game.can_play(card_selected_not_sprite):
                        card_selected.clear()
                        print("yes")
                        game.bin.insert(0, card_selected_not_sprite)
                        game.current_player().hand.delete(card_selected_not_sprite)

                        while not card_selected:
                            print("Veuillez sélectionner une carte.")
                            for event in pygame.event.get():
                                if event.type == pygame.MOUSEBUTTONDOWN:
                                    pos = pygame.mouse.get_pos()
                                    change_color_selected_card_sprites(pos)
                        
                        curr = card_selected[0].card
                        if curr.valeur == "Pioche":
                            game.current_player_pioche()
                        else:
                            game.current_player().add_card(curr)
                            game.bin.pop(0)

                        card_selected.clear()
                        game.change_player()
                        game.bin.insert(0, card_selected_not_sprite)
                        print(f"On change de joueur = {game.current_player().name}")
                        update_card_sprites()
                    else:
                        for sprite in card_selected:
                            sprite.color = (255,0,0)
                        red_timer = pygame.time.get_ticks()

                else:
                    change_color_selected_card_sprites(pos)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game.change_player()
                    update_card_sprites()
        # Fin event

        if game.is_finished():
            print(f"Le jeu est fini")
            game.print_joueur_sum()
            running = False

        # Mise à jour de l'état du jeu
        if red_timer and pygame.time.get_ticks() - red_timer > 1000:
            for sprite in card_selected:
                sprite.color = (200, 200, 255)
            card_selected.clear()
            red_timer = 0
        # Ajoutez ici la logique de mise à jour (exemple : déplacement, collisions, etc.)

        # Rendu graphique
        screen.fill(WHITE)  # Efface l'écran avec une couleur de fond
        label = font.render(f"Tour de : {game.current_player().name}", True, BLACK)
        draw_button(screen, "Jouer", 250, 10, button_width, button_height, font, (0, 128, 0), WHITE)
        screen.blit(label, (10, 10))
        # Ajoutez ici le rendu des éléments du jeu (exemple : joueurs, cartes, etc.)
        for sprite in card_sprites:
            sprite.draw(screen)

        pygame.display.flip()  # Met à jour l'écran

        # Contrôle du framerate
        clock.tick(60)  # Limite à 60 FPS

    pygame.quit()
    sys.exit()

# # Lancer la boucle de jeu
# if __name__ == "__main__":
#     main_game_loop()