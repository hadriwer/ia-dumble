import gym
from gym import spaces
import numpy as np
from src.game.game import Game
from itertools import combinations

class CardGameEnv(gym.Env):
    def __init__(self, verbose=False):
        super().__init__()
        self.turn_cnt = 0
        self.verbose = verbose
        self.game = Game()
        self.action_space = spaces.Discrete(256)  # 7 cartes + 1 pour draw choice
        self.observation_space = spaces.Box(low=0, high=20, shape=(13, 18), dtype=np.int32)

    def reset(self):
        self.turn_cnt = 0
        self.game = Game()
        return self._get_obs()

    def step(self, action):
        action = list(map(int, format(action, "08b")))
        player = self.game.current_player()
        hand = sorted(player.hand.hand, key=lambda c: (self.game.valeur_to_int(c.valeur), self.game.couleur_to_int(c.couleur)))
        self.turn_cnt += 1
        reward = 0
        done = False

        if len(action) != 8:
            raise ValueError(f"L'action doit avoir exactement 8 éléments, reçu {len(action)}")

        play_part = action[:-1]
        draw_choice = int(action[-1])

        card_select = [
            card for i, card in enumerate(hand)
            if i < len(play_part) and play_part[i] == 1
        ]

        if self.verbose:
            print(f"Main J | {hand}")
            print(f"SelC J | {card_select}")
            print(f"Bin    | {self.game.bin[0] if self.game.bin else '[]'}")
            if not card_select or not self.game.can_play(card_select):
                print(f"⚠️ Mauvaise action — Play: {play_part}, Draw: {draw_choice}")

        # regarde si l'IA a fini
        if self.game.is_finished():
            if self.verbose:
                print("L'IA a dumble")
            reward += 200
            reward += max(0, 30 - self.turn_cnt) * 2
            return self._get_obs(), reward, True, {}

        # si l'action n'est pas valide
        if not self._is_valid_action(action) or not card_select:
            reward -= 30
            return self._get_obs(), reward, False, {}
        
        if self.turn_cnt > 2 and len(hand) == 7:
            reward -= self.turn_cnt
            if self.verbose: print("TROP DE CARTES ON PUNIT")

        reward_len_hand = [0, 100, 50, 40, 30, 20, 10, 0]
        reward += reward_len_hand[len(hand)]

        # récompense dans la valeur des cartes selectionnées
        best_combos = self.find_valid_combinations(hand)

        combo_score = self.get_combo_score(card_select)
        reward += combo_score

        # Score max possible dans la main
        max_score = 0
        for combo in best_combos:
            score = self.get_combo_score(combo)
            if score > max_score:
                max_score = score

        if combo_score < max_score:
            penalty = max_score - combo_score
            reward -= penalty * 0.5
            if self.verbose: print(f"❌ Mauvais choix. Joué {combo_score}, possible {max_score}")
        else:
            reward += combo_score * 0.2
            if self.verbose: print(f"✅ Bon choix. Joué {combo_score}, possible {max_score}")


        if len(card_select) == 1:
            if self.game.has_straight(hand):
                reward -= 70
                if self.verbose: print("❌ L'IA pouvait jouer une suite")
        
            if self.game.has_pair(hand):
                reward -= 20
                if self.verbose: print("❌ L'IA pouvait jouer une paire")

            if self.game.has_brelan(hand):
                reward -= 50
                if self.verbose: print("❌ L'IA pouvait jouer un brelan")

            if self.game.has_carre(hand):
                reward -= 80
                if self.verbose: print("❌ L'IA pouvait jouer un carré")

        # Soit l'IA pioche ou tire dans la défausse
        if draw_choice == 0:
            if self.verbose: print("On pioche dans la PIOCHE")
            self.game.current_player_pioche()
        elif draw_choice == 1 and self.game.bin and self.game.bin[0]:
            if self.verbose: print("On picohe dans la DÉFAUSSE")
            player.add_card(self.game.bin[0][0])
            del self.game.bin[0][0]

        # Enlève cartes jouées et ajoute à la défausse
        player.hand.delete(card_select)
        self.game.bin.insert(0, card_select)

        # Tour de l'adversaire
        self.game.change_player()
        if self.verbose:
            print("Tour de l’adversaire")
            print(f"Main  A | {self.game.current_player().hand.hand}")
        done = self.game.is_finished()

        if done:
            if self.game.current_player().get_sum() <= player.get_sum():
                if self.verbose:
                    print("L’adversaire gagne")
                reward -= 200
            else:
                reward += 200
                if self.verbose:
                    print("On gagne malgré le Dumble adverse")
        else:
            self.simulate_adversary_turn()
        self.game.change_player()
        
        return self._get_obs(), reward, done, {}
    
    def get_combo_score(self, cards):
        if not cards:
            return 0
        sum_val = self.game.get_sum_card_select(cards)
        if self.is_four_of_a_kind(cards):
            return 200 + sum_val
        elif self.is_three_of_a_kind(cards):
            return 120 + sum_val
        elif self.game.is_straight(cards):
            return 160 + sum_val
        elif self.is_pair(cards):
            return 100 + sum_val
        elif len(cards) == 1:
            return 10 + sum_val
        return 0
    
    def is_pair(self, cards):
        return len(cards) == 2 and cards[0].valeur == cards[1].valeur
    
    def is_three_of_a_kind(self, cards):
        return len(cards) == 3 and cards[0].valeur == cards[1].valeur == cards[2].valeur
    
    def is_four_of_a_kind(self, cards):
        return len(cards) == 4 and cards[0].valeur == cards[1].valeur == cards[2].valeur == cards[3].valeur

    def simulate_adversary_turn(self):
        adversary = self.game.current_player()
        hand = adversary.hand.hand

        valid_combos = self.find_valid_combinations(hand)
        
        if valid_combos:
            # Trier les combinaisons par somme décroissante des cartes
            valid_combos.sort(key=lambda combo: self.game.get_sum_card_select(combo), reverse=True)

            # Sélectionner la meilleure combinaison après tri
            # best_combo = valid_combos[0]  # La combinaison avec la plus grande somme
            best_combo = valid_combos[len(valid_combos) // 4]

            adversary.hand.delete(best_combo)
            self.game.bin.insert(0, best_combo)

            if self.verbose:
                print(f"🤖 Adversaire joue : {best_combo}")
        else:
            if self.verbose:
                print("🤖 Adversaire passe (aucun coup valide)")

        self.game.current_player_pioche()

    def find_valid_combinations(self, hand):
        from itertools import combinations
        valid_combos = []
        for r in range(1, min(5, len(hand) + 1)):
            for combo in combinations(hand, r):
                if self.game.can_play(list(combo)):
                    valid_combos.append(list(combo))
        return valid_combos
    
    def _is_valid_action(self, action):
        player = self.game.current_player()
        hand = sorted(player.hand.hand, key=lambda c: self.game.valeur_to_int(c.valeur))

        if len(action) != 8:
            return False

        play_part = action[:-1]
        draw_choice = int(action[-1])

        # Cartes sélectionnées à jouer
        card_select = [card for i, card in enumerate(hand) if i < len(play_part) and play_part[i] == 1]

        # Validation du draw_choice : 0 ou 1 uniquement
        if draw_choice not in (0, 1):
            return False

        # Nombre de cartes jouées entre 0 et 4 (selon règles max 4)
        n = len(card_select)
        if n == 0:
            # On ne joue aucune carte, on pioche forcément (0 ou 1 draw OK)
            return True

        if n > 4:
            return False  # On ne peut pas jouer plus de 4 cartes d'un coup

        # Helpers : conversion valeurs et couleurs
        values = [self.game.valeur_to_int(c.valeur) for c in card_select]
        colors = [c.couleur for c in card_select]

        # Fonction vérif paire/brelan/carré
        def all_same_value(vals):
            return all(v == vals[0] for v in vals)

        # Fonction vérif suite même couleur (tierce)
        def is_tierce(cards):
            if len(cards) != 3:
                return False
            sorted_cards = sorted(cards, key=lambda c: self.game.valeur_to_int(c.valeur))
            vals = [self.game.valeur_to_int(c.valeur) for c in sorted_cards]
            cols = [c.couleur for c in sorted_cards]
            if len(set(cols)) != 1:
                return False
            return vals[1] == vals[0] + 1 and vals[2] == vals[1] + 1

        # Valide selon nombre de cartes
        if n == 1:
            # Une carte seule OK
            return True
        elif n == 2:
            # Paire : même valeur
            return all_same_value(values)
        elif n == 3:
            # Brelan ou tierce
            return all_same_value(values) or is_tierce(card_select)
        elif n == 4:
            # Carré : même valeur
            return all_same_value(values)

        # Sinon invalide
        return False


    def _get_obs(self):
        player = self.game.current_player()
        hand = sorted(player.hand.hand[:7], key=lambda c: (self.game.valeur_to_int(c.valeur), self.game.couleur_to_int(c.couleur)))

        flat_obs = []
        for card in hand:
            flat_obs.append(self._encode_card(card))

        while len(flat_obs) < 7:
            flat_obs.append([0] * 18)  # padding

        valid_combos = self.find_valid_combinations(hand)

        has_pair = any(self.is_pair(combo) for combo in valid_combos)
        has_brelan = any(self.is_three_of_a_kind(combo) for combo in valid_combos)
        has_straight = any(self.game.is_straight(combo) for combo in valid_combos)
        has_carre = any(self.is_four_of_a_kind(combo) for combo in valid_combos)
        has_combo_10_plus = any(self.game.get_sum_card_select(combo) >= 10 for combo in valid_combos)

        global_features = [
            [int(has_pair)] + [0] * 17,
            [int(has_brelan)] + [0] * 17,
            [int(has_straight)] + [0] * 17,
            [int(has_carre)] + [0] * 17,
            [int(has_combo_10_plus)] + [0] * 17,
            [len(hand)] + [0] * 17
        ]

        flat_obs.extend(global_features)

        return np.array(flat_obs, dtype=np.int32)
    
    def _encode_card(self, card):
        val_encoding = [0] * 14
        color_encoding = [0] * 4
        val_encoding[self.game.valeur_to_int(card.valeur)] = 1
        color_encoding[self.game.couleur_to_int(card.couleur)] = 1
        return val_encoding + color_encoding