from game.game import *
from game.cards import Carte
import pytest

@pytest.fixture
def game() -> Game:
    return Game()

def test_cartes_is_kind(game: Game):
    kind = [Carte("Ace", "Club")]
    assert game.is_same_kind(kind) == True, "Une seule carte"

def test_cartes_is_pair1(game : Game):
    carte1 = Carte("Joker", "")
    carte2 = Carte("7", "")
    kind = [carte1, carte2]
    assert game.is_same_kind(kind) == True, "Les cartes forment une paire"

def test_cartes_is_pair2(game : Game):
    carte1 = Carte("Joker", "")
    carte2 = Carte("7", "")
    kind = [carte2, carte1]
    assert game.is_same_kind(kind) == True, "Les cartes forment une paire"

def test_cartes_is_brelan(game : Game):
    carte1 = Carte("Joker", "")
    carte2 = Carte("3", "")
    carte3 = Carte("3", "")
    kind = [carte2, carte1, carte3]
    assert game.is_same_kind(kind) == True, "Les cartes forment un brelan"

def test_cartes_is_brelan(game : Game):
    carte1 = Carte("Queen", "")
    carte2 = Carte("Queen", "")
    carte3 = Carte("Queen", "")
    kind = [carte1, carte2, carte3]
    assert game.is_same_kind(kind) == True, "Les cartes forment un brelan"

def test_cartes_is_brelan_failed1(game : Game):
    carte1 = Carte("Joker", "")
    carte2 = Carte("4", "")
    carte3 = Carte("3", "")
    kind = [carte1, carte2, carte3]
    assert game.is_same_kind(kind) == False, "Les cartes forment un brelan"

def test_cartes_is_brelan_failed2(game : Game):
    carte1 = Carte("Joker", "")
    carte2 = Carte("3", "")
    carte3 = Carte("4", "")
    kind = [carte1, carte2, carte3]
    assert game.is_same_kind(kind) == False, "Les cartes forment un brelan"

def test_cartes_is_brelan_failed3(game : Game):
    carte1 = Carte("3", "")
    carte2 = Carte("Joker", "")
    carte3 = Carte("4", "")
    kind = [carte1, carte2, carte3]
    assert game.is_same_kind(kind) == False, "Les cartes forment un brelan"

def test_cartes_is_brelan_failed4(game : Game):
    carte1 = Carte("3", "")
    carte2 = Carte("4", "")
    carte3 = Carte("Joker", "")
    kind = [carte1, carte2, carte3]
    assert game.is_same_kind(kind) == False, "Les cartes forment un brelan"

def test_cartes_is_brelan_failed5(game : Game):
    carte1 = Carte("4", "")
    carte2 = Carte("3", "")
    carte3 = Carte("Joker", "")
    kind = [carte1, carte2, carte3]
    assert game.is_same_kind(kind) == False, "Les cartes forment un brelan"