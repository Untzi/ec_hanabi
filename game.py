# from __future__ import annotations
import random
from card import Card, PlayerCard
from player import Player
from functools import partial
from rule_set import RuleSet

p = 0.6
colors = ['blue', 'red', 'yellow', 'white', 'green']
val_count = {1: 3, 2: 2, 3: 2, 4: 2, 5: 1}

def print_name(func):
    def echo_func(*func_args, **func_kwargs):
        print(func.__name__)
        return func(*func_args, **func_kwargs)
    echo_func.__name__ = func.__name__
    return echo_func

class Game:
    def __init__(self, players_num, player_action_tree):
        # random.seed(1)
        self.deck = self.create_deck()
        self.discards = []
        self.clues = 8
        self.strikes = 3
        self.turn = 0
        self.last_round = False
        self.players = []
        self.inPlay = {color: 0 for color in colors}
        self.player_action = player_action_tree
        self.stop = False
        for player in range(players_num):
            hand = []
            for i in range(5):
                hand.append(self.deck.pop())
            player = Player(player, hand, self)
            self.players.append(player)
            # print(player)

    def reset(self, players_num, player_action_tree):
        self.deck = self.create_deck()
        self.discards = []
        self.clues = 8
        self.strikes = 3
        self.turn = 0
        self.last_round = False
        self.players = []
        self.inPlay = {color: 0 for color in colors}
        self.player_action = player_action_tree
        self.stop = False
        for player in range(players_num):
            hand = []
            for i in range(5):
                hand.append(self.deck.pop())
            player = Player(player, hand, self)
            self.players.append(player)

    def get_curr_player(self):
        return self.players[self.turn]

    def raise_clues(self):
        self.clues = self.clues+1 if self.clues+1 < 9 else 8

    def place_card(self, card:Card):
        color = card.color
        if self.inPlay[color] == card.val-1:
            self.raise_clues()
            self.inPlay[color] = card.val
            # print('legal card!! clues: '+ str(self.clues))
        else:
            if self.strikes > 0:
                self.strikes -= 1
                self.discards.append(card)
            if self.strikes == 0:
                self.last_round = True
                self.stop = True
                return
            # print('ilegal card!! strikes:' + str(self.strikes))

    def endgame(self):
        final_score = sum(self.inPlay.values())
        # print('final ' + str(final_score))
        fd = open('results.txt','a')
        fd.write(str(final_score) + '\n')
        fd.close()
        return (final_score)

    # @print_name
    def next_turn(self):
        self.turn = (self.turn+1) % len(self.players)
        return self.turn

    def get_card_list_by_color(self,cards):
        ret = {color: [] for color in colors}
        for card in cards:
            ret[card.color].append(card.val)
        return ret
    def get_card_list_by_val(self, cards):
        ret = {value: [] for value in [1,2,3,4,5]}
        for card in cards:
            ret[card.val].append(card.color)
        return ret

    @staticmethod
    def create_deck():
        deck = []
        for color in colors:
            for val, count in val_count.items():
                cards = [Card(color, val) for _ in range(count)]
                deck = deck + cards
        random.shuffle(deck)
        return deck

    @staticmethod
    def generate_counts():
        to_ret = {}
        for color in colors:
            to_ret[color] = [1, 1, 1, 2, 2, 3, 3, 4, 4, 5]
        return to_ret

    def print_deck(self):
        print([str(card) for card in self.deck])

    def print_discards(self):
        print([str(card) for card in self.discards])

    def print_inPlay(self):
        print(self.inPlay)

    def get_next_action(self, player_action_tree):
        player_action_tree()

    def run_game(self):
        turn_num = 0
        # print("start game")
        while (self.last_round == False) and (turn_num < 600) and (self.stop != True) and (self.strikes != 0):
            # print("player num ", self.turn)

            # print('turna ', self.turn)
            curr_player = self.players[self.turn] #type: Player
            counts = curr_player.deduction()
            curr_player.update_safe_probabilities(counts)
            self.get_next_action(self.player_action)

            if len(self.deck) == 0:
                self.last_round = True
            self.next_turn()
            turn_num += 1
        if self.stop != True and (self.strikes != 0):
            for i in range(len(self.players)):
                # print('turnb ', self.turn)
                curr_player = self.players[self.turn]  # type: Player
                counts = curr_player.deduction()
                curr_player.update_safe_probabilities(counts)
                self.get_next_action(self.player_action)
                self.next_turn()

        return self.endgame()

    def get_next_playable(self, color):
        return self.inPlay[color] + 1

    def is_card_playable(self, card):
        inPlay = self.inPlay
        return inPlay[card.color] == (card.val - 1)

    # @print_name
    def has_playable_card(self, out1, out2):
        to_ret = None
        for card in self.players[self.turn].hand: #type: PlayerCard
            if card.color_status != 'unknown' and card.val_status != 'unknown':
                if self.is_card_playable(card):
                    out1()
                    to_ret = card

        if isinstance(to_ret, type(None)):
            out2()


    # @print_name
    def play_playable_card(self):
        for card in self.players[self.turn].hand: #type: PlayerCard
            if card.color_status != 'unknown' and card.val_status != 'unknown':
                if self.is_card_playable(card):
                    self.inPlay[card.color] = card.val
                    self.players[self.turn].hand.remove(card)
                    if len(self.deck) > 0:
                        self.players[self.turn].hand.append(PlayerCard(self.deck.pop()))
                    if len(self.deck) == 0:
                        self.last_round = True
                    if self.clues < 8:
                        self.clues += 1

    def can_tell(self, out1, out2):
        if self.clues > 0:
            out1()
        else:
            out2()

    # @print_name
    def can_tell_about_ones(self, out1, out2):
        if self.clues == 0:
            out2()
            return

        for player in self.players:
            if player != self.players[self.turn]:
                for card in player.hand:
                    if card.val == 1 and card.val_status == 'unknown':
                        out1()
                        return
        out2()

    def tell_about_ones(self):
        for player in self.players:
            if player != self.players[self.turn]:
                for card in player.hand:
                    if card.val == 1 and card.val_status == 'unknown':
                        self.players[self.turn].tell_info(player, 1, self)
                        return

    def tell_about_fives(self):
        for player in self.players:
            if player != self.players[self.turn]:
                for card in player.hand:
                    if card.val == 5 and card.val_status == 'unknown':
                        self.players[self.turn].tell_info(player, 5, self)
                        return

    # @print_name
    def play_random_card(self):
        try:
            card = random.sample(self.players[self.turn].hand, 1)[0]
            self.players[self.turn].player_place_card(card, self)
        except:
            i = 1



    def discard_oldest_with_least_info(self):
        self.players[self.turn].discard_oldest_with_least_info()

    def has_probably_safe_card(self, out1, out2):
        global p
        for card in self.players[self.turn].hand:
            if card.safe_to_play_prob > p:
                out1()
                return
        out2()

    def play_safest_card(self):
        max_prob = 0
        try:
            to_play = self.players[self.turn].hand[0]
        except IndexError:
            print('index error')
            print('deck count', self.deck)

            self.last_round = True
            self.stop = True
            return
        for card in self.players[self.turn].hand:
            if card.safe_to_play_prob > max_prob:
                to_play = card
                max_prob = card.safe_to_play_prob
        self.players[self.turn].player_place_card(to_play, self)

    def tell_random(self):
        if self.clues == 0:
            return
        for player in self.players:
            if player.player_num != self.players[self.turn].player_num:
                counter = 0
                while counter < 20:
                    rand_card = random.sample(player.hand, 1)[0] #type: PlayerCard
                    if rand_card.color_status == 'unknown' and rand_card.val_status == 'unknown':
                        to_tell = random.sample([rand_card.val, rand_card.color], 1)[0]
                        self.players[self.turn].tell_info(player, to_tell, self)
                        break
                    elif rand_card.val_status == 'unknown':
                        to_tell = rand_card.val
                        self.players[self.turn].tell_info(player, to_tell, self)
                        break
                    elif rand_card.color_status == 'unknown':
                        to_tell = rand_card.color
                        self.players[self.turn].tell_info(player, to_tell, self)
                        break
                    counter += 1

    def play_just_hinted(self):
        global p
        current_player = self.get_curr_player()
        turns_with_no_info = 100
        card_to_play = None
        for card in current_player.hand:
            if card.turns_with_no_info < turns_with_no_info and card.safe_to_play_prob > p:
                turns_with_no_info = card.turns_with_no_info
                card_to_play = card
        if card_to_play:
            current_player.player_place_card(card_to_play, self)

    def can_tell_fives(self,out1,out2):
        if self.clues == 0:
            out2()
            return

        for player in self.players:
            if player != self.players[self.turn]:
                for card in player.hand:
                    if card.val == 5 and card.val_status == 'unknown':
                        out1()
                        return
        out2()

    def is_other_has_playable_card(self, out1, out2):
        if self.clues == 0:
            out2()
            return
        curr_player = self.get_curr_player()
        for player in self.players:
            if player.player_num != curr_player.player_num:
                for card in player.hand:
                    if self.is_card_playable(card):
                        out1()
                        return
        out2()

    def tell_playable_card(self):
        curr_player = self.get_curr_player()
        for player in self.players:
            if player.player_num != curr_player.player_num:
                for card in player.hand:
                    if self.is_card_playable(card):
                        to_tell = random.sample([card.val, card.color], 1)[0]
                        self.players[self.turn].tell_info(player, to_tell, self)
                        return
        self.tell_random()

    def has_useless_card(self, out1, out2):
        discards_by_color = self.get_card_list_by_color(self.discards)
        for card in self.get_curr_player().hand:
            if card.color_status != 'unknown' and card.val_status != 'unknown':
                if self.inPlay[card.color] > card.val:
                    out1()
                    return
                else:
                    for i in range(1, card.val):
                        if discards_by_color[card.color].count(i) == val_count[i]:
                            out1()
                            return
        out2()

    def discard_useless_card(self):
        if self.clues > 8:
            return
        discards_by_color = self.get_card_list_by_color(self.discards)
        discards_by_val = self.get_card_list_by_val(self.discards)
        for card in self.get_curr_player().hand:
            if card.color_status != 'unknown' and card.val_status != 'unknown':
                if self.inPlay[card.color] > card.val:
                    self.players[self.turn].discard_card(card, self)
                    return
                else:
                    for i in range(1, card.val):
                        if discards_by_color[card.color].count(i) == val_count[i]:
                            self.players[self.turn].discard_card(card, self)
                            return


if __name__=='__main__':
    # game = Game(2)
    # # game.run_game()
    # player1 = game.players[0]
    # # p = partial(print,end = 'lol')
    # # p('haha')
    # game.print_discards()
    # game.print_inPlay()
    # game.print_deck()
    # game.place_card(Card('red',1))
    # game.place_card(Card('red', 1))
    # game.place_card(Card('red', 1))
    # game.place_card(Card('red', 1))
    print(Game.generate_counts())

