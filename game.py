# from __future__ import annotations
import random
from card import Card, PlayerCard
from player import Player
from functools import partial
from rule_set import RuleSet

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

    def get_card_list_by_val(self, cards):
        ret = {value: [] for value in [1,2,3,4,5]}
        for card in cards:
            ret[card.val].append(card.color)

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
        while (self.last_round == False) and (turn_num < 600) and (self.stop != True):
            # print("player num ", self.turn)

            # print('turna ', self.turn)
            curr_player = self.players[self.turn] #type: Player
            self.get_next_action(self.player_action)

            if len(self.deck) == 0:
                self.last_round = True
            self.next_turn()
            turn_num += 1
        if self.stop != True:
            for i in range(len(self.players)):
                # print('turnb ', self.turn)
                curr_player = self.players[self.turn]  # type: Player
                self.get_next_action(self.player_action)
                self.next_turn()

        return self.endgame()


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

        if to_ret == None:
            out2()


    # @print_name
    def play_playable_card(self):
        for card in self.players[self.turn].hand: #type: PlayerCard
            if card.color_status != 'unknown' and card.val_status != 'unknown':
                if self.is_card_playable(card):
                    self.inPlay[card.color] = card.val
                    self.players[self.turn].hand.remove(card)
                    if len(self.deck) > 0:
                        self.players[self.turn].hand.append(self.deck.pop())
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
        out1_flag = False
        if self.clues == 0:
            out2()
            return

        for player in self.players:
            if player != self.players[self.turn]:
                for card in player.hand:
                    if card.val == 1 and card.val_status == 'unknown':
                        out1()
                        out1_flag = True
        if not out1_flag:
            out2()

    # @print_name
    def tell_about_ones(self):
        for player in self.players:
            if player != self.players[self.turn]:
                for card in player.hand:
                    if card.val == 1 and card.val_status == 'unknown':
                        self.players[self.turn].tell_info(player, 1, self)
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


if __name__=='__main__':
    game = Game(2)
    # game.run_game()
    player1 = game.players[0]
    #
    bla = partial(RuleSet.has_playable_card, player= player1)
    print( bla() )
    # p = partial(print,end = 'lol')
    # p('haha')
    game.print_discards()
    game.print_inPlay()
    game.print_deck()
    game.place_card(Card('red',1))
    game.place_card(Card('red', 1))
    game.place_card(Card('red', 1))
    game.place_card(Card('red', 1))
    print(Game.generate_counts())

