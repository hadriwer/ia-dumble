class Carte:
    def __init__(self, valeur, couleur):
        self.valeur = valeur
        self.couleur = couleur

    def get_value(self):
        """Give value of each card. Example : Joker == 0, King == 10, Queen == 10"""
        match self.valeur:
            case "Joker": return 0
            case "Ace": return 1
            case "Jack": return 10
            case "Queen": return 10
            case "King": return 10
            case _: return int(self.valeur)

    def __str__(self):
        return f"{self.valeur} of {self.couleur}"
    
    def __repr__(self):
        return f"{self.valeur} of {self.couleur}"
    
    def __eq__(self, other):
        if isinstance(other, Carte):
            return self.valeur == other.valeur and self.couleur == other.couleur
        return False
    
    def __lt__(self, other):
        # Comparaison basée sur la valeur, puis la couleur
        if self.valeur != other.valeur:
            return self.valeur < other.valeur
        return self.couleur < other.couleur