import pygame
from game.cards import Carte

class CardSprite:
    def __init__(self, card: Carte, x, y, font):
        self.card = card
        self.rect = pygame.Rect(x, y, 100, 150)
        self.font = font
        self.color = (200,200,255)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, border_radius=12)
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 2, border_radius=12)

        name_surf = self.font.render(self.card.couleur, True, (0, 0, 0))
        surface.blit(name_surf, (self.rect.x + 10, self.rect.y + 10))

        if self.card.valeur is not None:
            value_surf = self.font.render(str(self.card.valeur), True, (0, 0, 0))
            surface.blit(value_surf, (self.rect.x + 10, self.rect.y + 70))
